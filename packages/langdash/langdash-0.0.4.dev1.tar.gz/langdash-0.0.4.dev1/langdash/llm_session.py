from typing import TypeVar, Generic, Optional, List, Generator, Union, Tuple, TYPE_CHECKING
from collections.abc import Sequence
import copy

from langdash.response import RespInfer
from langdash.chains import CalledChain, LDNodeArgs, LDNode
from langdash.infer import InferArgs
from langdash.llm import LLM

if TYPE_CHECKING:
  from langdash._langdash import Langdash

class LLMSession:
  """
  A session for LLM.
  """
  def clone(self) -> "LLMSession":
    raise NotImplementedError("clone")

class LLMState:
  """
  A state class for a language model.
  """
  pass

T_LLM = TypeVar('T_LLM', bound=LLM)
T_LLMState = TypeVar("T_LLMState", bound=LLMState)

class LLMGenerationSession(LLMSession, Generic[T_LLM, T_LLMState]):
  """ Generation session for a language model. """
  
  def __init__(self,
               llm: T_LLM,
               ld: "Langdash",
               default_infer_args: InferArgs = InferArgs(),
               track_called_chains: bool = True,
               token_healing: bool = True,
               global_args: LDNodeArgs = {}):
    self._ld = ld
    self.llm = llm
    self.default_infer_args = default_infer_args
    self.called_chains: Optional[List[CalledChain]] = (
      [] if track_called_chains else None
    )
    self.token_healing = token_healing
    self.global_args = global_args
    self.tokens_counter = 0
    
  def set_state(self, state: Optional[T_LLMState]):
    """
    Set the state of the language model.

    Args:
      state (Optional[T_LLMState]):
        The state of the language model, or None to clear the state.
    """
    raise NotImplementedError("set_state")
  
  def clone_state(self) -> T_LLMState:
    """
    Clone the current state of the language model.
    """
    raise NotImplementedError("clone_state")
  
  def clone(self) -> "LLMGenerationSession":
    """
    Clone the current session.
    """
    session = self.__class__(
      llm=self.llm,
      ld=self._ld,
      default_infer_args=self.default_infer_args,
      track_called_chains=False,
      global_args=copy.copy(self.global_args)
    )
    session.set_state(self.clone_state())
    if self.called_chains is not None:
      session.called_chains = copy.copy(self.called_chains)
    return session
  
  def _append_called_chain(self,
                           node: LDNode,
                           args: LDNodeArgs,
                           tokens_used: int):
    if self.called_chains is None:
      pass
    else:
      self.called_chains.append(CalledChain(node=node, args=args, tokens_used=tokens_used))
  
  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    """
    Tokenize the given text into a list of tokens.

    Args:
      text (str): The text to tokenize.
      add_special_tokens (bool): Whether to add special tokens to the output.

    Returns:
      (List[int]) The list of tokens.
    """
    raise NotImplementedError("tokenize")
  
  def decode(self, tokids: List[int]) -> str:
    raise NotImplementedError("decode")
  
  def next_token_probs(self) -> List[float]:
    """
    Returns the probabilities for next token.
    """
    raise NotImplementedError("next_token_probs")
  
  def _infer(self,
            end: Optional[Union[str, int]],
            args: Optional[InferArgs] = None) -> Generator[RespInfer, None, None]:
    raise NotImplementedError("_infer")

  def infer(self,
            end: Optional[Union[str, int]],
            args: Optional[InferArgs] = None) -> Generator[RespInfer, None, None]:
    """
    Infer the next token from the input sequence.

    Args:
      end (Optional[Union[str, int]]):
        The end of the output sequence.
        If set to None, the output sequence will be generated until the maximum number of tokens is reached.
      args (Optional[InferArgs]):
        Optionak inference parameters.
        
    Returns:
      Inference response
    """
    if not args:
      args = self.default_infer_args
    yield from self._infer(end, args)
    
  def inject(self, text: Union[str, int], add_special_tokens: bool = False) -> int:
    raise NotImplementedError("inject")

T_Logits = TypeVar('T_Logits')

class LLMGenerationSessionForRawText(LLMGenerationSession, Generic[T_LLM, T_LLMState, T_Logits]):
  """ Generation session for a language model that processes raw text. """
  
  _logits: Optional[T_Logits]
  _next_token: Optional[Tuple[int, str]]
  
  def _eval(self, tokid: int) -> T_Logits:
    raise NotImplementedError("_eval")
  
  def _next_token_probs(self):
    raise NotImplementedError("_next_token_probs")
  
  def flush_token(self):
    """
    Flushes the previous token into the language model if healing is enabled.
    
    **Warning:** unexpected behavior if the previous token is a "boundary" token
    like spaces.
    """
    if self._next_token is None:
      return
    self.inject(self._next_token[0])
    self._next_token = None
  
  def next_token_probs(self, *args, **kwargs) -> List[float]:
    assert self._next_token is None, "token healing must be disabled or flush_token() must be called"
    probs = self._next_token_probs(*args, **kwargs)
    return list(map(float, probs))
  
  def inject(self, text: Union[str, int], add_special_tokens: bool = False) -> int:
    if isinstance(text, str):
      input_ids = self.tokenize(text, add_special_tokens=add_special_tokens)
    else:
      input_ids = [text]
    if not input_ids:
      return 0
    
    num_toks = 0
      
    if self.token_healing:
      init_offset = 0
      if self._next_token is not None:
        tokid, tokstr = self._next_token
        healed_str = self.decode([tokid, input_ids[0]])
        healed_tokens = self.tokenize(healed_str, add_special_tokens=add_special_tokens)
        
        if len(input_ids) == 1:
          if len(healed_tokens) == 1:
            self._next_token = (healed_tokens[0], healed_str)
            return 1
          else:
            # handle rare case where 1 input token maps to 2 or more "healed" tokens
            for tokid in healed_tokens[:-1]:
              self._logits = self._eval(tokid)
            self._next_token = (healed_tokens[-1], self.decode(healed_tokens[-1:]))
            return len(healed_tokens) - 1
        else:
          for tokid in healed_tokens:
            self._logits = self._eval(tokid)
          init_offset = 1
        
      for tokid in input_ids[init_offset:-1]:
        self._logits = self._eval(tokid)
      num_toks += len(input_ids) - init_offset - 1
      self._next_token = (input_ids[-1], self.decode(input_ids[-1:]))
    else:
      if self._next_token is not None:
        tokid, tokstr = self._next_token
        self._eval(tokid)
        num_toks += 1
      for tokid in input_ids:
        self._logits = self._eval(tokid)
      num_toks += len(input_ids)

    return num_toks

T_Embedding = TypeVar('T_Embedding')

class LLMEmbeddingSession(LLMSession, Generic[T_LLM, T_Embedding]):
  """ Session for a language model that outputs an embedding for raw text. """
  
  def __init__(self,
               llm: T_LLM,
               ld: "Langdash"):
    self._ld = ld
    self.llm = llm
    
  def embedding_size(self) -> int:
    """
    Returns the embedding size of the model.
    """
    raise NotImplementedError("embedding_size")
    
  def infer(self, text: str) -> T_Embedding:
    """
    Infer the embedding of a text.
    
    Args:
      text (str): The text to be embedded.
      
    Returns:
      The embedding vector of the text.
    """
    raise NotImplementedError("infer")
