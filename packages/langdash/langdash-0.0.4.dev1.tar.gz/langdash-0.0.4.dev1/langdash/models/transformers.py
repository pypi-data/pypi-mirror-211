from typing import Generator, List, Optional, Tuple, Union, Any
from math import inf
from dataclasses import dataclass
import copy

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
from langdash.infer import InferArgs
import langdash.sampling as sampling

import transformers
import torch

@dataclass
class TransformersState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _past_key_values: Any = None
  _next_token: Optional[Tuple[int, str]] = None

class TransformersSession(LLMGenerationSessionForRawText["TransformersModel", TransformersState, torch.Tensor]):
  """
  Session for transformers model.
  """
  
  _next_token: Optional[Tuple[int, str]]
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    def load_model(llm: TransformersModel):
      model = transformers.AutoModelForCausalLM.from_pretrained(llm._model_name)
      tokenizer = transformers.AutoTokenizer.from_pretrained(llm._tokenizer_name)
      return model, tokenizer
      
    self._model, self._tokenizer = self._ld.get_model_internal(self.llm, load_model)
    
    if isinstance(
      self._tokenizer,
      (
        transformers.GPT2Tokenizer,
        transformers.GPT2TokenizerFast
      )
    ):
      self._space_token = "\u0120"
      self._buffered_token_head = set(
        v for k, v in self._tokenizer.get_vocab().items() if "\u0122" in k
      )
    else:
      self._space_token = " "
      self._buffered_token_head = set()

    self._logits = None
    self._past_key_values = None
    self._next_token = None
  
  def _heal_token(self, tok_a: int, tok_b: int) -> str:
    return self._tokenizer.decode([tok_a, tok_b])
  
  def set_state(self, state: Optional[TransformersState]):
    if state is None:
      self._logits = None
      self._past_key_values = None
      self._next_token = None
    else:
      self._logits = copy.deepcopy(state._logits)
      self._past_key_values = copy.deepcopy(state._past_key_values)
      self._next_token = state._next_token
    
  def clone_state(self) -> TransformersState:
    return TransformersState(
      _logits = copy.deepcopy(self._logits),
      _past_key_values = copy.deepcopy(self._past_key_values),
      _next_token = self._next_token,
    )
  
  def _eval(self, tokid: int):
    outputs = self._model.forward(
      torch.IntTensor([tokid]),
      past_key_values=self._past_key_values,
      use_cache=True
    )
    self._past_key_values = outputs.past_key_values
    return outputs.logits[-1]
  
  def decode(self, tokids: List[int]) -> str:
    return self._tokenizer.decode(tokids)
  
  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._tokenizer.encode(text, add_special_tokens=add_special_tokens).tolist()
  
  def _next_token_probs(self) -> torch.Tensor:
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits = self._model.forward(
        torch.IntTensor([self._next_token[0]]),
        past_key_values=self._past_key_values,
        use_cache=True
      )._logits[-1]
    return torch.nn.functional.softmax(logits, dim=-1)
  
  def _infer(self,
            end: Optional[Union[str, int]],
            args: Optional[InferArgs] = None) -> Generator[RespInfer, None, None]:
    generated = ""
    ctx: List[int] = []
    buffered_tokens: List[int] = []
    stops_at_eot = (
      (isinstance(end, str) and len(end) == 0) or
      (isinstance(end, int) and end == self._tokenizer.eos_token_id)
    )
    
    for i in range(args.max_new_tokens):
      postprocess_fn = None
      
      if i == 0 and self._next_token is not None:
        _, tokstr = self._next_token
        if tokstr == " ":
          for key, value in self._tokenizer.get_vocab().items():
            #https://github.com/openai/gpt-2/issues/80
            #starts with 0x120
            if key.startswith(self._space_token):
              self._logits[value] = -inf
          postprocess_fn = lambda x: " " + x
        else:
          for key, value in self._tokenizer.get_vocab().items():
            if not key.startswith(tokstr):
              self._logits[value] = -inf
          _tokstr_len = len(tokstr)
          postprocess_fn = lambda x: x[_tokstr_len:]
        # self._next_token = None
      
      if not stops_at_eot: # no early endoftext
        self._logits[0] = -inf
      
      tokid = sampling.sample(self._logits, args, ctx)
      ctx.append(tokid)
      
      if stops_at_eot and tokid == self._tokenizer.eos_token_id:
        break
      elif tokid in self._buffered_token_head:
        buffered_tokens.append(tokid)
      else:
        if buffered_tokens:
          tokstr = self._tokenizer.decode(buffered_tokens + [tokid])
          buffered_tokens = []
        else:
          tokstr = self._tokenizer.decode([tokid])
        
        if postprocess_fn is not None:
          tokstr = postprocess_fn(tokstr)
        
        self._next_token = (tokid, tokstr)
        
        generated += tokstr
        if isinstance(end, str) and end and generated.endswith(end):
          generated = generated[:-len(end)]
          break
      
        yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)
      
      self._logits = self._eval(tokid)
    
    yield RespInfer(tokid=0, tokstr="", running_infer=generated)

class TransformersModel(LLM[TransformersSession]):
  """
  transformers model.
  """
  Session = TransformersSession
  
  def __init__(self, model_name: str, tokenizer_name: Optional[str] = None):
    """
    Creates a template for a language model powered by the transformers library.
    
    Args:
      model_name (str):
        The name of the model.
      tokenizer_name (str):
        The name of the tokenizer.
        If None, the model_name will be used to detect the tokenizer.
    """
    if tokenizer_name is None:
      tokenizer_name = model_name
    self._model_name = model_name
    self._tokenizer_name = tokenizer_name
