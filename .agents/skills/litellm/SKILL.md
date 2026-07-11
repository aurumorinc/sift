---
name: litellm
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging litellm. Use this skill whenever modifying litellm configurations or adding related functionality.
---
# litellm

## File Tree

```text
litellm/
├── assets
├── modules
│   ├── litellm (See AST Map below)
│   └── litellm-docs (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/litellm`

```python
litellm-proxy-extras/litellm_proxy_extras/utils.py:
⋮
│def str_to_bool(value: Optional[str]) -> bool:
⋮

litellm-rust/crates/ai-gateway/src/auth/mod.rs:
⋮
│/// `LiteLLM_SpendLogs.api_key`, so realtime spend joins with the rest of LiteLLM.
│pub fn hash_token(token: &str) -> String {
│    let digest = Sha256::digest(token.as_bytes());
│    let mut hex = String::with_capacity(digest.len() * 2);
│    for byte in digest {
│        use std::fmt::Write;
│        let _ = write!(hex, "{byte:02x}");
│    }
│    hex
⋮

litellm-rust/crates/core/src/router/deployment.rs:
⋮
│mod tests {
│    use super::*;
│
│    #[test]
│    fn deserializes_from_model_list_entry() {
│        let entry = r#"{
│            "model_name": "gpt-realtime",
│            "litellm_params": {"model": "openai/gpt-realtime", "api_base": "https://x"}
│        }"#;
│        let deployment: Deployment = serde_json::from_str(entry).expect("valid entry");
│        assert_eq!(deployment.model_name, "gpt-realtime");
│        assert_eq!(deployment.litellm_params.model, "openai/gpt-realtime");
│        assert_eq!(deployment.litellm_params.api_key, None);
│        assert_eq!(
⋮

litellm/_uuid.py:
⋮
│def uuid4():
⋮

litellm/caching/dual_cache.py:
⋮
│class DualCache(BaseCache):
⋮

litellm/integrations/focus/destinations/base.py:
⋮
│class FocusDestination(Protocol):
⋮

litellm/integrations/otel/model/config.py:
⋮
│class ExporterSpec(BaseModel):
⋮

litellm/integrations/otel/model/semconv.py:
⋮
│class Error:
⋮

litellm/litellm_core_utils/core_helpers.py:
⋮
│def map_finish_reason(finish_reason: str) -> OpenAIChatCompletionFinishReason:
⋮

litellm/litellm_core_utils/get_llm_provider_logic.py:
⋮
│def get_llm_provider(
│    model: str,
│    custom_llm_provider: Optional[str] = None,
│    api_base: Optional[str] = None,
│    api_key: Optional[str] = None,
│    litellm_params: Optional[GenericLiteLLMParams] = None,
⋮

litellm/litellm_core_utils/litellm_logging.py:
⋮
│class Logging(LiteLLMLoggingBaseClass):
│    global \
⋮
│    def post_call(self, original_response, input=None, api_key=None, additional_args={}):
⋮

litellm/litellm_core_utils/logging_callback_manager.py:
⋮
│class LoggingCallbackManager:
│    """
│    A centralized class that allows easy add / remove callbacks for litellm.
│
│    Goals of this class:
│    - Prevent adding duplicate callbacks / success_callback / failure_callback
│    - Keep a reasonable MAX_CALLBACKS limit (this ensures callbacks don't exponentially grow and co
⋮
│    def add_litellm_callback(self, callback: Union[CustomLogger, str, Callable]):
⋮

litellm/litellm_core_utils/safe_json_dumps.py:
⋮
│def safe_dumps(data: Any, max_depth: int = DEFAULT_MAX_RECURSE_DEPTH) -> str:
⋮

litellm/litellm_core_utils/sensitive_data_masker.py:
⋮
│class SensitiveDataMasker:
│    def __init__(
│        self,
│        sensitive_patterns: Optional[Set[str]] = None,
│        non_sensitive_overrides: Optional[Set[str]] = None,
│        visible_prefix: int = 4,
│        visible_suffix: int = 4,
│        mask_char: str = "*",
│        mask_short_values: bool = True,
⋮
│    def mask_dict(
│        self,
│        data: Dict[str, Any],
│        depth: int = 0,
│        max_depth: int = DEFAULT_MAX_RECURSE_DEPTH_SENSITIVE_DATA_MASKER,
│        excluded_keys: Optional[Set[str]] = None,
⋮

litellm/litellm_core_utils/url_utils.py:
⋮
│class SSRFError(ValueError):
⋮

litellm/llms/base_llm/chat/transformation.py:
⋮
│class BaseLLMException(Exception):
⋮

litellm/llms/black_forest_labs/common_utils.py:
⋮
│class BlackForestLabsError(BaseLLMException):
⋮

litellm/llms/custom_httpx/http_handler.py:
⋮
│def get_default_headers() -> dict:
⋮
│class AsyncHTTPHandler:
│    def __init__(
│        self,
│        timeout: Optional[Union[float, httpx.Timeout]] = None,
│        event_hooks: Optional[Mapping[str, List[Callable[..., Any]]]] = None,
│        concurrent_limit=None,  # Kept for backward compatibility, but ignored (no limits)
│        client_alias: Optional[str] = None,  # name for client in logs
│        ssl_verify: Optional[VerifyTypes] = None,
│        shared_session: Optional["ClientSession"] = None,
⋮
│    async def patch(
│        self,
│        url: str,
│        data: Optional[Union[dict, str, bytes]] = None,  # type: ignore
│        json: Optional[dict] = None,
│        params: Optional[dict] = None,
│        headers: Optional[dict] = None,
│        timeout: Optional[Union[float, httpx.Timeout]] = None,
│        stream: bool = False,
│        content: Any = None,
⋮
│class HTTPHandler:
│    def __init__(
│        self,
│        timeout: Optional[Union[float, httpx.Timeout]] = None,
│        concurrent_limit=None,  # Kept for backward compatibility, but ignored (no limits)
│        client: Optional[httpx.Client] = None,
│        ssl_verify: Optional[Union[bool, str]] = None,
│        disable_default_headers: Optional[
│            bool
│        ] = False,  # arize phoenix returns different API responses when user agent header in reque
⋮
│    def patch(
│        self,
│        url: str,
│        data: Optional[Union[dict, str, bytes]] = None,
│        json: Optional[Union[dict, str]] = None,
│        params: Optional[dict] = None,
│        headers: Optional[dict] = None,
│        stream: bool = False,
│        timeout: Optional[Union[float, httpx.Timeout]] = None,
│        content: Any = None,
⋮
│def get_async_httpx_client(
│    llm_provider: Union[LlmProviders, httpxSpecialProvider],
│    params: Optional[dict] = None,
│    shared_session: Optional["ClientSession"] = None,
⋮

litellm/llms/custom_httpx/httpx_handler.py:
⋮
│def get_default_headers() -> dict:
⋮
│class HTTPHandler:
⋮

litellm/models/mcp_server.py:
⋮
│class MCPEnvVarScope(str, enum.Enum):
⋮

litellm/models/team.py:
⋮
│class Member(MemberBase):
⋮

litellm/proxy/_experimental/mcp_server/outbound_credentials/oauth_token_store.py:
⋮
│@dataclass(frozen=True, slots=True, repr=False)
│class OAuthToken:
⋮

litellm/proxy/_experimental/mcp_server/outbound_credentials/result.py:
⋮
│@dataclass(frozen=True)
│class Ok(Generic[_TOk_co, _TError_co]):
│    ok: _TOk_co
│
⋮
│    def is_error(self) -> Literal[False]:
⋮
│@dataclass(frozen=True)
│class Error(Generic[_TOk_co, _TError_co]):
│    error: _TError_co
│
⋮
│    def is_error(self) -> Literal[True]:
⋮

litellm/proxy/_experimental/out/_next/static/chunks/00q4mtjboprhm.js:
⋮
│            color: hsl(${Math.max(0,Math.min(120-120*n,120))}deg 100% 31%);`,null==l?void 0:l.key)}

litellm/proxy/_experimental/out/_next/static/chunks/02ax9y70kcggv.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/03~yq9q893hmn.js:
│!function(){var t="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof window?window:"unde
⋮

litellm/proxy/_experimental/out/_next/static/chunks/04jvxoid~vpxj.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/07.fwfv-sinb5.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS
⋮

litellm/proxy/_experimental/out/_next/static/chunks/08o64zaid_juv.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/08yy42xvwaak6.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/0e9hs7onyj28m.js:
⋮
│    `,boxShadowTabsOverflowLeft:"inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",boxShadowTabsOverflowRi
│      ${t}-loading > ${r}`]:{color:s}};return[{[t]:Object.assign(Object.assign({},(0,p.resetCompone
⋮
│      `]:{animationName:C,animationDuration:f,animationPlayState:"paused",animationTimingFunction:u
│        ${t}-move-up-appear${t}-move-up-appear-active,
│        ${t}-move-up-enter${t}-move-up-enter-active
│      `]:{animationPlayState:"running"},[`${t}-move-up-leave`]:{animationName:x,animationDuration:f
⋮
│        `]:{animationName:i.slideDownOut},"&-hidden":{display:"none"},[o]:Object.assign(Object.assi
│Must be valid JSON format`:r.enum?`Select from available options
│Allowed values: ${r.enum.join(", ")}`:E)}),children:u},e)})}):null};e.s(["ALL_PROXY_MCP_SERVERS_SEN

litellm/proxy/_experimental/out/_next/static/chunks/0ivj_wax-joap.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS
⋮

litellm/proxy/_experimental/out/_next/static/chunks/0m6zdocif1gl4.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/0nnx~7-7e5t~1.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS
⋮

litellm/proxy/_experimental/out/_next/static/chunks/0p.6bs58-_3lw.js:
⋮
│Read more: https://nextjs.org/docs/messages/failed-to-find-server-action`),"__NEXT_ERROR_CODE",{val

litellm/proxy/_experimental/out/_next/static/chunks/0pidya1qvuvx8.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/0piozaeodiue..js:
⋮
│Read more: https://nextjs.org/docs/messages/next-image-unconfigured-localpatterns`),"__NEXT_ERROR_C
⋮
│Please migrate to a newer model. Visit https://docs.anthropic.com/en/docs/resources/model-deprecati
│Please migrate to a newer model. Visit https://docs.anthropic.com/en/docs/resources/model-deprecati
⋮

litellm/proxy/_experimental/out/_next/static/chunks/0ys10755n8os_.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/11ibt3khr2hk3.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_experimental/out/_next/static/chunks/151r-5htw45m~.js:
│(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentS

litellm/proxy/_types.py:
⋮
│def hash_token(token: str):
⋮
│class UserAPIKeyAuth(LiteLLM_VerificationTokenView):  # the expected response object for user api k
⋮
│class CallbackOnUI(LiteLLMPydanticObjectBase):
⋮

litellm/proxy/auth/resolvers/models.py:
⋮
│class PrincipalType(str, Enum):
⋮

litellm/proxy/client/exceptions.py:
⋮
│class UnauthorizedError(Exception):
⋮

litellm/proxy/common_utils/swagger_utils.py:
⋮
│def get_status_code(exception):
⋮

litellm/proxy/guardrails/guardrail_hooks/custom_code/primitives.py:
⋮
│def lower(text: str) -> str:
⋮

litellm/proxy/swagger/swagger-ui-bundle.js:
⋮
│!function webpackUniversalModuleDefinition(s,o){"object"==typeof exports&&"object"==typeof module?m
⋮

litellm/proxy/utils.py:
⋮
│class PrismaClient:
│    spend_log_transactions: List = []
⋮
│    def hash_token(self, token: str):
⋮
│def hash_token(token: str):
⋮

litellm/router_strategy/budget_limiter.py:
⋮
│class _LiteLLMParamsDictView:
│    """
│    Lightweight attribute view over `litellm_params` dict.
│
│    This avoids pydantic construction in request hot-path while preserving
│    attribute-style access used by `litellm.get_llm_provider(...)`.
⋮
│    def dict(self) -> Dict[str, Any]:
⋮

litellm/router_utils/add_retry_fallback_headers.py:
⋮
│def get_hidden_params_dict(
│    response: object,
│    *,
│    create: bool = False,
⋮
│def get_fallback_errors_from_headers(
│    additional_headers: dict[str, object],
⋮

litellm/rust_bridge/loader.py:
⋮
│def get_native_bridge() -> ModuleType | None:
⋮

litellm/secret_managers/main.py:
⋮
│def str_to_bool(value: Optional[str]) -> Optional[bool]:
⋮
│def get_secret_str(
│    secret_name: str,
│    default_value: Optional[Union[str, bool]] = None,
⋮
│def get_secret(
│    secret_name: str,
│    default_value: Optional[Union[str, bool]] = None,
⋮

litellm/types/caching.py:
⋮
│class RedisPipelineSetOperation(TypedDict):
⋮
│class CachedEmbedding(TypedDict):
⋮

litellm/types/completion.py:
⋮
│class ChatCompletionContentPartTextParam(TypedDict, total=False):
⋮
│class ImageURL(TypedDict, total=False):
⋮
│class ChatCompletionContentPartImageParam(TypedDict, total=False):
⋮
│class Function(TypedDict, total=False):
⋮
│class ChatCompletionToolMessageParam(TypedDict, total=False):
⋮
│class ChatCompletionFunctionMessageParam(TypedDict, total=False):
⋮
│class ChatCompletionMessageToolCallParam(TypedDict, total=False):
⋮
│class ChatCompletionAssistantMessageParam(TypedDict, total=False):
⋮

litellm/types/interactions/generated.py:
⋮
│class Function(BaseModel):
⋮
│class Error(BaseModel):
⋮

litellm/types/llms/base.py:
⋮
│class HiddenParams(OpenAIObject):
⋮

litellm/types/llms/openai.py:
⋮
│class Function(TypedDict, total=False):
⋮

litellm/types/llms/vertex_ai.py:
⋮
│class Date(TypedDict):
⋮

litellm/types/mcp_server/mcp_server_manager.py:
⋮
│class MCPServer(BaseModel):
⋮

litellm/types/proxy/litellm_pre_call_utils.py:
⋮
│class RedactedDict(dict):
⋮

litellm/types/proxy/management_endpoints/common_daily_activity.py:
⋮
│class GroupByDimension(str, Enum):
⋮
│class MetricBase(BaseModel):
⋮
│class LiteLLM_DailyUserSpend(BaseModel):
⋮
│class GroupedData(TypedDict):
⋮

litellm/types/proxy/policy_engine/policy_types.py:
⋮
│class PolicyScope(BaseModel):
⋮
│class PolicyAttachment(BaseModel):
│    """
│    Attaches a policy to a scope - defines WHERE a policy applies.
│
│    Attachments are REQUIRED to make policies active. A policy without
│    an attachment will not be applied to any requests.
│
│    Example YAML:
│    ```yaml
│    policy_attachments:
│      - policy: global-baseline
⋮
│    def is_global(self) -> bool:
⋮

litellm/types/router.py:
⋮
│class GenericLiteLLMParams(CredentialLiteLLMParams, CustomPricingLiteLLMParams):
⋮

litellm/types/utils.py:
⋮
│class Function(OpenAIObject):
⋮
│class PromptTokensDetailsWrapper(
│    SafeAttributeModel, PromptTokensDetails
⋮
│class StreamingChoices(OpenAIObject):
⋮
│class ModelResponseStream(ModelResponseBase):
⋮
│class ModelResponse(ModelResponseBase):
⋮
│class ImageObject(OpenAIImage):
⋮
│class LiteLLMLoggingBaseClass:
│    """
│    Base class for logging pre and post call
│
│    Meant to simplify type checking for logging obj.
⋮
│    def post_call(self, original_response, input=None, api_key=None, additional_args={}):
⋮

terraform/litellm/aws/variables.tf:
⋮
│variable "gateway_num_workers" {
⋮
│variable "redis_num_replicas" {
⋮
│variable "otel_exporter" {
⋮
│variable "otel_capture_message_content" {
⋮

terraform/litellm/gcp/variables.tf:
⋮
│variable "gateway_num_workers" {
⋮
│variable "db_edition" {
⋮
│variable "otel_exporter" {
⋮
│variable "otel_capture_message_content" {
⋮

terraform/provider/litellm/types.go:
⋮
│type ModelResponse struct {
│	ModelName     string                 `json:"model_name"`
│	LiteLLMParams LiteLLMParams          `json:"litellm_params"`
│	ModelInfo     ModelInfo              `json:"model_info"`
│	Additional    map[string]interface{} `json:"additional"`
⋮

tests/agent_tests/test_a2a_agent.py:
⋮
│class MockA2AResponse:
│    def __init__(self, text: str):
│        self._payload = {
│            "id": str(uuid4()),
│            "jsonrpc": "2.0",
│            "result": {
│                "message": {
│                    "role": "agent",
│                    "parts": [{"kind": "text", "text": text}],
│                    "messageId": uuid4().hex,
│                }
⋮
│    def model_dump(self, mode="json", exclude_none=True):
⋮

tests/e2e/e2e_http.py:
⋮
│class UnauthorizedError(BaseModel):
⋮
│class StreamingResponse(BaseModel):
⋮

tests/e2e/models.py:
⋮
│class CustomPricing(BaseModel):
⋮

tests/litellm_utils_tests/test_get_secret.py:
⋮
│class MockSecretClient:
│    def get_secret(self, secret_name):
⋮

tests/llm_responses_api_testing/test_responses_hooks.py:
⋮
│def test_log_completed_response_falls_back_when_model_validate_fails(monkeypatch):
│    class _BadSerializableResponse:
│        @classmethod
│        def model_validate(cls, value):
│            raise RuntimeError("nope")
│
│        def model_dump(self):
⋮

tests/llm_translation/reasoning_effort_grid/grid_spec.py:
⋮
│@dataclass(frozen=True)
│class ModelEntry:
⋮

tests/llm_translation/test_openai.py:
⋮
│@patch("litellm.main.openai_chat_completions._get_openai_client")
│def test_openai_image_generation_forwards_organization(mock_get_openai_client):
│    """Ensure organization flows to OpenAI client for image generation."""
│
│    class _DummyImages:
│        def generate(self, **kwargs):  # type: ignore
│            class _Resp:
│                def model_dump(self_inner):  # minimal OpenAI ImagesResponse shape
│                    return {
│                        "created": 123,
│                        "data": [{"url": "http://example.com/image.png"}],
│                        "usage": {
│                            "input_tokens": 0,
│                            "output_tokens": 0,
│                            "total_tokens": 0,
│                        },
⋮

tests/local_testing/test_streaming.py:
⋮
│class Function(BaseModel):
⋮

tests/pass_through_unit_tests/test_pass_through_unit_tests.py:
⋮
│@pytest.fixture
│def mock_request():
│    # Create a mock request with headers
│    class QueryParams:
│        def __init__(self):
│            self._dict = {}
│
│        def __iter__(self):
│            return iter(self._dict.items())
│
│        def items(self):
│            return self._dict.items()
│
⋮

tests/test_litellm/caching/test_redis_semantic_cache.py:
⋮
│def test_redis_semantic_cache_prompt_extraction_handles_model_objects():
│    from litellm.caching.redis_semantic_cache import RedisSemanticCache
│
⋮
│    class DictInput:
│        def dict(self):
⋮

tests/test_litellm/integrations/code_interpreter_interception/test_handler.py:
⋮
│class FakeLogging:
│    def __init__(self, litellm_call_id="k1"):
│        self.litellm_call_id = litellm_call_id
│        self.model_call_details = {}
⋮
│    def post_call(self, *args, **kwargs):
⋮

tests/test_litellm/litellm_core_utils/test_safe_json_dumps.py:
⋮
│def test_clean_strings_are_not_run_through_replace():
│    """Regression for LIT-3910.
│
│    safe_dumps must not call ``str.replace`` on NUL-free strings. Running the
│    NUL strip unconditionally on every value and dict key (the v1.89.x behavior)
│    added per-request serialization overhead that scaled with payload size and
│    showed up under ``store_prompts_in_spend_logs``. Clean strings, which are the
│    overwhelming majority, must be returned untouched.
⋮
│    class ReplaceForbidden(str):
│        def replace(self, *args, **kwargs):
⋮

tests/test_litellm/llms/bedrock/batches/test_handler.py:
⋮
│def test_extract_region_swallows_unexpected_split_errors():
│    """Defensive `except Exception` branch — anything that isn't a plain str
⋮
│    class WeirdArn:
│        def split(self, _sep):
⋮

tests/test_litellm/llms/github_copilot/test_github_copilot_transformation.py:
⋮
│@patch("litellm.llms.openai.openai.OpenAIChatCompletion._get_openai_client")
⋮
│def test_openai_handler_repairs_github_copilot_empty_choices(
│    mock_request, mock_get_client
│):
│    """
│    The OpenAI SDK handler calls convert_to_model_response_object directly on the
│    SDK's parsed output, bypassing transform_response. convert raises APIError on
│    empty choices, so the handler must route github_copilot responses through
│    transform_parsed_response_dict first. Removing that wiring (or resolving a
│    config without the override) fails this test with APIError.
│
│    See: https://github.com/BerriAI/litellm/issues/30927
⋮
│    class _FakeSDKResponse:
│        def model_dump(self):
│            return {
│                "id": "msg_vrtx_01",
│                "model": "claude-opus-4.8",
│                "object": "chat.completion",
│                "choices": [],
│                "content": [{"type": "text", "text": "Hi there"}],
│                "stop_reason": "end_turn",
│                "usage": {"input_tokens": 12, "output_tokens": 3},
⋮

tests/test_litellm/passthrough/test_passthrough_main.py:
⋮
│@pytest.fixture
│def mock_request():
│    """Create a mock request with headers"""
⋮
│    class QueryParams:
⋮

tests/test_litellm/proxy/_experimental/mcp_server/test_mcp_server.py:
⋮
│@pytest.mark.asyncio
│async def test_stateful_mcp_get_stream_does_not_block_post():
│    """
│    A long-lived GET (server-to-client SSE stream) on a stateful session
│    must NOT hold the per-session lock — otherwise subsequent POSTs on the
│    same mcp-session-id hang for the lifetime of the stream.
⋮
│    async def call(method: str, body: bytes = b""):
⋮
│@pytest.mark.asyncio
│async def test_truncated_jsonrpc_response_with_nested_method_skips_lock():
│    """Regression: a large JSON-RPC *response* POST whose ``result`` payload
│    nests a ``method`` key must skip the per-session lock so it does not
│    deadlock behind the in-flight request POST that is holding the lock while
⋮
│    async def call(body: bytes):
⋮

tests/test_litellm/proxy/guardrails/guardrail_hooks/test_presidio.py:
⋮
│@pytest.mark.asyncio
│async def test_presidio_filter_scope_initializer(monkeypatch):
│    """
│    Ensure initializer respects presidio_filter_scope for input/output/both.
⋮
│    class DummyManager:
│        def __init__(self):
⋮
│        def add_litellm_callback(self, cb):
⋮

tests/test_litellm/proxy/proxy_server/test_streaming_helpers.py:
⋮
│def test_data_generator_yields_sse_lines_for_dict_chunks():
│    class DictChunk:
│        def __init__(self, payload):
│            self._payload = payload
│
│        def dict(self):
⋮
│def test_data_generator_fallback_when_dict_raises_exception():
│    class BadChunk:
│        def dict(self):
⋮

tests/test_litellm/proxy/utils/helpers/test_model_access.py:
⋮
│def test_model_dump_with_preserved_fields_no_choices_returns_plain_dump():
│    class _Bare:
│        def model_dump(self, **_kwargs):
⋮

tests/test_litellm/repositories/test_repositories.py:
⋮
│class MockRecord:
│    """Mock database record for testing."""
│
⋮
│    def dict(self) -> Dict[str, Any]:
⋮
│class TestBaseRepository:
│    @pytest.fixture
│    def prisma_client(self):
⋮
│    def test_record_to_dict_branches(self):
│        from litellm.repositories.base_repository import _record_to_dict
│
⋮
│        class WithDict:
│            def dict(self):
⋮

tests/test_litellm/router_utils/test_add_retry_fallback_headers.py:
⋮
│def test_get_hidden_params_dict_with_pydantic_model_hidden_params():
│    class InnerHiddenParams(BaseModel):
⋮
│    class Response:
⋮

ui/litellm-dashboard/src/app/(dashboard)/access-groups/_components/AccessGroupsModal/AccessGroupBase
⋮
│interface AccessGroupBaseFormProps {
│  form: FormInstance<AccessGroupFormValues>;
│  isNameDisabled?: boolean;
⋮

ui/litellm-dashboard/src/app/(dashboard)/caching/_components/coordination_redis_settings/types.ts:
⋮
│export type CoordinationRedisSection = "connection" | "cluster" | "sentinel";
│
⋮

ui/litellm-dashboard/src/app/(dashboard)/cost-tracking/_components/add_margin_form.tsx:
⋮
│                const numValue = parseFloat(value);
⋮
│                const numValue = parseFloat(value);
⋮

ui/litellm-dashboard/src/app/(dashboard)/cost-tracking/_components/pricing_calculator/types.ts:
⋮
│export interface ModelEntry {
│  id: string;
│  model: string;
│  input_tokens: number;
│  output_tokens: number;
│  num_requests_per_day?: number;
│  num_requests_per_month?: number;
⋮

ui/litellm-dashboard/src/app/(dashboard)/cost-tracking/_components/types.ts:
⋮
│export interface DiscountConfig {
│  [provider: string]: number;
⋮
│export interface MarginConfig {
│  [provider: string]: number | { percentage?: number; fixed_amount?: number };
⋮

ui/litellm-dashboard/src/app/(dashboard)/guardrails/_components/content_filter/CompetitorIntentConfi
⋮
│export interface CompetitorIntentConfig {
│  competitor_intent_type: "airline" | "generic";
│  brand_self: string[];
│  locations?: string[];
│  competitors?: string[];
│  policy?: {
│    competitor_comparison?: "refuse" | "reframe";
│    possible_competitor_comparison?: "refuse" | "reframe";
│  };
│  threshold_high?: number;
⋮

ui/litellm-dashboard/src/app/(dashboard)/guardrails/_components/content_filter/ContentCategoryConfig
⋮
│interface SelectedCategory {
│  id: string;
│  category: string;
│  display_name: string;
│  action: "BLOCK" | "MASK";
│  severity_threshold: "high" | "medium" | "low";
⋮

ui/litellm-dashboard/src/app/(dashboard)/guardrails/_components/guardrail_optional_params.tsx:
⋮
│interface ProviderParam {
│  param: string;
│  description: string;
│  required: boolean;
│  default_value?: string;
│  options?: string[];
│  type?: string;
│  fields?: { [key: string]: ProviderParam };
│  dict_key_options?: string[];
│  dict_value_type?: string;
⋮

ui/litellm-dashboard/src/app/(dashboard)/playground/components/chat_ui/A2AMetrics.tsx:
⋮
│export interface A2ATaskMetadata {
│  taskId?: string;
│  contextId?: string;
│  status?: {
│    state?: string;
│    timestamp?: string;
│    message?: string;
│  };
│  metadata?: Record<string, any>;
⋮

ui/litellm-dashboard/src/app/(dashboard)/playground/components/chat_ui/ChatUI.tsx:
⋮
│                      <TextInput
│                        className="mt-2"
│                        placeholder="Enter custom model name"
│                        onValueChange={(value) => {
│                          // Using setTimeout to create a simple debounce effect
│                          if (customModelTimeout.current) {
│                            clearTimeout(customModelTimeout.current);
│                          }
│
│                          customModelTimeout.current = setTimeout(() => {
⋮

ui/litellm-dashboard/src/app/(dashboard)/playground/components/compareUI/endpoint_config.ts:
⋮
│export type EndpointIdType = (typeof EndpointId)[keyof typeof EndpointId];
│
⋮

ui/litellm-dashboard/src/app/(dashboard)/vector-stores/_components/CreateVectorStore.tsx:
⋮
│                        <img
│                          src={resolveLogoSrc(vectorStoreProviderLogoMap[providerDisplayName])}
│                          alt={`${providerEnum} logo`}
│                          className="w-5 h-5"
│                          onError={(e) => {
│                            // Create a div with provider initial as fallback
│                            const target = e.target as HTMLImageElement;
│                            const parent = target.parentElement;
│                            if (parent) {
│                              const fallbackDiv = document.createElement("div");
│                              fallbackDiv.className =
│                                "w-5 h-5 rounded-full bg-gray-200 flex items-center justify-center 
│                              fallbackDiv.textContent = providerDisplayName.charAt(0);
│                              parent.replaceChild(fallbackDiv, target);
⋮

ui/litellm-dashboard/src/components/AIHub/AgentHubTableColumns.tsx:
⋮
│export interface AgentHubData {
│  agent_id?: string;
│  protocolVersion: string;
│  name: string;
│  description: string;
│  url: string;
│  version: string;
│  capabilities?: {
│    streaming?: boolean;
│    [key: string]: any;
⋮

ui/litellm-dashboard/src/components/CloudZeroCostTracking/types.ts:
│export interface CloudZeroSettings {
⋮

ui/litellm-dashboard/src/components/GuardrailsMonitor/mockData.ts:
⋮
│export interface LogEntry {
│  id: string;
│  timestamp: string;
│  input?: string;
│  output?: string;
│  input_snippet?: string;
│  output_snippet?: string;
│  score?: number;
│  action: "blocked" | "passed" | "flagged";
│  model?: string;
⋮

ui/litellm-dashboard/src/components/Settings/LoggingAndAlerts/LoggingCallbacks/types.ts:
⋮
│export interface AlertingVariables {
│  SLACK_WEBHOOK_URL: string | null;
│  LANGFUSE_PUBLIC_KEY: string | null;
│  LANGFUSE_SECRET_KEY: string | null;
│  LANGFUSE_HOST: string | null;
│  OPENMETER_API_KEY: string | null;
⋮

ui/litellm-dashboard/src/components/chat/ConversationList.tsx:
⋮
│type DateGroup = "Recents" | "Yesterday" | "Last 7 Days" | "Older";
│
⋮
│  const [query, setQuery] = useState("");
⋮

ui/litellm-dashboard/src/components/chat/types.ts:
⋮
│export interface Conversation {
│  id: string;
│  title: string;
│  model: string;
│  messages: ChatMessage[];
│  mcpServerNames: string[];
│  createdAt: number;
│  updatedAt: number;
⋮

ui/litellm-dashboard/src/components/chat_ui/ResponseMetrics.tsx:
⋮
│export interface TokenUsage {
│  completionTokens?: number;
│  promptTokens?: number;
│  totalTokens?: number;
│  reasoningTokens?: number;
│  cost?: number;
⋮

ui/litellm-dashboard/src/components/chat_ui/mode_endpoint_mapping.tsx:
⋮
│export enum EndpointType {
│  IMAGE = "image",
│  VIDEO = "video",
│  CHAT = "chat",
│  RESPONSES = "responses",
│  IMAGE_EDITS = "image_edits",
│  ANTHROPIC_MESSAGES = "anthropic_messages",
│  EMBEDDINGS = "embeddings",
│  SPEECH = "speech",
│  TRANSCRIPTION = "transcription",
⋮

ui/litellm-dashboard/src/components/chat_ui/types.ts:
⋮
│export interface A2ATaskMetadata {
│  taskId?: string;
│  contextId?: string;
│  status?: {
│    state?: string;
│    timestamp?: string;
│    message?: string;
│  };
│  metadata?: Record<string, any>;
⋮
│export interface MessageType {
│  role: string;
│  content: string | MultimodalContent[];
│  model?: string;
│  isImage?: boolean;
│  isAudio?: boolean;
│  isEmbeddings?: boolean;
│  reasoningContent?: string;
│  timeToFirstToken?: number;
│  totalLatency?: number;
⋮

ui/litellm-dashboard/src/components/cloudzero_export_modal.tsx:
⋮
│interface CloudZeroSettings {
│  api_key: string;
│  connection_id: string;
⋮

ui/litellm-dashboard/src/components/common_components/TableHeaderSortDropdown/TableHeaderSortDropdow
⋮
│export type SortState = "asc" | "desc" | false;
│
⋮

ui/litellm-dashboard/src/components/guardrails/types.ts:
⋮
│export enum GuardrailDefinitionLocation {
│  DB = "db",
│  CONFIG = "config",
⋮

ui/litellm-dashboard/src/components/key_team_helpers/BudgetWindowsEditor.tsx:
⋮
│interface BudgetWindowsEditorProps {
│  value: BudgetWindowEntry[];
│  onChange: (v: BudgetWindowEntry[]) => void;
⋮

ui/litellm-dashboard/src/components/key_team_helpers/key_list.tsx:
⋮
│interface UseKeyListReturn {
│  keys: KeyResponse[];
│  isLoading: boolean;
│  error: Error | null;
│  pagination: PaginationData;
│  refresh: (params?: Record<string, unknown>) => Promise<void>;
│  setKeys: Setter<KeyResponse[]>;
⋮

ui/litellm-dashboard/src/components/logging_settings_view.tsx:
⋮
│interface LoggingSettingsViewProps {
│  loggingConfigs?: LoggingConfig[];
│  disabledCallbacks?: string[];
│  variant?: "card" | "inline";
│  className?: string;
⋮

ui/litellm-dashboard/src/components/mcp_tools/mcp_tools.test.tsx:
⋮
│const renderViewer = (props: Record<string, unknown>) =>
│  render(
│    <QueryClientProvider client={new QueryClient({ defaultOptions: { queries: { retry: false } } })
│      <MCPToolsViewer
│        serverId="srv-1"
│        accessToken="litellm-key"
│        userRole="admin"
│        userID="tin@berri.ai"
│        serverAlias="slack"
│        auth_type="oauth2"
│        tokenUrl={TOKEN_URL}
⋮

ui/litellm-dashboard/src/components/mcp_tools/types.tsx:
⋮
│export type MCPEnvVarScope = "global" | "user";
│
⋮

ui/litellm-dashboard/src/components/model_dashboard/table.tsx:
⋮
│declare module "@tanstack/react-table" {
│  interface ColumnMeta<TData, TValue> {
│    className?: string;
│  }
⋮
│interface ModelDataTableProps<TData, TValue> {
│  data: TData[];
│  columns: ColumnDef<TData, TValue>[];
│  isLoading?: boolean;
│  defaultSorting?: SortingState;
│  pagination?: PaginationState;
│  onPaginationChange?: OnChangeFn<PaginationState>;
│  enablePagination?: boolean;
│  onRowClick?: (row: TData) => void;
⋮

ui/litellm-dashboard/src/components/molecules/message_manager.tsx:
⋮
│const MessageManager = {
│  success(content: string, duration?: number) {
│    getMessageApi().success(content, duration);
│  },
│
│  error(content: string, duration?: number) {
│    getMessageApi().error(content, duration);
│  },
│
│  warning(content: string, duration?: number) {
│    getMessageApi().warning(content, duration);
⋮

ui/litellm-dashboard/src/components/molecules/notifications_manager.tsx:
⋮
│type Placement = "top" | "topLeft" | "topRight" | "bottom" | "bottomLeft" | "bottomRight";
│
⋮
│type NotificationConfigResolved = Omit<NotificationConfig, "message"> & { message: string | React.R
│
⋮
│const NotificationManager = {
│  error(input: string | NotificationConfig) {
│    const cfg = normalize(input, "Error");
│    getNotification().error({
│      ...COMMON_NOTIFICATION_PROPS,
│      ...cfg,
│      placement: cfg.placement ?? defaultPlacement(),
│      duration: cfg.duration ?? 6,
│    });
│  },
│
│  warning(input: string | NotificationConfig) {
│    const cfg = normalize(input, "Warning");
│    getNotification().warning({
│      ...COMMON_NOTIFICATION_PROPS,
│      ...cfg,
│      placement: cfg.placement ?? defaultPlacement(),
│      duration: cfg.duration ?? 5,
│    });
⋮
│  fromBackend(input: any, extra?: Omit<NotificationConfig, "message" | "description">) {
│    const status = extractStatus(input);
│    const description = extractDescription(input);
│    const base = { ...(extra ?? {}), description, placement: extra?.placement ?? defaultPlacement()
│
│    if (looksErrorPayload(input, status)) {
│      const title = titleFor(status, description);
│      const payload = { ...base, message: title };
│
│      if (
⋮

ui/litellm-dashboard/src/components/organization/organization_view.tsx:
⋮
│              <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-6">
│                <Card>
│                  <Text>Organization Details</Text>
│                  <div className="mt-2">
│                    <Text>Created: {new Date(orgData.created_at).toLocaleDateString()}</Text>
│                    <Text>Updated: {new Date(orgData.updated_at).toLocaleDateString()}</Text>
│                    <Text>Created By: {orgData.created_by}</Text>
│                  </div>
│                </Card>
│
│                <Card>
│                  <Text>Budget Status</Text>
│                  <div className="mt-2">
│                    <Title>${formatNumberWithCommas(orgData.spend, 4)}</Title>
│                    <Text>
⋮

ui/litellm-dashboard/src/components/provider_info_helpers.tsx:
⋮
│export enum Providers {
│  A2A_Agent = "A2A Agent",
│  AI21 = "Ai21",
│  AI21_CHAT = "Ai21 Chat",
│  AIML = "AI/ML API",
│  AIOHTTP_OPENAI = "Aiohttp Openai",
│  Anthropic = "Anthropic",
│  ANTHROPIC_TEXT = "Anthropic Text",
│  AssemblyAI = "AssemblyAI",
│  AUTO_ROUTER = "Auto Router",
⋮

ui/litellm-dashboard/src/components/shared/DataTable/DataTableSortHeader.tsx:
⋮
│export type DataTableSortVariant = "header-cycle" | "dropdown-tristate";
│
⋮

ui/litellm-dashboard/src/components/shared/charts/chart_tooltip.tsx:
⋮
│export type ChartTooltipProps = Pick<
│  TooltipContentProps<TooltipValueType, string | number>,
│  "active" | "payload" | "label"
⋮

ui/litellm-dashboard/src/components/ui/chart.tsx:
⋮
│export type ChartConfig = Record<
│  string,
│  {
│    label?: React.ReactNode;
│    icon?: React.ComponentType;
│  } & ({ color?: string; theme?: never } | { color?: never; theme: Record<keyof typeof THEMES, stri
⋮

ui/litellm-dashboard/src/components/vector_store_management/types.tsx:
⋮
│export interface VectorStoreMetadata {
│  ingested_files?: IngestedFile[];
│  [key: string]: any;
⋮

ui/litellm-dashboard/src/components/vector_store_providers.tsx:
⋮
│export interface VectorStoreFieldConfig {
│  name: string;
│  label: string;
│  tooltip: string;
│  placeholder?: string;
│  required: boolean;
│  type?: "text" | "password" | "select";
│  options?: { value: string; label: string }[];
│  initialValue?: string;
⋮

ui/litellm-dashboard/src/components/view_logs/columns.tsx:
⋮
│export type LogsSortField = keyof typeof LOGS_SORT_FIELD_MAP;
│
⋮
│export type LogEntry = {
│  request_id: string;
│  api_key: string;
│  team_id: string;
│  model: string;
│  model_id: string;
│  api_base?: string;
│  call_type: string;
│  spend: number;
│  total_tokens: number;
⋮

ui/litellm-dashboard/src/data/compliancePrompts.ts:
⋮
│export interface CompliancePrompt {
│  id: string;
│  framework: string;
│  category: string;
│  categoryIcon: string;
│  categoryDescription: string;
│  prompt: string;
│  expectedResult: "fail" | "pass";
⋮

ui/litellm-dashboard/src/lib/http/client.ts:
⋮
│export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
│
⋮
│export type QueryParams = Record<string, QueryValue | QueryValue[]>;
│
│export interface RequestOptions {
│  /** Bearer token. When present, the auth header is set automatically. */
│  accessToken?: string | null;
│  /** Serialized to JSON unless `rawBody` is provided. */
│  body?: unknown;
│  /** Sent verbatim (FormData, Blob, pre-stringified text); disables JSON handling. */
│  rawBody?: BodyInit;
│  query?: QueryParams;
│  headers?: Record<string, string>;
│  signal?: AbortSignal;
⋮
│export class ApiError extends Error {
│  readonly status: number;
│  readonly body: unknown;
│
│  constructor(message: string, status: number, body: unknown) {
│    super(message);
│    this.name = "ApiError";
│    this.status = status;
│    this.body = body;
│  }
⋮
│export interface ApiClient {
│  request<T = any>(method: HttpMethod, path: string, options?: RequestOptions): Promise<T>;
│  get<T = any>(path: string, options?: RequestOptions): Promise<T>;
│  post<T = any>(path: string, options?: RequestOptions): Promise<T>;
│  put<T = any>(path: string, options?: RequestOptions): Promise<T>;
│  delete<T = any>(path: string, options?: RequestOptions): Promise<T>;
│  patch<T = any>(path: string, options?: RequestOptions): Promise<T>;
⋮
```

### AST Map: `modules/litellm-docs`

```python
blog/harnesses-are-the-new-llms/diagrams.js:
⋮
│const s = {
│  fig: { margin: '2.5rem 0', fontFamily: 'inherit' },
│  wrap: {
│    display: 'grid',
│    gridTemplateColumns: '180px 1fr 24px 1fr',
│    gap: '12px 12px',
│    alignItems: 'center',
│  },
│  colHeader: {
│    fontSize: 14,
⋮
│  box: (open) => ({
│    border: open ? `1.5px dashed ${BLUE}` : '1px solid var(--ifm-color-emphasis-300)',
│    background: open ? 'rgba(59,130,246,0.08)' : 'transparent',
│    borderRadius: 8,
│    padding: '14px 18px',
│    minHeight: 56,
│    display: 'flex',
│    flexDirection: 'column',
│    justifyContent: 'center',
│  }),
│  boxName: (open) => ({
│    fontSize: 14,
│    fontWeight: 700,
│    color: open ? BLUE : 'inherit',
⋮
│  legendSwatch: (open) => ({
│    width: 24,
│    height: 14,
│    borderRadius: 4,
│    border: open ? `1.5px dashed ${BLUE}` : '1px solid var(--ifm-color-emphasis-300)',
│    background: open ? 'rgba(59,130,246,0.08)' : 'transparent',
⋮

blog/litellm_rust_launch/benchmark/llm_app.py:
⋮
│@app.post("/v1/chat/completions")
│async def chat(req: Request):
⋮

blog/litellm_rust_launch/benchmark/main.rs:
⋮
│async fn run_mock() {
│    let app = Router::new()
│        .route("/v1/responses", post(mock_responses))
│        .route("/v1/chat/completions", post(mock_chat))
│        .route("/chat/completions", post(mock_chat));
│    let l = tokio::net::TcpListener::bind("127.0.0.1:9001").await.unwrap();
│    axum::serve(l, app).await.unwrap();
⋮
│async fn run_gateway() {
│    let client = reqwest::Client::builder()
│        .pool_max_idle_per_host(256)
│        .build()
│        .unwrap();
│    let app = Router::new()
│        .route("/v1/responses", post(gw_handler))
│        .route("/v1/chat/completions", post(gw_chat))
│        .with_state(Arc::new(client));
│    let l = tokio::net::TcpListener::bind("127.0.0.1:9000").await.unwrap();
⋮
│async fn run_bench(url: String, total: usize, conc: usize) {
│    let client = reqwest::Client::builder()
│        .pool_max_idle_per_host(conc * 4)
│        .build()
│        .unwrap();
│    let text = "Summarize the following text in one sentence: the quick brown fox jumps over the la
│    let payload = if url.contains("chat/completions") {
│        json!({"model": "mock", "messages": [{"role": "user", "content": text}]})
│    } else {
│        json!({"model": "openai/gpt-4o-mini", "input": text})
⋮

blog/litellm_rust_launch/benchmark/orchestrate_compare.py:
⋮
│def wait_port(port, timeout=90):
⋮
│def post_ok(url):
⋮
│def run_bench(url, total, conc):
⋮

blog/litellm_rust_launch/diagrams.js:
⋮
│export function RustHeader() {
│  const N = 37, TOP = 22, BOT = 478, NODE_X = 1000, NODE_Y = 250, CREAM = '#faf9f5';
│  const center = (N - 1) / 2;
│  const paths = [];
│  for (let i = 0; i < N; i++) {
│    const t = i / (N - 1);
│    const yl = TOP + t * (BOT - TOP);
│    const cy = NODE_Y + (yl - NODE_Y) * 0.3;
│    const op = 0.16 + (1 - Math.abs(i - center) / center) * (0.5 - 0.16);
│    paths.push(
⋮
│const s = {
│  fig: {margin: '2.5rem 0', fontFamily: 'inherit'},
│  box: {borderRadius: 12, border: '1px solid #e5e7eb', background: '#fff', padding: '2rem 2.5rem'},
│  label: {fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.12em', color
│  caption: {textAlign: 'center', fontSize: 12, color: '#9ca3af', marginTop: 12},
│  node: (border = '#d1d5db', bg = '#f9fafb', color = '#111827') => ({
│    border: `1.5px solid ${border}`, borderRadius: 8, padding: '12px 18px',
│    background: bg, color, textAlign: 'center', width: '100%', boxSizing: 'border-box',
│  }),
⋮
│const SmallArrow = ({color = '#9ca3af', h = 26}) => (
│  <svg width="2" height={h} style={{display: 'block'}} aria-hidden="true">
│    <line x1="1" y1="0" x2="1" y2={h - 6} stroke={color} strokeWidth="1.5" />
│    <polygon points={`1,${h} -2,${h - 7} 4,${h - 7}`} fill={color} />
│  </svg>
⋮
│const RightArrow = ({color = '#6b7280', w = 40, label}) => (
│  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'cen
│    {label && <span style={{fontSize: 10, color, fontWeight: 600, marginBottom: 3}}>{label}</span>}
│    <svg width={w} height="14" viewBox={`0 0 ${w} 14`} aria-hidden="true">
│      <path d={`M0 7h${w - 8}`} stroke={color} strokeWidth="1.5" />
│      <path d={`M${w - 9} 1l8 6-8 6z`} fill={color} />
│    </svg>
│  </div>
⋮
│export function RustMigrationStages() {
│  const stages = [
│    {stage: 'Stage 0 · Today', title: 'Pure Python SDK + FastAPI proxy', foot: '100% Python', color
│    {stage: 'Stage 1 · Core in Rust', title: 'Python drives Rust transforms via PyO3', foot: 'V0 to
│    {stage: 'Stage 2 · Thin shell', title: 'FastAPI shell, hot path all Rust', foot: 'V4 to V5a', c
│    {stage: 'Stage 3 · Pure Rust', title: 'axum server, Python in sidecar', foot: 'V5b', color: '#7
│  ];
│  const axis = [
│    {text: '0%', color: '#2563eb'},
│    {text: 'transforms + router', color: '#16a34a'},
⋮
│export function RouteCadence() {
│  const beats = ['1. Prove one provider', '2. Roll out all providers', '3. Fold route into the Rust
│  const routes = [
│    {name: 'OCR', start: 'Mistral OCR', note: 'lowest-risk route, start here', color: '#16a34a', bg
│    {name: '/v1/messages', start: 'one provider', note: 'adds the streaming axis', color: '#2563eb'
│    {name: '/chat/completions', start: 'one provider', note: 'largest param surface', color: '#7c3a
│  ];
│  const beatCell = (route, i) => (
│    <div style={{border: `1.5px solid ${route.color}`, background: route.bg, borderRadius: 8, paddi
│      <div style={{fontSize: 12, color: '#111827', fontWeight: 700}}>{i === 0 ? route.start : (i ==
│      {i === 0 && <div style={{fontSize: 10, color: '#9ca3af', marginTop: 3}}>{route.note}</div>}
│    </div>
⋮
│export function Stage1Architecture() {
│  return (
│    <figure style={s.fig}>
│      <div style={{...s.box, overflowX: 'auto'}}>
│        <p style={s.label}>Stage 1 · Rust core, driven by the Python SDK</p>
│        <div style={{minWidth: 720, maxWidth: 760, margin: '0 auto', display: 'flex', flexDirection
│          <div style={{...s.node('#9ca3af', '#f3f4f6'), width: 140}}>client</div>
│          <SmallArrow />
│          <div style={s.node('#2563eb', '#eff6ff', '#1e3a8a')}>
│            <div style={{fontWeight: 700, fontSize: 13}}>FastAPI proxy (Python)</div>
⋮
│export function RustServerSteps() {
│  const node = (border, bg, color, title, sub, lines) => (
│    <div style={s.node(border, bg, color)}>
│      <div style={{fontSize: 13, fontWeight: 700}}>{title}</div>
│      {sub && <div style={{fontSize: 11, color: '#6b7280', marginTop: 4}}>{sub}</div>}
│      {lines.map((line) => <div key={line} style={{fontSize: 11, color: '#374151', marginTop: 2}}>{
│    </div>
│  );
│  return (
│    <figure style={s.fig}>
⋮

blog/redis_circuit_breaker/diagrams.js:
⋮
│const s = {
│  fig: {margin: '2.5rem 0', fontFamily: 'inherit'},
│  box: {borderRadius: 12, border: '1px solid #e5e7eb', background: '#fff', padding: '2rem 2.5rem'},
│  label: {fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.12em', color
│  caption: {textAlign: 'center', fontSize: 12, color: '#9ca3af', marginTop: 12},
│  node: (border='#d1d5db', bg='#f9fafb') => ({
│    border: `1px solid ${border}`, borderRadius: 6, padding: '8px 20px',
│    fontSize: 13, background: bg, display: 'inline-block',
│  }),
│  arrow: {display: 'flex', flexDirection: 'column', alignItems: 'center'},
⋮
│const SmallArrow = ({color='#9ca3af'}) => (
│  <svg width="2" height="28" style={{display:'block'}}>
│    <line x1="1" y1="0" x2="1" y2="22" stroke={color} strokeWidth="1.5"/>
│    <polygon points="1,28 -2,21 4,21" fill={color}/>
│  </svg>
⋮
│export function CascadeFailure() {
│  return (
│    <figure style={s.fig}>
│      <div style={s.box}>
│        <p style={s.label}>Without circuit breaker — cascade failure</p>
│        <div style={{display:'flex', flexDirection:'column', alignItems:'center', gap:0}}>
│          <div style={s.node()}>LiteLLM Pod (×100)</div>
│          <SmallArrow />
│          <div style={s.node()}>Rate limit / cache check</div>
│          <div style={{position:'relative', display:'flex', flexDirection:'column', alignItems:'cen
⋮
│export function CircuitBreakerStates() {
│  const circle = (border, color, label, sub) => (
│    <div style={{display:'flex', flexDirection:'column', alignItems:'center', width: 140}}>
│      <div style={{width:88, height:88, borderRadius:'50%', border:`2px solid ${border}`, backgroun
│        <span style={{fontSize:11, fontWeight:700, color, letterSpacing:'0.06em'}}>{label}</span>
│        <span style={{fontSize:10, color:'#9ca3af', marginTop:2}}>{sub}</span>
│      </div>
│      <p style={{fontSize:11, color:'#6b7280', textAlign:'center', marginTop:10, lineHeight:1.5}}>{
│    </div>
│  );
│  const arrow = (label) => (
│    <div style={{display:'flex', flexDirection:'column', alignItems:'center', marginTop:36, marginL
│      <span style={{fontSize:10, color:'#6b7280', marginBottom:4}}>{label}</span>
│      <div style={{display:'flex', alignItems:'center'}}>
│        <div style={{height:1, width:48, background:'#9ca3af'}}/>
│        <svg width="8" height="8" style={{marginLeft:-1}}><polygon points="0,0 8,4 0,8" fill="#6b72
│      </div>
│    </div>
⋮
│export function CircuitBreakerFlow() {
│  return (
│    <figure style={s.fig}>
│      <div style={s.box}>
│        <p style={s.label}>With circuit breaker — graceful degradation</p>
│        <div style={{display:'flex', flexDirection:'column', alignItems:'center'}}>
│          <div style={s.node()}>Incoming request</div>
│          <SmallArrow />
│          <div style={{...s.node('#111827'), border:'2px solid #111827', fontWeight:600}}>Circuit B
│          <div style={{display:'flex', gap:80, marginTop:20, alignItems:'flex-start'}}>
⋮
│export function IncidentTimeline() {
│  const row = (color, text) => (
│    <div style={{display:'flex', alignItems:'flex-start', gap:10, marginBottom:12}}>
│      <div style={{marginTop:5, width:6, height:6, borderRadius:'50%', background:color, flexShrink
│      <p style={{fontSize:13, color:'#4b5563', margin:0, lineHeight:1.5}}>{text}</p>
│    </div>
│  );
│  return (
│    <figure style={s.fig}>
│      <div style={s.box}>
⋮

docusaurus.config.js:
⋮
│const config = {
│  title: 'liteLLM',
│  tagline: 'Simplify LLM API Calls',
│  favicon: '/img/favicon.ico', 
│
│  // Set the production url of your site here
│  url: 'https://docs.litellm.ai/',
│  // Set the /<baseUrl>/ pathname under which your site is served
│  // For GitHub pages deployment, it is often '/<projectName>/'
│  baseUrl: '/',
│
⋮
│  plugins: [
│    require('./plugins/optimize-images'),
│    [
│      '@docusaurus/plugin-client-redirects',
│      {
│        redirects: [
│          {
│            from: '/docs/proxy/control_plane_and_data_plane',
│            to: '/docs/proxy/multi_region',
│          },
⋮
│    [
│      '@docusaurus/plugin-content-docs',
│      {
⋮
│        async sidebarItemsGenerator({defaultSidebarItemsGenerator, docs, ...args}) {
│          const items = await defaultSidebarItemsGenerator({docs, ...args});
│
│          // Build map of doc id -> year from frontmatter date
│          const docYearMap = {};
│          for (const doc of docs) {
│            const date = doc.frontMatter && doc.frontMatter.date;
│            if (date) {
│              const year = new Date(date).getFullYear();
│              docYearMap[doc.id] = year;
⋮
│          function parseVersion(str) {
│            const match = (str || '').match(/v?(\d+)\.(\d+)\.(\d+)/);
│            if (!match) return [0, 0, 0];
│            return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
⋮
│          function flattenDocs(list) {
│            const result = [];
│            for (const item of list) {
│              if (item.type === 'doc' && item.id === 'index') continue;
│              if (item.type === 'doc') {
│                const label = item.id.replace(/\/index$/, '');
│                result.push({...item, label});
│              } else if (item.type === 'category') {
│                if (item.link && item.link.type === 'doc' && item.link.id !== 'index') {
│                  const id = item.link.id;
⋮
│          function buildMinorCategories(yearItems, expandNewest) {
│            const byMinor = {};
│            for (const item of yearItems) {
│              const [maj, min] = parseVersion(item.label || item.id || '');
│              const key = `v${maj}.${min}.x`;
│              if (!byMinor[key]) byMinor[key] = {maj, min, items: []};
│              byMinor[key].items.push(item);
│            }
│            const keys = Object.keys(byMinor);
│            for (const key of keys) byMinor[key].items.sort(compareVersionsDesc);
⋮

plugins/optimize-images.js:
⋮
│function walk(dir) {
│  if (!fs.existsSync(dir)) return [];
│  const files = [];
│  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
│    const full = path.join(dir, entry.name);
│    if (entry.isDirectory()) files.push(...walk(full));
│    else if (EXTENSIONS.has(path.extname(entry.name).toLowerCase())) files.push(full);
│  }
│  return files;
⋮
│async function optimizeFile(filePath) {
│  const ext = path.extname(filePath).toLowerCase();
│  const tmp = filePath + '.opt';
│  try {
│    const pipeline = sharp(filePath);
│    if (ext === '.png') {
│      await pipeline.png({ quality: QUALITY, compressionLevel: 9 }).toFile(tmp);
│    } else {
│      await pipeline.jpeg({ quality: QUALITY, mozjpeg: true }).toFile(tmp);
│    }
⋮
│module.exports = function optimizeImagesPlugin() {
│  return {
│    name: 'optimize-images',
│    async postBuild({ outDir }) {
│      const files = walk(outDir);
│      if (!files.length) return;
│      let saved = 0;
│      await Promise.all(files.map(async (f) => { saved += await optimizeFile(f); }));
│      const mb = (saved / 1024 / 1024).toFixed(1);
│      console.log(`\n[optimize-images] Compressed ${files.length} images, saved ${mb} MB`);
│    },
⋮

src/components/ClaudeCodeCompatibilityTable/index.tsx:
⋮
│type CellStatus = "pass" | "fail" | "not_tested" | "not_applicable";
│
│interface Cell {
│  status: CellStatus;
│  error?: string;
│  reason?: string;
⋮
│interface Feature {
│  id: string;
│  name: string;
│  providers: Record<string, Cell>;
⋮
│interface Matrix {
│  schema_version: string;
│  generated_at: string;
│  litellm_version: string;
│  claude_code_version: string;
│  providers: string[];
│  features: Feature[];
⋮
│function cellTitle(cell: Cell): string {
│  if (cell.status === "fail" && cell.error) return cell.error;
│  if (cell.status === "not_applicable" && cell.reason) return cell.reason;
│  if (cell.status === "not_tested") return "no test ran for this combination";
│  return "passing";
⋮
│export default function ClaudeCodeCompatibilityTable(): JSX.Element {
│  const m = matrix as Matrix;
│  return (
│    <div className={styles.wrapper}>
│      <div className={styles.meta}>
│        <span>
│          litellm <code>{m.litellm_version}</code>
│        </span>
│        <span>
│          claude code <code>{m.claude_code_version}</code>
│        </span>
│        <span>
⋮
│          {m.features.map((feature) => (
│            <tr key={feature.id}>
│              <th scope="row" className={styles.featureCol}>
│                {feature.name}
│              </th>
│              {m.providers.map((p) => {
│                const cell = feature.providers[p] ?? { status: "not_tested" as const };
│                return (
│                  <td
│                    key={p}
│                    className={styles[`status_${cell.status}`]}
│                    title={cellTitle(cell)}
│                  >
│                    {STATUS_GLYPH[cell.status]}
│                  </td>
⋮

src/components/CloudArchitecture/CloudArchitecture.tsx:
⋮
│function Icon({ file, className }: { file: string; className?: string }) {
│  return (
│    <img
│      src={useBaseUrl(`/img/cloud_icons/${file}`)}
⋮
│function Node({
│  icon,
│  title,
│  subtitle,
│  accent,
│  small,
⋮
│function ComputeNode({
│  icon,
│  title,
│  subtitle,
│  replicas,
⋮
│function ConnectorDown({ label }: { label?: string }) {
│  if (!label) return <div className={styles.connectorDown} />;
│  return (
│    <div className={styles.connectorLabeled}>
│      <span className={styles.connectorLabel}>{label}</span>
│      <div className={styles.connectorDown} />
│    </div>
│  );
⋮
│        {CSP_TABS.map((t) => (
│          <button
│            key={t.key}
│            role="tab"
│            aria-selected={t.key === csp.key}
│            className={`${styles.tab} ${t.key === csp.key ? styles.tabActive : ''}`}
│            onClick={() => setCspKey(t.key)}
│          >
│            <Icon file={t.icon} className={styles.tabIcon} />
│            {t.label}
⋮
│            <button
│              key={v.key}
│              className={`${styles.variantPill} ${v.key === variant ? styles.variantPillActive : ''
│              onClick={() => setVariantByCsp({ ...variantByCsp, [csp.key]: v.key })}
⋮
│          <button
│            key={k}
│            role="tab"
│            aria-selected={k === csp}
│            className={`${styles.tab} ${k === csp ? styles.tabActive : ''}`}
│            onClick={() => setCsp(k)}
⋮

src/components/ControlPlaneArchitecture/ControlPlaneArchitecture.tsx:
⋮
│function ArchitectureView() {
│  return (
│    <div className={styles.diagram}>
│      {/* User */}
│      <div className={styles.userRow}>
│        <div className={styles.userIcon}>&#128100;</div>
│        <span className={styles.userLabel}>Admin</span>
│      </div>
│
│      <div className={styles.connectorDown} />
│
⋮
│export default function ControlPlaneArchitecture() {
│  return (
│    <div className={styles.wrapper}>
│      <ArchitectureView />
│    </div>
│  );
⋮

src/components/CrispChat.js:
⋮
│const CrispChat = () => {
│    useEffect(() => {
│        window.$crisp = [];
│        window.CRISP_WEBSITE_ID = "be07a4d6-dba0-4df7-961d-9302c86b7ebc";
│
│        const d = document;
│        const s = d.createElement("script");
│        s.src = "https://client.crisp.chat/l.js";
│        s.async = 1;
│        document.getElementsByTagName("head")[0].appendChild(s);
⋮

src/components/DashboardWebRTCTester.jsx:
⋮
│function useLog() {
│  const [entries, setEntries] = useState([]);
│  const add = useCallback((level, tag, msg) => {
│    const time = new Date().toTimeString().slice(0, 8);
│    setEntries(prev => [...prev, { level, tag, msg, time, id: Date.now() + Math.random() }]);
│  }, []);
│  const clear = useCallback(() => setEntries([]), []);
│  return { entries, add, clear };
⋮
│export default function WebRTCTester() {
│  const [open, setOpen] = useState(false);
│  const [activeTab, setActiveTab] = useState('logs');
│  const [proxyUrl, setProxyUrl] = useState('http://localhost:4000');
│  const [apiKey, setApiKey] = useState('sk-1234');
│  const [model, setModel] = useState('gpt-4o-realtime-preview');
│  const [status, setStatus] = useState('idle');
│  const [flowStep, setFlowStep] = useState(0);
│  const [tokenPreview, setTokenPreview] = useState('—');
│  const [iceState, setIceState] = useState('—');
⋮
│  function drawBars() {
│    animRef.current = requestAnimationFrame(drawBars);
│    if (!analyserRef.current) return;
│    const data = new Uint8Array(analyserRef.current.frequencyBinCount);
│    analyserRef.current.getByteFrequencyData(data);
│    setBars(Array.from({ length: 28 }, (_, i) => Math.max(2, ((data[i] || 0) / 255) * 42)));
⋮
│  function setupAnalyser(stream) {
│    audioCtxRef.current = new AudioContext();
│    const src = audioCtxRef.current.createMediaStreamSource(stream);
│    analyserRef.current = audioCtxRef.current.createAnalyser();
│    analyserRef.current.fftSize = 64;
│    src.connect(analyserRef.current);
│    drawBars();
⋮
│  function stopSession() {
│    if (pcRef.current) { pcRef.current.close(); pcRef.current = null; }
│    if (streamRef.current) { streamRef.current.getTracks().forEach(t => t.stop()); streamRef.curren
│    if (animRef.current) { cancelAnimationFrame(animRef.current); animRef.current = null; }
│    tokenRef.current = null;
│    micRef.current = false;
│    setConnected(false);
│    setStatus('idle');
│    setFlowStep(0);
│    setTokenPreview('—');
⋮
│  const f = (n) => flowStep >= n;
│
⋮

src/components/HomepageFeatures/index.js:
⋮
│function Feature({Svg, title, description}) {
│  return (
│    <div className={clsx('col col--4')}>
│      <div className="text--center">
│        <Svg className={styles.featureSvg} role="img" />
│      </div>
│      <div className="text--center padding-horiz--md">
│        <h3>{title}</h3>
│        <p>{description}</p>
│      </div>
⋮
│export default function HomepageFeatures() {
│  return (
│    <section className={styles.features}>
│      <div className="container">
│        <div className="row">
│          {FeatureList.map((props, idx) => (
│            <Feature key={idx} {...props} />
│          ))}
│        </div>
│      </div>
⋮

src/components/MiddlewareDiagrams/BaseHTTPMiddlewareAnimation.tsx:
⋮
│interface Stage {
│  label: string;
│  subtitle: string;
│  code: string;
⋮
│          <div className={styles.stageWrapper} key={i}>
│            <div
│              className={`${styles.stage} ${activeStage === i ? styles.stageActive : ''}`}
│              onClick={() => handleStageClick(i)}
│              role="button"
│              tabIndex={0}
⋮

src/components/MiddlewareDiagrams/BenchmarkVisualization.tsx:
⋮
│interface Dot {
│  id: number;
│  progress: number; // 0..1 (top to bottom)
⋮

src/components/MiddlewareDiagrams/PureASGIAnimation.tsx:
⋮
│interface Stage {
│  label: string;
│  subtitle: string;
⋮

src/components/NavigationCards/index.js:
⋮
│export default function NavigationCards({ items, columns = 2 }) {
│  return (
│    <div
│      className={styles.grid}
│      style={{ '--nav-columns': columns }}
│    >
│      {items.map((item, i) => {
│        const isExternal =
│          item.to && (item.to.startsWith('http://') || item.to.startsWith('https://'));
│        return (
⋮

src/components/QuickStart.js:
⋮
│  const QuickStart = () => {
│    const [token, setToken] = useState(null);
│  
│    useEffect(() => {
│      const generateToken = async () => {
│        try {
│          const response = await fetch('https://proxy.litellm.ai/key/new', {
│            method: 'POST',
│            headers: {
│              'Content-Type': 'application/json',
│              'Authorization': 'Bearer sk-liteplayground',
│            },
│            body: JSON.stringify({'total_budget': 100})
│          });
│          
⋮

src/components/SubscribeForm/index.js:
⋮
│export default function SubscribeForm() {
│  const [email, setEmail] = React.useState('');
│  const [honeypot, setHoneypot] = React.useState('');
│  const [status, setStatus] = React.useState('idle'); // idle | loading | success | error
│
│  async function handleSubmit(e) {
│    e.preventDefault();
│    if (honeypot) return;
│    setStatus('loading');
│    try {
│      const res = await fetch(LOOPS_FORM_URL, {
│        method: 'POST',
│        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
│        body: new URLSearchParams({email}),
│      });
⋮

src/components/TokenGen.js:
⋮
│const TokenGen = () => {
│  const [token, setToken] = useState(null);
│
│  useEffect(() => {
│    const generateToken = async () => {
│      try {
│        const response = await fetch('https://proxy.litellm.ai/key/new', {
│          method: 'POST',
│          headers: {
│            'Content-Type': 'application/json',
│            'Authorization': 'Bearer sk-liteplayground',
│          },
│          body: JSON.stringify({'total_budget': 100})
│        });
│        
⋮

src/components/TransformRequestPlayground.tsx:
⋮
│type ViewMode = 'split' | 'request' | 'transformed';
│
⋮

src/components/VersionVerificationTable/index.tsx:
⋮
│interface VersionEntry {
│  version: string;
│  sha256: string;
│  gitCommit: string;
⋮
│interface Props {
│  entries: VersionEntry[];
⋮
│function CopyButton({ text }: { text: string }) {
│  const [copied, setCopied] = useState(false);
│
│  const handleCopy = () => {
│    navigator.clipboard.writeText(text).then(() => {
│      setCopied(true);
│      setTimeout(() => setCopied(false), 1500);
│    });
│  };
│
⋮

src/components/WebRTCTester.jsx:
⋮
│export default function WebRTCTester() {
│  return (
│    <>
│      <DashboardWebRTCTester />
│      <style>{LIGHT_MODE_OVERRIDES}</style>
│    </>
│  );
⋮

src/components/queryParamReader.js:
⋮
│const CodeBlock = ({ token }) => {
│  const codeWithToken = `
│import os
│from litellm import completion
│
│# set ENV variables 
│os.environ["LITELLM_TOKEN"] = '${token}'
│
│messages = [{ "content": "Hello, how are you?","role": "user"}]
│
⋮
│const QueryParamReader = () => {
│  const [token, setToken] = useState(null);
│
│  useEffect(() => {
│    const urlParams = new URLSearchParams(window.location.search);
│    console.log("urlParams: ", urlParams)
│    const token = urlParams.get('token');
│    setToken(token);
│  }, []);
│
⋮

src/components/queryParamToken.js:
⋮
│const QueryParamToken = () => {
│  const [token, setToken] = useState(null);
│
│  useEffect(() => {
│    const urlParams = new URLSearchParams(window.location.search);
│    const token = urlParams.get('token');
│    setToken(token);
│  }, []);
│
│  return (
⋮

src/pages-fake/index.js:
⋮
│function HomepageHeader() {
│  const {siteConfig} = useDocusaurusContext();
│  return (
│    <header className={clsx('hero hero--primary', styles.heroBanner)}>
│      <div className="container">
│        <h1 className="hero__title">{siteConfig.title}</h1>
│        <p className="hero__subtitle">{siteConfig.tagline}</p>
│        <div className={styles.buttons}>
│          <Link
│            className="button button--secondary button--lg"
⋮
│export default function Home() {
│  const {siteConfig} = useDocusaurusContext();
│  return (
│    <Layout
│      title={`Hello from ${siteConfig.title}`}
│      description="Description will go into a meta tag in <head />">
│      <HomepageHeader />
│      <main>
│        <HomepageFeatures />
│      </main>
⋮

src/remark/raw-markdown.js:
│function remarkRawMarkdown() {
⋮

src/theme/BlogListPage/index.js:
⋮
│function hasTag(item, tagSet) {
│  const tags = item.content?.metadata?.tags || [];
│  return tags.some(t => tagSet.includes(t.label));
⋮
│function filterItems(items, tab) {
│  if (tab === 'all') return items;
│  if (tab === 'security') return items.filter(i => hasTag(i, SECURITY_TAGS));
│  if (tab === 'infrastructure') return items.filter(i => hasTag(i, INFRA_TAGS));
│  if (tab === 'ideas') return items.filter(i => hasTag(i, IDEAS_TAGS));
│  return items.filter(i =>
│    !hasTag(i, SECURITY_TAGS) &&
│    !hasTag(i, INFRA_TAGS) &&
│    !hasTag(i, IDEAS_TAGS)
│  );
⋮
│function formatDate(dateStr) {
│  return new Date(dateStr).toLocaleDateString('en-US', {
│    month: 'long', day: 'numeric', year: 'numeric',
│  });
⋮

src/theme/BlogPostPage/index.js:
⋮
│function BackLink() {
│  return (
│    <div className={styles.backOuter}>
│      <a href="/blog" className={styles.backLink}>
│        <svg className={styles.backArrow} fill="none" stroke="currentColor" viewBox="0 0 24 24" ari
│          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16l-4-4m0 0l4-4m
│        </svg>
│        Blog
│      </a>
│    </div>
⋮
│export default function BlogPostPage(props) {
│  // Add body class so CSS can hide the sidebar
│  useEffect(() => {
│    document.body.classList.add('blog-post-body');
│    return () => document.body.classList.remove('blog-post-body');
│  }, []);
│
│  return (
│    <>
│      <BackLink />
⋮

src/theme/DocItem/Content/index.js:
⋮
│const CopyIcon = () => (
│  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
│    <rect x="9" y="9" width="13" height="13" rx="2" />
│    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
│  </svg>
⋮
│const CheckIcon = () => (
│  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.
│    <polyline points="20 6 9 17 4 12" />
│  </svg>
⋮
│function CopyMarkdownButton({rawMarkdownB64}) {
│  const [copied, setCopied] = useState(false);
│
│  async function handleClick() {
│    if (copied) return;
│    try {
│      await navigator.clipboard.writeText(atob(rawMarkdownB64));
│      setCopied(true);
│      setTimeout(() => setCopied(false), 2000);
│    } catch {
│      // clipboard write failed silently
│    }
⋮
│function useSyntheticTitle() {
│  const {metadata, frontMatter, contentTitle} = useDoc();
│  const shouldRender = !frontMatter.hide_title && typeof contentTitle === 'undefined';
│  return shouldRender ? metadata.title : null;
⋮
│export default function DocItemContent({children}) {
│  const syntheticTitle = useSyntheticTitle();
│  const {frontMatter} = useDoc();
│  const rawMarkdownB64 = frontMatter.rawMarkdownB64;
│
│  return (
│    <div className={clsx(ThemeClassNames.docs.docMarkdown, 'markdown')}>
│      {syntheticTitle ? (
│        <header className={styles.titleRow}>
│          <Heading as="h1" className={styles.title}>{syntheticTitle}</Heading>
⋮

src/theme/DocSidebar/index.js:
⋮
│export default function DocSidebar(props) {
│  return (
│    <>
│      <div className={styles.sidebarDesktop}>
│        <div className={styles.sidebarContainer}>
│          <div className={styles.searchBarSection}>
│            <div className={styles.searchBarInner}>
│              <SearchBar />
│            </div>
│          </div>
⋮

src/theme/Navbar/Content/index.js:
⋮
│function useNavbarItems() {
│  return useThemeConfig().navbar.items;
⋮
│function NavbarItems({ items }) {
│  return (
│    <>
│      {items.map((item, i) => (
│        <ErrorCauseBoundary
│          key={i}
│          onError={(error) =>
│            new Error(
│              `A theme navbar item failed to render.\n${JSON.stringify(item, null, 2)}`,
│              { cause: error },
⋮
│export default function NavbarContent() {
│  const mobileSidebar = useNavbarMobileSidebar();
│  const items = useNavbarItems();
│  const [leftItems, rightItems] = splitNavbarItems(items);
│  const searchBarItem = items.find((item) => item.type === 'search');
│
│  return (
│    <div className="navbar__inner">
│      {/* Left: Logo only */}
│      <div className="navbar__brand-col">
⋮

src/theme/TOC/index.js:
⋮
│export default function TOC({ className, ...props }) {
│  return (
│    <div className={clsx(styles.tableOfContents, className)}>
│      {/* Scrollable TOC items */}
│      <div className={clsx(styles.tocItemsContainer, 'thin-scrollbar')}>
│        <TOCItems
│          {...props}
│          linkClassName={LINK_CLASS_NAME}
│          linkActiveClassName={LINK_ACTIVE_CLASS_NAME}
│        />
⋮
```