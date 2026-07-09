---
name: dspy
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging dspy. Use this skill whenever modifying dspy configurations or adding related functionality.
---
# dspy

## File Tree

```text
dspy/
├── assets
├── modules
│   └── dspy (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/dspy`

```python
docs/docs/js/tutorial-nav.js:
⋮
│  function collapseTutorialNav() {
│    // Find the navigation sidebar
│    const navSidebar = document.querySelector('.md-sidebar--primary');
│    if (!navSidebar) return;
│
│    // Find the 'Tutorials' section in the navigation
│    const tutorialsSection = Array.from(
│      navSidebar.querySelectorAll('.md-nav__item')
│    ).find((item) => {
│      const linkSpan = item.querySelector('.md-nav__link .md-ellipsis');
⋮

dspy/__init__.py:
⋮
│configure = settings.configure
⋮

dspy/adapters/base.py:
⋮
│class Adapter:
│    """Base Adapter class.
│
│    The Adapter serves as the interface layer between DSPy module/signature and Language Models (LM
│    complete transformation pipeline from DSPy inputs to LM calls and back to structured outputs.
│
│    Key responsibilities:
│        - Transform user inputs and signatures into properly formatted LM prompts, which also instr
│            the response in a specific format.
│        - Parse LM outputs into dictionaries matching the signature's output fields.
│        - Enable/disable native LM features (function calling, citations, etc.) based on configurat
⋮
│    def parse(self, signature: type[Signature], completion: str) -> dict[str, Any]:
⋮

dspy/adapters/chat_adapter.py:
⋮
│class FieldInfoWithName(NamedTuple):
⋮
│class ChatAdapter(Adapter):
│    """Default Adapter for most language models.
│
│    The ChatAdapter formats DSPy signatures into a format compatible with most language models.
│    It uses delimiter patterns like `[[ ## field_name ## ]]` to clearly separate input and output f
│    the message content.
│
│    Key features:
│        - Structures inputs and outputs using field header markers for clear field delineation.
│        - Provides automatic fallback to JSONAdapter if the chat format fails.
⋮
│    def format_field_structure(self, signature: type[Signature]) -> str:
│        """
│        `ChatAdapter` requires input and output fields to be in their own sections, with section he
│        `[[ ## field_name ## ]]`. An arbitrary field `completed` ([[ ## completed ## ]]) is added t
│        output fields section to indicate the end of the output fields.
⋮
│        def format_signature_fields_for_instructions(fields: dict[str, FieldInfo]):
⋮
│    def user_message_output_requirements(self, signature: type[Signature]) -> str:
⋮
│    def parse(self, signature: type[Signature], completion: str) -> dict[str, Any]:
⋮
│    def format_field_with_value(self, fields_with_values: dict[FieldInfoWithName, Any]) -> str:
⋮

dspy/adapters/json_adapter.py:
⋮
│class JSONAdapter(ChatAdapter):
│    def __init__(
│        self,
│        callbacks: list[BaseCallback] | None = None,
│        use_native_function_calling: bool = True,
│        parallel_tool_calls: bool | None = None,
⋮
│    def format_field_structure(self, signature: type[Signature]) -> str:
│        parts = []
⋮
│        def format_signature_fields_for_instructions(fields: dict[str, FieldInfo], role: str):
⋮
│    def user_message_output_requirements(self, signature: type[Signature]) -> str:
⋮
│    def parse(self, signature: type[Signature], completion: str) -> dict[str, Any]:
⋮
│    def format_field_with_value(self, fields_with_values: dict[FieldInfoWithName, Any], role: str =
⋮

dspy/adapters/two_step_adapter.py:
⋮
│class TwoStepAdapter(Adapter):
│    """
│    A two-stage adapter that:
│        1. Uses a simpler, more natural prompt for the main LM
│        2. Uses a smaller LM with chat adapter to extract structured data from the response of main
│    This adapter uses a common __call__ logic defined in base Adapter class.
│    This class is particularly useful when interacting with reasoning models as the main LM since r
│    are known to struggle with structured outputs.
│
│    Examples:
│    ```
⋮
│    def parse(self, signature: Signature, completion: str) -> dict[str, Any]:
⋮

dspy/adapters/types/base_type.py:
⋮
│class Type(pydantic.BaseModel):
│    """Base class to support creating custom types for DSPy signatures.
│
│    This is the parent class of DSPy custom types, e.g, dspy.Image. Subclasses must implement the `
│    return a list of dictionaries (same as the Array of content parts in the OpenAI API user messag
│
│    Examples:
│
│        ```python
│        class Image(Type):
│            url: str
│
⋮
│    @classmethod
│    def extract_custom_type_from_annotation(cls, annotation):
⋮

dspy/adapters/types/citation.py:
⋮
│@experimental(version="3.0.4")
│class Citations(Type):
│    """Citations extracted from an LM response with source references.
│
│    This type represents citations returned by language models that support
│    citation extraction, particularly Anthropic's Citations API through LiteLLM.
│    Citations include the quoted text and source information.
│
│    Examples:
│        ```python
│        import os
│        import dspy
⋮
│    class Citation(Type):
⋮
│    @classmethod
│    def from_dict_list(cls, citations_dicts: list[dict[str, Any]]) -> "Citations":
⋮

dspy/adapters/types/reasoning.py:
⋮
│class Reasoning(Type):
⋮

dspy/adapters/types/tool.py:
⋮
│class ToolCalls(Type):
│    class ToolCall(Type):
│        id: str | None = None
│        name: str
│        args: dict[str, Any]
│
│        @classmethod
│        def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any) -> dict[str, Any]:
│            schema = super().__get_pydantic_json_schema__(core_schema, handler)
│            schema = handler.resolve_ref_schema(schema)
│            properties = schema.get("properties")
⋮
│    @classmethod
│    def from_dict_list(cls, tool_calls_dicts: list[dict[str, Any]]) -> "ToolCalls":
⋮
│def _resolve_json_schema_reference(schema: dict) -> dict:
│    """Recursively resolve json model schema, expanding all references."""
│
⋮
│    def resolve_refs(obj: Any) -> Any:
⋮
│def convert_input_schema_to_tool_args(
│    schema: dict[str, Any],
⋮

dspy/adapters/utils.py:
⋮
│def serialize_for_json(value: Any) -> Any:
⋮
│def format_field_value(field_info: FieldInfo, value: Any, assume_text=True) -> str | dict:
⋮
│def _get_json_schema(field_type):
│    def move_type_to_front(d):
│        # Move the 'type' key to the front of the dictionary, recursively, for LLM readability/adhe
│        if isinstance(d, Mapping):
│            return {
│                k: move_type_to_front(v) for k, v in sorted(d.items(), key=lambda item: (item[0] !=
│            }
│        elif isinstance(d, list):
│            return [move_type_to_front(item) for item in d]
⋮
│def translate_field_type(field_name, field_info):
⋮
│def find_enum_member(enum, identifier):
⋮
│def parse_value(value, annotation):
⋮
│def get_annotation_name(annotation):
⋮
│def get_field_description_string(fields: dict) -> str:
⋮

dspy/adapters/xml_adapter.py:
⋮
│class XMLAdapter(ChatAdapter):
│    field_pattern = re.compile(r"<(?P<name>\w+)>((?P<content>.*?))</\1>", re.DOTALL)
│
│    def format_field_with_value(self, fields_with_values: dict[FieldInfoWithName, Any]) -> str:
⋮
│    def format_field_structure(self, signature: type[Signature]) -> str:
│        """
│        XMLAdapter requires input and output fields to be wrapped in XML tags like `<field_name>`.
⋮
│        def format_signature_fields_for_instructions(fields: dict[str, FieldInfo]):
⋮
│    def user_message_output_requirements(self, signature: type[Signature]) -> str:
⋮
│    def parse(self, signature: type[Signature], completion: str) -> dict[str, Any]:
⋮

dspy/clients/_litellm.py:
⋮
│@functools.cache
│def get_litellm(*, feature: str) -> Any:
⋮

dspy/clients/base_lm.py:
⋮
│class BaseLM:
│    """Base class for DSPy language models.
│
│    Most users should use `dspy.LM`, which is a `BaseLM` subclass.
│
│    For advanced use cases, such as custom language model backends, users can
│    subclass `BaseLM` and implement `forward()`.
│
│    DSPy is migrating `forward()` from the legacy OpenAI/LiteLLM-shaped
│    contract to a typed DSPy contract. During this migration, subclasses should
│    declare which contract they implement with `forward_contract`:
│
⋮
│    def copy(self, **kwargs):
⋮

dspy/clients/cache.py:
⋮
│class Cache:
│    """DSPy Cache
│
│    `Cache` provides 2 levels of caching (in the given order):
│        1. In-memory cache - implemented with cachetools.LRUCache
│        2. On-disk cache - implemented with diskcache.FanoutCache
⋮
│    def cache_key(self, request: dict[str, Any], ignored_args_for_cache_key: list[str] | None = Non
⋮
│    def get(self, request: dict[str, Any], ignored_args_for_cache_key: list[str] | None = None) -> 
⋮
│def request_cache(
│    cache_arg_name: str | None = None,
│    ignored_args_for_cache_key: list[str] | None = None,
│    enable_memory_cache: bool = True,
│    *,  # everything after this is keyword-only
│    maxsize: int | None = None,  # legacy / no-op
│):
│    """
│    Decorator for applying caching to a function based on the request argument.
│
│    Args:
│        cache_arg_name: The name of the argument that contains the request. If not provided, the en
│            as the request.
│        ignored_args_for_cache_key: A list of arguments to ignore when computing the cache key from
│        enable_memory_cache: Whether to enable in-memory cache at call time. If False, the memory c
│            written to on new data.
⋮
│    def decorator(fn):
│        @wraps(fn)
│        def process_request(args, kwargs):
│            # Use fully qualified function name for uniqueness
│            fn_identifier = f"{fn.__module__}.{fn.__qualname__}"
│
│            # Create a modified request that includes the function identifier so that it's incorpor
│            # key. Deep copy is required because litellm sometimes modifies the kwargs in place.
│            if cache_arg_name:
│                # When `cache_arg_name` is provided, use the value of the argument with this name a
│                # caching.
⋮

dspy/clients/disk_serialization.py:
⋮
│class DeserializationError(Exception):
⋮
│class _RestrictedUnpickler(pickle.Unpickler):
│    _allowed: frozenset[tuple[str, str]] = frozenset()
│
│    def find_class(self, module: str, name: str) -> type:
⋮
│def restricted_disk(allowed: frozenset[tuple[str, str]]) -> type[_RestrictedDisk]:
⋮

dspy/clients/embedding.py:
⋮
│class Embedder:
⋮

dspy/clients/openai_format.py:
⋮
│def parts_to_openai_content(parts: list[Any]) -> str | list[dict[str, Any]]:
⋮
│def provider_tool_call_to_part(tool_call: Any) -> LMToolCallPart:
⋮
│def citation_to_part(citation: Any) -> LMCitationPart:
⋮
│def usage_from_response(response: Any) -> LMUsage | None:
⋮
│def data_uri(media_type: str, data: str) -> str:
⋮
│def split_data_uri(value: str) -> tuple[str, str]:
⋮
│def get_value(value: Any, key: str, default: Any = None) -> Any:
⋮
│def model_dump(value: Any) -> dict[str, Any]:
⋮

dspy/clients/utils_finetune.py:
⋮
│def get_finetune_directory() -> str:
⋮

dspy/core/types.py:
⋮
│class LMTextPart(LMBasePart):
⋮
│class LMImagePart(LMSourcePart):
⋮
│class LMAudioPart(LMSourcePart):
⋮
│class LMVideoPart(LMSourcePart):
⋮
│class LMDocumentPart(LMBasePart):
⋮
│class LMBinaryPart(LMSourcePart):
⋮
│class LMToolCallPart(LMBasePart):
⋮
│class LMToolResultPart(LMBasePart):
⋮
│class LMThinkingPart(LMBasePart):
⋮
│class LMMessage(BaseModel):
⋮
│class LMToolSpec(BaseModel):
⋮
│class LMReasoningConfig(BaseModel):
│    """Reasoning controls for models with native reasoning support."""
│
⋮
│    @classmethod
│    def from_value(cls, value: Any = None, **overrides: Any) -> LMReasoningConfig:
⋮
│class LMToolChoice(BaseModel):
│    """Tool-choice controls for native tool-capable models."""
│
⋮
│    @classmethod
│    def from_value(cls, value: Any = None, **overrides: Any) -> LMToolChoice:
⋮
│class LMCacheConfig(BaseModel):
│    """DSPy memoization cache controls for a normalized LM request.
│
│    This cache skips the provider call entirely when DSPy finds an exact
│    request match. Use `LMPromptCacheConfig` for provider-side prompt/token
│    caching that still sends the request to the provider.
⋮
│    @classmethod
│    def from_value(cls, value: Any = None, **overrides: Any) -> LMCacheConfig:
⋮
│class LMPromptCacheConfig(BaseModel):
│    """Provider-side prompt/token cache controls.
│
│    Prompt caching is not DSPy memoization. The provider call still happens,
│    but the backend may reuse cached prompt prefixes or KV state for lower
│    latency or lower input-token cost.
⋮
│    @classmethod
│    def from_value(cls, value: Any = None, **overrides: Any) -> LMPromptCacheConfig:
⋮
│class LMConfig(BaseModel):
│    """Common generation controls for an LM request."""
│
⋮
│    @classmethod
│    def from_kwargs(cls, **kwargs: Any) -> LMConfig:
⋮
│@dataclass
│class LMRequestPatch:
⋮
│class LMRequest(BaseModel):
│    """A normalized request passed to a `LanguageModel`."""
│
⋮
│    @classmethod
│    def from_call(
│        cls,
│        *,
│        model: str,
│        items: tuple[Any, ...] = (),
│        prompt: str | None = None,
│        messages: list[dict[str, Any] | LMMessage] | None = None,
│        tools: list[Any] | None = None,
│        **kwargs: Any,
⋮
│class LMOutput(BaseModel):
│    """One generated candidate in an LM response."""
│
⋮
│    def to_value(self) -> Any:
⋮
│    def to_output_dict(self) -> dict[str, Any]:
⋮
│class LMResponse(BaseModel):
│    """The normalized result of one LM request."""
│
⋮
│    def to_values(self) -> list[Any]:
⋮
│    def to_outputs(self) -> list[Any]:
⋮
│    def usage_as_dict(self) -> dict[str, Any]:
⋮
│class LMOutputBuilder:
│    """Assemble streamed LM events into a final `LMResponse`."""
│
⋮
│    def to_response(self, *, usage: LMUsage | dict[str, Any] | None = None, cost: float | None = No
⋮
│ToolCall = LMToolCallPart
⋮

dspy/dsp/utils/dpr.py:
⋮
│def DPR_normalize(text):  # noqa: N802
⋮

dspy/dsp/utils/settings.py:
⋮
│class Settings:
│    """
│    A singleton class for DSPy configuration settings.
│    Thread-safe global configuration.
│    - 'configure' can be called by only one 'owner' thread (the first thread that calls it).
│    - Other threads see the configured global values from 'main_thread_config'.
│    - 'context' sets thread-local overrides. These overrides propagate to threads spawned
│      inside that context block, when (and only when!) using a ParallelExecutor that copies overrid
│
│      1. Only one unique thread (which can be any thread!) can call dspy.configure.
│      2. It affects a global state, visible to all. As a result, user threads work, but they should
⋮
│    def __setattr__(self, name, value):
⋮
│    def get(self, key, default=None):
⋮
│    def copy(self):
⋮
│    def configure(self, **kwargs):
⋮
│    @classmethod
│    def load(cls, path: str, allow_pickle: bool = False) -> dict[str, Any]:
⋮

dspy/dsp/utils/utils.py:
⋮
│def print_message(*s, condition=True, pad=False, sep=None):
⋮
│class dotdict(dict):  # noqa: N801
│    def __getattr__(self, key):
│        if key.startswith("__") and key.endswith("__"):
│            return super().__getattr__(key)
│        try:
│            return self[key]
│        except KeyError:
⋮
│    def __setattr__(self, key, value):
⋮

dspy/evaluate/evaluate.py:
⋮
│class Evaluate:
⋮

dspy/evaluate/metrics.py:
⋮
│def normalize_text(s):
⋮

dspy/predict/avatar/models.py:
⋮
│class Action(BaseModel):
⋮

dspy/predict/chain_of_thought.py:
⋮
│class ChainOfThought(Module):
⋮

dspy/predict/parallel.py:
⋮
│class Parallel:
⋮

dspy/predict/parameter.py:
│class Parameter:
⋮

dspy/primitives/base_module.py:
⋮
│class BaseModule:
│    def __init__(self):
⋮
│    def named_parameters(self):
│        """
│        Unlike PyTorch, handles (non-recursive) lists of parameters too.
⋮
│        def add_parameter(param_name, param_value):
⋮
│    def named_sub_modules(self, type_=None, skip_compiled=False) -> Generator[tuple[str, "BaseModul
│        """Find all sub-modules in the module, as well as their names.
│
│        Say `self.children[4]['key'].sub_module` is a sub-module. Then the name will be
│        `children[4]['key'].sub_module`. But if the sub-module is accessible at different
│        paths, only one of the paths will be returned.
⋮
│        def add_to_queue(name, item):
⋮
│    def deepcopy(self):
⋮
│    def reset_copy(self):
⋮
│    def load(self, path, allow_pickle=False, allow_unsafe_lm_state=False):
⋮

dspy/primitives/code_interpreter.py:
⋮
│SIMPLE_TYPES = (str, int, float, bool, list, dict, type(None))
│
⋮
│class CodeInterpreterError(RuntimeError):
⋮
│@runtime_checkable
│class CodeInterpreter(Protocol):
│    """Protocol for code execution environments (interpreters).
│
│    Implementations must provide:
│    - start(): Initialize the interpreter (optional, can be lazy)
│    - execute(): Run code and return results
│    - shutdown(): Clean up resources
│
│    The interpreter maintains state across execute() calls within a session,
│    allowing variables defined in one call to be used in subsequent calls.
│
⋮
│    @property
│    def tools(self) -> dict[str, Callable[..., str]]:
⋮

dspy/primitives/example.py:
⋮
│class Example:
│    """A flexible data container for DSPy examples and training data with named fields.
│
│    An `Example` is roughly one row from a HuggingFace dataset or pandas
│    `DataFrame`. It behaves a lot like a dictionary or dot-access record: you
│    can read fields with `example["question"]` or `example.question`.
│
│    In DSPy, lists of `Example` objects are your trainset, devset, and testset.
│    Most examples are built from keyword arguments or an existing record, then
│    tagged with `with_inputs(...)` to say which fields should be fed into a
│    module. The remaining fields are labels or metadata.
│
⋮
│    def __setattr__(self, key, value):
⋮
│    def keys(self, include_dspy=False):
⋮
│    def values(self, include_dspy=False):
⋮
│    def items(self, include_dspy=False):
⋮
│    def get(self, key, default=None):
⋮
│    def with_inputs(self, *keys):
⋮
│    def inputs(self):
⋮
│    def copy(self, **kwargs):
⋮
│    def toDict(self):  # noqa: N802
│        """Convert to a plain dictionary, recursively serializing nested objects.
│
│        Nested `Example` objects, Pydantic models, lists, and dicts are
│        converted so the result is JSON-friendly.
│
│        Examples:
│            >>> import dspy
│            >>> dspy.Example(question="Why?", answer="Because.").toDict()
│            {'question': 'Why?', 'answer': 'Because.'}
│        """
│        def convert_to_serializable(value):
⋮

dspy/primitives/module.py:
⋮
│class Module(BaseModule, metaclass=ProgramMeta):
│    """Base class for all DSPy modules (programs).
│
│    A Module is a building block for DSPy programs that can contain predictors,
│    sub-modules, and custom logic. Modules can be composed together to create
│    complex pipelines and can be optimized using DSPy's teleprompters.
│
│    All DSPy programs should inherit from this class and implement a ``forward``
│    method that defines the program's logic.
│
│    Args:
⋮
│    def named_predictors(self):
⋮

dspy/primitives/prediction.py:
⋮
│class Prediction(Example):
│    """A prediction object that contains the output of a DSPy module.
│    
│    Prediction inherits from Example.
│    
│    To allow feedback-augmented scores, Prediction supports comparison operations
│    (<, >, <=, >=) for Predictions with a `score` field. The comparison operations
│    compare the 'score' values as floats. For equality comparison, Predictions are equal
│    if their underlying data stores are equal (inherited from Example).
│    
│    Arithmetic operations (+, /, etc.) are also supported for Predictions with a 'score'
⋮
│    def __float__(self):
⋮
│class Completions:
│    def __init__(self, list_or_dict, signature=None):
│        self.signature = signature
│
│        if isinstance(list_or_dict, list):
│            kwargs = {}
│            for arg in list_or_dict:
│                for k, v in arg.items():
│                    kwargs.setdefault(k, []).append(v)
│        else:
│            kwargs = list_or_dict
│
⋮
│    def items(self):
⋮

dspy/primitives/python_interpreter.py:
⋮
│class PythonInterpreter:
⋮

dspy/primitives/repl_types.py:
⋮
│class REPLVariable(pydantic.BaseModel):
│    """Metadata about a variable available in the REPL environment."""
│
⋮
│    @classmethod
│    def from_value(
│        cls,
│        name: str,
│        value: Any,
│        field_info: FieldInfo | None = None,
│        preview_chars: int = 1000,
⋮
│class REPLEntry(pydantic.BaseModel):
│    """A single REPL interaction entry containing reasoning, code, and output."""
│
⋮
│    @staticmethod
│    def format_output(output: str, max_output_chars: int = 10_000) -> str:
⋮
│class REPLHistory(pydantic.BaseModel):
│    """Container for REPL interaction history.
│
│    Immutable: append() returns a new instance with the entry added.
⋮
│    def append(self, *, reasoning: str = "", code: str, output: str) -> REPLHistory:
⋮

dspy/propose/grounded_proposer.py:
⋮
│class GroundedProposer(Proposer):
│    def __init__(
│        self,
│        prompt_model,
│        program,
│        trainset,
│        view_data_batch_size=10,
│        use_dataset_summary=True,
│        program_aware=True,
│        use_task_demos=True,
│        num_demos_in_context = 3,
⋮
│    def propose_instructions_for_program(
│        self,
│        trainset,
│        program,
│        demo_candidates,
│        trial_logs,
│        N, # noqa: N803
⋮
│    def propose_instruction_for_predictor(
│        self,
│        program,
│        predictor,
│        pred_i,
│        demo_candidates,
│        demo_set_i,
│        trial_logs,
│        tip=None,
⋮

dspy/propose/propose_base.py:
⋮
│class Proposer(ABC):
│    def __init__(self):
⋮
│    @abstractmethod
│    def propose_instructions_for_program(self):
⋮
│    def propose_instruction_for_predictor(self):
⋮

dspy/retrievers/databricks_rm.py:
⋮
│@dataclass
│class Document:
⋮

dspy/retrievers/embeddings.py:
⋮
│class Embeddings:
│    """DSPy Embeddings retriever.
│
│    This class retrieves the top-k most similar passages from a corpus using embedding-based simila
│    For large corpora, a FAISS index is built for fast approximate candidate retrieval, followed by
│    re-ranking. For small corpora, brute-force search is used.
⋮
│    def load(self, path: str, embedder):
⋮

dspy/signatures/field.py:
⋮
│def move_kwargs(**kwargs):
⋮
│def _warn_deprecated_field_args(**kwargs):
⋮
│def InputField(**kwargs): # noqa: N802
⋮
│def OutputField(**kwargs): # noqa: N802
⋮

dspy/signatures/signature.py:
⋮
│class Signature(BaseModel, metaclass=SignatureMeta):
│    """"""
│
⋮
│    @classmethod
│    def append(cls, name, field, type_=None) -> type["Signature"]:
⋮
│def ensure_signature(signature: str | type[Signature], instructions=None) -> None | type[Signature]
⋮
│def make_signature(
│    signature: str | dict[str, tuple[type, FieldInfo]],
│    instructions: str | None = None,
│    signature_name: str = "StringSignature",
│    custom_types: dict[str, type] | None = None,
⋮
│def _parse_type_node(node, names=None) -> Any:
│    """Recursively parse an AST node representing a type annotation.
│
│    This function converts Python's Abstract Syntax Tree (AST) nodes into actual Python types.
│    It's used to parse type annotations in signature strings like "x: list[int] -> y: str".
│
│    Examples:
│        - For "x: int", the AST node represents 'int' and returns the int type
│        - For "x: list[str]", it processes a subscript node to return typing.list[str]
│        - For "x: Optional[int]", it handles the Union type to return Optional[int]
│        - For "x: MyModule.CustomType", it processes attribute access to return the actual type
│
⋮
│    def resolve_name(type_name: str):
⋮
│def infer_prefix(attribute_name: str) -> str:
⋮

dspy/signatures/utils.py:
⋮
│def get_dspy_field_type(field: FieldInfo) -> Literal["input", "output"]:
⋮

dspy/streaming/streaming_listener.py:
⋮
│class StreamListener:
│    """Class that listens to the stream to capture the streeaming of a specific output field of a p
│
⋮
│    def flush(self) -> str:
⋮

dspy/teleprompt/bootstrap.py:
⋮
│class BootstrapFewShot(Teleprompter):
⋮

dspy/teleprompt/ensemble.py:
⋮
│class Ensemble(Teleprompter):
│    def __init__(self, *, reduce_fn=None, size=None, deterministic=False):
│        """A common reduce_fn is dspy.majority."""
│
│        assert deterministic is False, "TODO: Implement example hashing for deterministic ensemble.
│
│        self.reduce_fn = reduce_fn
│        self.size = size
⋮
│    def compile(self, programs):
│        size = self.size
⋮
│        class EnsembledProgram(dspy.Module):
⋮

dspy/teleprompt/utils.py:
⋮
│def get_signature(predictor):
⋮

dspy/utils/annotation.py:
⋮
│@overload
│def experimental(f: Callable[P, R], version: str | None = None) -> Callable[P, R]: ...
│
│@overload
│def experimental(f: None = None, version: str | None = None) -> Callable[[Callable[P, R]], Callable
│
⋮
│def experimental(
│    f: Callable[P, R] | None = None,
│    version: str | None = None,
⋮
│def _experimental(api: Callable[P, R], version: str | None = None) -> Callable[P, R]:
⋮
│def _get_min_indent_of_docstring(docstring_str: str) -> str:
⋮

dspy/utils/constants.py:
⋮
│IS_TYPE_UNDEFINED = "IS_TYPE_UNDEFINED"

dspy/utils/exceptions.py:
⋮
│class AdapterParseError(DSPyError):
⋮

dspy/utils/hasher.py:
⋮
│class Hasher:
│    """Hasher that accepts python objects as inputs."""
│
⋮
│    @classmethod
│    def hash_bytes(cls, value: bytes | list[bytes]) -> str:
⋮
│    @classmethod
│    def hash(cls, value: Any) -> str:
⋮
│    def update(self, value: Any) -> None:
⋮
│    def hexdigest(self) -> str:
⋮

dspy/utils/inspect_history.py:
⋮
│def pretty_print_history(history: list[dict[str, Any]], n: int = 1, file: TextIO | None = None) -> 
│    """Print the last n prompts and their completions.
│
│    Args:
│        history: The history list to print from.
│        n: Number of recent entries to display. Defaults to 1.
│        file: An optional file-like object to write output to (must have a
│            `.write()` method). When provided, ANSI color codes are
│            automatically disabled. Defaults to `None` (prints to stdout).
⋮
│    def print_tool_calls(tool_calls):
⋮

dspy/utils/langchain_tool.py:
⋮
│def convert_langchain_tool(tool: "BaseTool") -> Tool:
⋮

dspy/utils/lazy_import.py:
⋮
│class _LazyModule(types.ModuleType):
│    """Module proxy that imports the real module on first attribute access.
│
│    Attribute assignment also materializes the real module so configuration writes apply to the rea
⋮
│    def __setattr__(self, attr: str, value: Any) -> None:
⋮
│def require(module: str, *, extra: str | None = None, feature: str | None = None) -> Any:
⋮

dspy/utils/logging_utils.py:
⋮
│class DSPyLoggingStream:
│    """
│    A Python stream for use with event logging APIs throughout DSPy (`eprint()`,
│    `logger.info()`, etc.). This stream wraps `sys.stderr`, forwarding `write()` and
│    `flush()` calls to the stream referred to by `sys.stderr` at the time of the call.
│    It also provides capabilities for disabling the stream to silence event logs.
⋮
│    def write(self, text):
⋮
│    def flush(self):
⋮
│def configure_dspy_loggers(root_module_name):
⋮

dspy/utils/magicattr.py:
⋮
│def get(obj, attr, **kwargs):
⋮
│def set(obj, attr, val):
⋮
│def lookup(obj, attr):
⋮
│def _lookup_subscript_value(node):
⋮

dspy/utils/mcp.py:
⋮
│def convert_mcp_tool(session: "mcp.ClientSession", tool: "mcp.types.Tool") -> Tool:
⋮

dspy/utils/parallelizer.py:
⋮
│class ParallelExecutor:
⋮

dspy/utils/saving.py:
⋮
│def get_dependency_versions():
⋮
│def load(path: str, allow_pickle: bool = False) -> "Module":
⋮

dspy/utils/syncify.py:
⋮
│def run_async(coro):
⋮
│def syncify(program: "Module", in_place: bool = True) -> "Module":
│    """Convert an async DSPy module to a sync program.
│
│    There are two modes of this function:
│
│    - `in_place=True` (recommended): Modify the module in place. But this may not work if you alrea
│        method which does different things from `aforward`.
│    - `in_place=False`: Return a wrapper module. This changes the module's architecture, but it's m
│
│    Args:
│        program: The async program to convert, must have an `aforward` method implemented.
⋮
│    if in_place:
│
⋮
│    else:
│        from dspy.primitives.module import Module
│
│        class SyncWrapper(Module):
⋮

dspy/utils/unbatchify.py:
⋮
│class Unbatchify:
⋮

dspy/utils/usage_tracker.py:
⋮
│class UsageTracker:
⋮

tests/adapters/test_xml_adapter.py:
⋮
│def test_xml_adapter_with_tool_like_output():
│    # XMLAdapter does not natively support tool calls, but we can test structured output
│    class ToolCall(pydantic.BaseModel):
│        name: str
│        args: dict
⋮

tests/clients/test_lazy_litellm_import.py:
⋮
│def _hide_litellm(monkeypatch):
│    real_find_spec = importlib.util.find_spec
│
│    def find_spec(name, *args, **kwargs):
⋮

tests/metadata/test_metadata.py:
⋮
│def test_metadata():
⋮

tests/predict/test_best_of_n.py:
⋮
│class DummyModule(dspy.Module):
⋮

tests/predict/test_react_v2.py:
⋮
│def test_react_v2_text_mock_lm_loop_records_inputs_once():
│    def lookup(query: str) -> str:
⋮
│def test_react_v2_continuation_omits_missing_original_inputs():
│    def lookup(query: str) -> str:
⋮
│def test_react_v2_text_mode_accepts_top_level_tool_arguments():
│    def lookup(query: str) -> str:
⋮
│def test_react_v2_native_tool_loop_replays_tool_result_with_provider_id():
│    def lookup(query: str) -> str:
⋮
│def test_react_v2_native_parallel_tool_calls_are_requested_and_replayed():
│    def lookup(query: str) -> str:
⋮

tests/predict/test_refine.py:
⋮
│class DummyModule(dspy.Module):
⋮

tests/predict/test_rlm.py:
⋮
│@pytest.mark.deno
│class TestRLMWithDummyLM:
│    """End-to-end tests using DummyLM with RLM and PythonInterpreter.
│
│    Note: These tests let RLM create its own PythonInterpreter so it can register
│    typed output_fields for SUBMIT based on the signature.
⋮
│    def test_with_tool_e2e(self):
│        """Test RLM calling a host-side tool through the sandbox."""
│        def lookup(key: str) -> str:
⋮

tests/propose/test_grounded_proposer.py:
⋮
│@pytest.mark.parametrize(
│    "demo_candidates",
│    [
│        None,
│        [[[dspy.Example(question="What is the capital of France?", answer="Paris")]]],
│    ],
│)
│def test_propose_instruction_for_predictor(demo_candidates):
│    class TrackingDummyLM(DummyLM):
│        def copy(self, **kwargs):
│            self.last_copy_kwargs = kwargs
⋮

tests/teleprompt/test_gepa.py:
⋮
│@pytest.mark.parametrize("reflection_minibatch_size, batch, expected_callback_metadata", [
│    (None, [], {"metric_key": "eval_full"}),
│    (None, [Example(input="What is the color of the sky?", output="blue")], {"metric_key": "eval_fu
│    (1, [], {"disable_logging": True}),
│    (1, [
│        Example(input="What is the color of the sky?", output="blue"),
│        Example(input="What does the fox say?", output="Ring-ding-ding-ding-dingeringeding!"),
│    ], {"metric_key": "eval_full"}),
│])
│def test_gepa_adapter_disables_logging_on_minibatch_eval(monkeypatch, reflection_minibatch_size, ba
│    from dspy.teleprompt import bootstrap_trace as bootstrap_trace_module
⋮
│    class DummyModule(dspy.Module):
⋮

tests/teleprompt/test_knn_fewshot.py:
⋮
│def mock_example(question: str, answer: str) -> dspy.Example:
⋮
│class SimpleModule(dspy.Module):
│    def __init__(self, signature):
│        super().__init__()
⋮
│    def reset_copy(self):
⋮
```