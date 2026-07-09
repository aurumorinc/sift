---
name: langfuse
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging langfuse. Use this skill whenever modifying langfuse configurations or adding related functionality.
---
# langfuse

## File Tree

```text
langfuse/
├── assets
├── modules
│   ├── langfuse (See AST Map below)
│   ├── langfuse-docs (See AST Map below)
│   └── langfuse-python (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/langfuse`

```python
packages/shared/scripts/seeder/scenarios/trace-tree.ts:
⋮
│type TreeNode = {
│  index: number;
│  parentIndex: number | null;
│  depth: number;
│  kind: ObservationType;
⋮

packages/shared/scripts/seeder/scenarios/types.ts:
⋮
│export type ScenarioFlagType = "string" | "number" | "boolean";
│
⋮
│export type ScenarioContext = {
│  projectId: string;
│  environment: string;
│  seed: number;
│  idPrefix: string;
│  dryRun: boolean;
│  baseUrl: string;
│  log: (message: string) => void;
⋮

packages/shared/scripts/seeder/utils/types.ts:
⋮
│export type SeederMode = "bulk" | "synthetic";
│
⋮

packages/shared/src/domain/observation-field-groups.ts:
⋮
│export type ObservationFieldGroupFull =
⋮

packages/shared/src/domain/observations.ts:
⋮
│export type ObservationType = z.infer<typeof ObservationTypeDomain>;
│
⋮

packages/shared/src/domain/score-configs.ts:
⋮
│export type ScoreConfigCategoryDomain = z.infer<typeof ScoreConfigCategory>;

packages/shared/src/domain/scores.ts:
⋮
│export type ScoreSourceType = z.infer<typeof ScoreSourceDomain>;
│
⋮
│export type ScoreDataTypeType = z.infer<typeof ScoreDataTypeDomain>;
│
⋮

packages/shared/src/domain/table-view-presets.ts:
⋮
│export enum TableViewPresetTableName {
│  Traces = "traces",
│  Observations = "observations",
│  ObservationsEvents = "observations-events",
│  Scores = "scores",
│  Sessions = "sessions",
│  SessionDetail = "session-detail",
│  Datasets = "datasets",
│  Experiments = "experiments",
│  ExperimentItems = "experiment-items",
⋮
│export enum SystemTableViewPresetCategory {
│  SlowCalls = "slow-calls",
│  Errors = "errors",
│  CostRegression = "cost-regression",
⋮
│export type TableViewPresetState = Pick<
│  TableViewPresetDomain,
│  "filters" | "columnOrder" | "columnVisibility" | "orderBy"
⋮

packages/shared/src/env.ts:
⋮
│export type SharedEnv = z.infer<typeof EnvSchema>;
│
⋮

packages/shared/src/errors/BaseError.ts:
│export class BaseError extends Error {
⋮
│  public isUserError(): boolean {
│    return this.httpCode >= 400 && this.httpCode < 500;
⋮

packages/shared/src/errors/ForbiddenError.ts:
⋮
│export class ForbiddenError extends BaseError {
│  constructor(description = "Forbidden") {
│    super("ForbiddenError", 403, description, true);
│  }
⋮

packages/shared/src/errors/InvalidRequestError.ts:
⋮
│export class InvalidRequestError extends BaseError {
│  constructor(description = "Invalid Request Error") {
│    super("InvalidRequestError", 400, description, true);
│  }
⋮

packages/shared/src/errors/NotFoundError.ts:
⋮
│export class LangfuseNotFoundError extends BaseError {
│  constructor(description = "Not Found") {
│    super("LangfuseNotFoundError", 404, description, true);
│  }
⋮

packages/shared/src/features/batchAction/types.ts:
⋮
│export type TraceDeleteBatchActionConfig = z.infer<
│  typeof TraceDeleteBatchActionConfigSchema
⋮

packages/shared/src/features/entitlements/plans.ts:
⋮
│export type Plan = keyof typeof planLabels;
│
⋮

packages/shared/src/features/evals/types.ts:
⋮
│export type EvalTargetObject =
⋮
│export type BatchEvalSourceTable =
⋮

packages/shared/src/features/monitors/scheduler/scheduler.ts:
⋮
│type FilterState = z.infer<typeof singleFilter>[];
│
⋮
│type PublishMonitorEvent = (event: MonitorQueueEventInput) => Promise<void>;
│
⋮
│type MonitorBatchResult = {
│  project_id: string;
│  scheduler_batch_id: bigint;
│  run_at: Date;
│  view: PrismaMonitorView;
│  filters: FilterState;
│  window_ms: bigint;
│  metrics: Metric[];
│  monitors: { monitorId: string; metricName: string }[];
⋮

packages/shared/src/features/monitors/scheduler/types.ts:
⋮
│export type MonitorQueueEventInput = z.input<typeof MonitorQueueEventSchema>;
│
⋮
│export type MonitorWebhookQueueEvent = z.infer<
│  typeof MonitorWebhookQueueEventSchema
⋮

packages/shared/src/features/monitors/service/types.ts:
⋮
│export class MonitorNotFoundError extends LangfuseNotFoundError {
│  constructor(monitorId: string, projectId: string) {
│    super(`Monitor ${monitorId} not found in project ${projectId}`);
│  }
⋮
│export type MonitorListOrderBy = z.infer<typeof MonitorListOrderBySchema>;
│
⋮
│export type ListMonitorSeverityFilter = z.infer<
│  typeof ListMonitorSeverityFilterSchema
⋮
│export type ListMonitorTagsFilter = z.infer<typeof ListMonitorTagsFilterSchema>;
│
⋮

packages/shared/src/features/monitors/types.ts:
⋮
│export type MonitorWindow = z.infer<typeof MonitorWindowSchema>;
│
⋮

packages/shared/src/features/prompts/parsePromptDependencyTags.ts:
⋮
│export function parsePromptDependencyTags(
│  content: string | object,
⋮

packages/shared/src/features/scores/interfaces/ui/types.ts:
⋮
│export type ScoreAggregate = Record<string, AggregatedScoreData>;
│
⋮

packages/shared/src/interfaces/orderBy.ts:
⋮
│export type OrderByState = z.infer<typeof orderBy>;
│
⋮

packages/shared/src/interfaces/search.ts:
⋮
│export type TracingSearchType = z.infer<typeof TracingSearchType>;

packages/shared/src/interfaces/tableNames.ts:
⋮
│export enum BatchTableNames {
│  Scores = "scores",
│  Sessions = "sessions",
│  Traces = "traces",
│  Observations = "observations",
│  Events = "events",
│  Datasets = "datasets",
│  DatasetRunItems = "dataset_run_items",
│  DatasetItems = "dataset_items",
│  AuditLogs = "audit_logs",
⋮

packages/shared/src/server/auth/types.ts:
⋮
│export type ApiAccessLevel = "organization" | "project" | "scores";
│
⋮
│export type ApiAccessScopeIngestion = BaseApiAccessScope &
⋮
│export type ApiAccessScope = BaseApiAccessScope & ApiAccessScopeMetadata;

packages/shared/src/server/cache/localCache.ts:
⋮
│export type LocalCacheConfig = {
│  namespace: string;
│  enabled: boolean;
│  ttlMs: number;
│  max: number;
⋮

packages/shared/src/server/clickhouse/client.ts:
⋮
│export type ClickhouseClientType = ReturnType<typeof createClient>;
│
│export type PreferredClickhouseService =
│  | "ReadWrite"
│  | "ReadOnly"
⋮
│type ServiceClickhouseSettings = ClickHouseSettings & {
│  enable_full_text_index?: 1;
⋮
│type RequestTimeoutClickHouseSettings = ClickHouseSettings & {
│  max_execution_time?: number;
│  timeout_before_checking_execution_speed?: number;
⋮
│export class ClickHouseClientManager {
│  private static instance: ClickHouseClientManager;
│  private clientMap: Map<string, ClickhouseClientType> = new Map();
│
│  /**
│   * Private constructor to enforce singleton pattern
│   */
│  private constructor() {}
│
│  /**
⋮

packages/shared/src/server/clickhouse/queryTags.ts:
⋮
│export type ClickHouseQueryTags = {
│  surface?: ClickHouseQuerySurface | (string & {});
│  route?: string;
│  projectId?: string;
⋮

packages/shared/src/server/evals/codeEvalDispatcherTypes.ts:
⋮
│export type DispatchInput = {
│  scope: CodeEvalScope;
│  runtime: { language: CodeEvalRuntimeLanguage };
│  execution: {
│    jobExecutionId: string;
│  };
│  code: {
│    source: string;
│  };
│  payload: CodeEvalPayload;
⋮
│export class CodeEvalDispatcherError extends Error {
│  public readonly code: CodeEvalDispatcherErrorCode;
│  public readonly retryable: boolean;
│  public readonly returnedResult?: unknown;
│
│  constructor(
│    message: string,
│    options: {
│      code: CodeEvalDispatcherErrorCode;
│      retryable?: boolean;
⋮

packages/shared/src/server/ingestion/ingestionAttribution.ts:
⋮
│export type IngestionAttribution = {
│  ingestionApiKey: string;
│  ingestionSdkName: string;
│  ingestionSdkVersion: string;
⋮

packages/shared/src/server/instrumentation/index.ts:
⋮
│export type TCarrier = {
│  traceparent?: string;
│  tracestate?: string;
⋮

packages/shared/src/server/llm/ai-sdk/providers/types.ts:
⋮
│export type TranslatedProviderOptions =
│  | { ok: true; value: Record<string, unknown> | undefined }
⋮

packages/shared/src/server/llm/baseUrlValidation.ts:
⋮
│export type LlmBaseUrlValidationWhitelist = OutboundUrlValidationWhitelist;
│
⋮

packages/shared/src/server/llm/internalTraceEvents.ts:
⋮
│export type InternalTraceExperimentContext = {
│  id: string;
│  name: string;
│  metadata?: Record<string, unknown>;
│  description?: string | null;
│  datasetId: string;
│  itemId: string;
│  itemVersion: string;
│  itemExpectedOutput?: unknown;
│  itemMetadata?: Record<string, unknown> | null;
⋮
│type InternalTraceSnapshot = {
│  spanId: string;
│  traceId: string;
│  parentSpanId?: string;
│  name?: string;
│  type: "SPAN" | "GENERATION";
│  environment?: string;
│  version?: string;
│  release?: string;
│  startTimeISO?: string;
⋮

packages/shared/src/server/llm/types.ts:
⋮
│export enum LLMAdapter {
│  Anthropic = "anthropic",
│  OpenAI = "openai",
│  Azure = "azure",
│  Bedrock = "bedrock",
│  VertexAI = "google-vertex-ai",
│  GoogleAIStudio = "google-ai-studio",
⋮
│type OpenAIReasoningMap = Record<OpenAIModel, boolean>;
⋮
│export type OpenAIModel = (typeof openAIModels)[number];
│
⋮
│export type ProcessedTraceEvent = {
│  type: string;
│  timestamp: string;
│  body: Record<string, unknown>;
⋮
│export type InternalTraceWriteInput = {
│  rootSpanId: string;
│  eventInputs: InternalTraceEventInput[];
⋮
│export type InternalTraceWriter = (
│  params: InternalTraceWriteInput,
⋮
│export type InternalEventsWriter = {
│  experimentContext?: InternalTraceExperimentContext;
│  write: InternalTraceWriter;
⋮

packages/shared/src/server/outbound-url/validation.ts:
⋮
│export interface OutboundUrlValidationWhitelist {
│  hosts: string[];
│  ips: string[];
│  ip_ranges: string[];
⋮
│export interface ValidateOutboundUrlHostOptions {
│  url: URL;
│  whitelist: OutboundUrlValidationWhitelist;
│  logContext: string;
│  shouldSkipDnsCheckForLiteralIps: boolean;
⋮
│interface ValidateOutboundResolvedIpOptions {
│  hostname: string;
│  ip: string;
│  whitelist: OutboundUrlValidationWhitelist;
│  logContext: string;
⋮

packages/shared/src/server/queries/clickhouse-sql/clickhouse-filter.ts:
⋮
│export type ClickhouseOperator =
│  | (typeof filterOperators)[keyof typeof filterOperators][number]
│  | "!="
⋮
│type ClickhouseFilter = {
│  query: string;
│  params: { [x: string]: any } | {};
⋮
│export class FilterList {
│  private filters: Filter[];
│
│  constructor(filters: Filter[] = []) {
│    this.filters = filters;
│  }
│
│  push(...filter: Filter[]) {
│    this.filters.push(...filter);
│  }
│
⋮

packages/shared/src/server/repositories/clickhouseExecExceptionTag.ts:
⋮
│export interface ClickhouseExecExceptionTagTransformOptions {
│  // `x-clickhouse-exception-tag` response header; undefined pre-25.11 → detection off.
│  exceptionTag: string | undefined;
│  // Lets the caller classify the error (e.g. ClickHouseResourceError). Identity
│  // by default, keeping this module free of server-only imports and unit-testable.
│  wrapError?: (error: Error) => Error;
⋮

packages/shared/src/server/repositories/comments.ts:
⋮
│export type CommentObjectType = "TRACE" | "OBSERVATION" | "SESSION" | "PROMPT";
│
⋮

packages/shared/src/server/services/DefaultViewService/types.ts:
⋮
│export type DefaultViewScope = z.infer<typeof DefaultViewScope>;
│
⋮

packages/shared/src/server/services/PromptService/types.ts:
⋮
│export type PromptReference = Pick<Prompt, "id" | "version" | "name">;
│
⋮

packages/shared/src/server/utils/rendering.ts:
⋮
│export interface RenderingProps {
│  /**
│   * Whether to truncate input/output fields to a specific character limit
│   */
│  truncated: boolean;
│
│  /**
│   * Whether to skip JSON parsing of input/output fields and return them as raw strings.
│   * This is useful when the client will handle JSON parsing to avoid double parsing.
│   */
⋮

packages/shared/src/tableDefinitions/types.ts:
│export type UiColumnMatchable = Readonly<{
⋮
│export type UiColumnMappings = readonly UiColumnMapping[];
│
⋮

packages/shared/src/types.ts:
⋮
│export type TimeFilter = z.infer<typeof timeFilter>;
│export type FilterCondition = z.infer<typeof singleFilter>;
│export type FilterState = FilterCondition[];
│export type EventsTableFilterCondition = z.infer<
│  typeof eventsTableSingleFilter
│>;
│export type EventsTableFilterState = z.infer<typeof eventsTableFilterState>;
│
⋮
│export type MakeOptional<T> = {
│  [K in keyof T]?: T[K];
⋮
│type AllowStringAsValue<T> = {
│  [K in keyof T]: K extends "value" ? string | T[K] : T[K];
⋮
│export type WipFilterCondition = AllowStringAsValue<
│  MakeOptional<FilterCondition>
│>;
│export type WipFilterState = WipFilterCondition[];
│
│export type FilterOption = {
│  value: string;
│  count?: number;
│  displayValue?: string; // FIX: Temporary workaround: Used to display a different value than the a
│  description?: string;
⋮
│export type TableName =
│  | "traces"
│  | "generations"
│  | "sessions"
│  | "scores"
│  | "prompts"
│  | "dashboard"
│  | "widgets"
│  | "users"
│  | "eval_configs"
⋮

packages/shared/src/utils/chatml/types.ts:
│export type NormalizerContext = {
⋮

packages/shared/src/utils/jsonSchemaValidation.ts:
⋮
│export type FieldValidationResult =
│  | {
│      isValid: true;
│    }
│  | {
│      isValid: false;
│      errors: FieldValidationError[];
⋮

web/src/__tests__/server/redis-test-utils.ts:
⋮
│export type RedisTestClient = NonNullable<
│  ReturnType<typeof createNewRedisInstance>
⋮

web/src/components/ItemBadge.tsx:
⋮
│export type LangfuseItemType =
│  | ObservationType
│  | "TRACE"
│  | "SESSION"
│  | "USER"
│  | "QUEUE_ITEM"
│  | "DATASET"
│  | "DATASET_RUN"
│  | "DATASET_ITEM"
│  | "ANNOTATION_QUEUE"
⋮

web/src/components/layouts/app-layout/utils/pathClassification.ts:
⋮
│export type PathClassification = {
│  /** Whether this is an auth page (sign-in, sign-up, etc.) */
│  isAuthPage: boolean;
│  /** Whether navigation should be hidden (public, onboarding, auth pages) */
│  hideNavigation: boolean;
│  /** Whether this path can be accessed without authentication (shared traces/sessions) */
│  isPublishable: boolean;
⋮

web/src/components/layouts/header.tsx:
⋮
│type HeaderProps = {
│  title: string;
│  status?: Status;
│  label?: {
│    text: string;
│    href: string;
│  };
│  help?: { description: string; href?: string; className?: string };
│  actionButtons?: React.ReactNode;
│  className?: string;
⋮

web/src/components/session/TraceEventsRow.tsx:
⋮
│type LazyTraceEventsRowProps = {
│  trace: RouterOutputs["sessions"]["tracesFromEvents"][number];
│  projectId: string;
│  sessionId: string;
│  openPeek: (id: string, row: any) => void;
│  index: number;
│  traceCommentCounts: Map<string, number> | undefined;
│  showCorrections: boolean;
│  filterState: FilterState;
│  /** Selected view's display name, for the empty-state notice (null = custom). */
⋮
│                    <NewDatasetItemFromTraceId
│                      projectId={projectId}
│                      traceId={trace.id}
│                      timestamp={new Date(trace.timestamp)}
⋮

web/src/components/session/TraceRow.tsx:
⋮
│type LazyTraceRowProps = {
│  trace: RouterOutputs["sessions"]["byIdWithScores"]["traces"][number];
│  projectId: string;
│  openPeek: (id: string, row: any) => void;
│  index: number;
│  traceCommentCounts: Map<string, number> | undefined;
⋮
│                <NewDatasetItemFromTraceId
│                  projectId={projectId}
│                  traceId={trace.id}
│                  timestamp={new Date(trace.timestamp)}
⋮

web/src/components/table/data-table-controls.clienttest.tsx:
⋮
│        <CategoricalFacet
│          label="Type"
│          filterKey="type"
│          expanded
│          loading={false}
│          options={[]}
│          counts={new Map()}
│          value={["AGENT"]}
│          onChange={() => {}}
│          isActive
│          isDisabled={false}
⋮
│        <CategoricalFacet
│          label="Type"
│          filterKey="type"
│          expanded
│          loading={false}
│          options={[]}
│          counts={new Map()}
│          value={["AGENT"]}
│          onChange={() => {}}
│          isActive
│          isDisabled={false}
⋮

web/src/components/table/peek/store/peekPanelStore.ts:
⋮
│export interface PeekPanelStoreState {
│  /** Committed widget width (persisted), as a fraction of the viewport. */
│  widthFraction: number;
│  /** Live widget width during a drag; null when not dragging or expanded. */
│  draftFraction: number | null;
│  /** True while a drag is previewing the expanded (max) width. */
│  draftExpanded: boolean;
│  /** True while the resize handle is being dragged. */
│  isResizing: boolean;
│  actions: {
⋮

web/src/components/table/types.ts:
⋮
│export type DataTableCellPadding = "compact" | "comfortable" | "none";
│
⋮

web/src/components/trace/components/IOPreview/hooks/useChatMLParser.ts:
⋮
│export interface ChatMLParserResult {
│  canDisplayAsChat: boolean;
│  allMessages: ChatMlMessage[];
│  additionalInput: Record<string, unknown> | undefined;
│  allTools: ToolDefinition[];
│  toolCallCounts: Map<string, number>;
│  toolCallsByName: Map<string, ToolCallInvocation[]>;
│  messageToToolCallNumbers: Map<number, number[]>;
│  toolNameToDefinitionNumber: Map<string, number>;
│  inputMessageCount: number;
⋮

web/src/components/trace/lib/types.ts:
⋮
│export type TreeNode = {
│  id: string;
│  type: "TRACE" | ObservationType;
│  name: string;
│  startTime: Date;
│  endTime?: Date | null;
│  level?: string;
│  children: TreeNode[];
│  // Token usage
│  inputUsage?: number | null;
⋮

web/src/components/ui/AdvancedJsonViewer/types.ts:
⋮
│export type JSONType =
│  | "string"
│  | "number"
│  | "boolean"
│  | "null"
│  | "undefined"
│  | "object"
⋮
│export type StringWrapMode = "nowrap" | "truncate" | "wrap";
│
⋮
│export interface FlatJSONRow {
│  /** Unique identifier for this row (dot-separated path: "root.users.0.name") */
│  id: string;
│
│  /** Nesting depth (0 = root) */
│  depth: number;
│
│  /** Property name or array index */
│  key: string | number;
│
⋮
│export type ExpansionState = Record<string, boolean> | boolean;
│
⋮
│export interface JSONTheme {
│  // Background colors
│  background: string;
│  foreground: string;
│
│  // Syntax colors
│  keyColor: string;
│  stringColor: string;
│  numberColor: string;
│  booleanColor: string;
⋮
│export interface SectionContext {
│  /** Section identifier */
│  sectionKey: string;
│
│  /** Number of visible JSON rows in this section */
│  rowCount: number;
│
│  /** Is section expanded? */
│  isExpanded: boolean;
│
⋮

web/src/components/ui/AdvancedJsonViewer/utils/treeStructure.ts:
⋮
│export interface TreeNode {
│  // Identity
│  id: string; // Full path as string (e.g., "root.users.0.name")
│  key: string | number; // Key in parent (e.g., "users", 0, "name")
│  pathArray: (string | number)[]; // Path as array (e.g., ["root", "users", 0, "name"])
│
│  // Value
│  value: unknown; // The actual JSON value
│  type:
│    | "null"
⋮

web/src/components/ui/MarkdownViewer.tsx:
⋮
│type ReactMarkdownNode = ReactMarkdownExtraProps["node"];
⋮
│type MarkdownAstNode = {
│  type: string;
│  value?: string;
│  url?: string;
│  children?: MarkdownAstNode[];
⋮

web/src/components/ui/chart.tsx:
⋮
│export type ChartConfig = {
│  [k in string]: {
│    label?: React.ReactNode;
│    icon?: React.ComponentType;
│  } & (
│    | { color?: string; theme?: never }
│    | { color?: never; theme: Record<keyof typeof THEMES, string> }
│  );
⋮

web/src/components/ui/dialog.tsx:
⋮
│type DialogOverlayMode = "subtle" | "invisible" | "blocking";
│
⋮

web/src/components/ui/layer.tsx:
⋮
│export type LayerName = (typeof LAYER_ORDER)[number];
│
⋮

web/src/components/ui/media/mediaUtils.ts:
⋮
│export type MediaDescriptor = NonNullable<
│  ReturnType<typeof classifyMediaValue>
⋮

web/src/components/ui/side-panel.tsx:
⋮
│  if (!showPanel) {
│    return (
│      <Button
│        variant="ghost"
│        size="icon"
│        onClick={() => setShowPanel(true)}
│        title="Show details"
│      >
│        <ChevronLeft className="h-4 w-4" />
│      </Button>
⋮

web/src/ee/features/in-app-agent/schema.ts:
⋮
│export type InAppAgentMessageSource = z.infer<
│  typeof InAppAgentMessageSourceSchema
⋮
│export type AgUiCustomEvent = AgUiEvent & {
│  type: EventType.CUSTOM;
│  name: string;
│  value: unknown;
⋮

web/src/features/annotation-queues/components/DeleteAnnotationQueueButton.tsx:
⋮
│type DeleteAnnotationQueueButtonProps = {
│  projectId: string;
│  queueId: string;
⋮

web/src/features/batch-exports/components/BatchExportsTable.tsx:
⋮
│        return (
│          <div className="flex items-center gap-2">
│            <span className="whitespace-break-spaces">{name}</span>
│            <TooltipProvider>
│              <Tooltip>
│                <TooltipTrigger>
│                  <InfoIcon className="text-muted-foreground size-3" />
│                </TooltipTrigger>
│                <TooltipContent>
│                  <div className="space-y-1">
│                    <div>Created: {new Date(createdAt).toLocaleString()}</div>
⋮

web/src/features/blobstorage-integration/types.ts:
⋮
│export type BlobStorageIntegrationFormSchema = z.infer<
│  typeof blobStorageIntegrationFormSchema
⋮

web/src/features/blobstorage-integration/validation.ts:
⋮
│export function exportStartDateNotInFuture(d: Date | null | undefined) {
│  return !d || d.getTime() <= Date.now() + MAX_EXPORT_START_DATE_FUTURE_MS;
⋮
│export function validateExportFieldGroups(
│  data: { exportFieldGroups: unknown[] },
│  ctx: z.RefinementCtx,
⋮
│export function validateAzureContainerName(
│  data: { type: string; bucketName: string },
│  ctx: z.RefinementCtx,
⋮

web/src/features/cloud-status-notification/types.ts:
⋮
│export type CloudStatus = z.infer<typeof CloudStatus>;

web/src/features/dashboard/components/EditDashboardDialog.tsx:
⋮
│interface EditDashboardDialogProps {
│  open: boolean;
│  onOpenChange: (open: boolean) => void;
│  projectId: string;
│  dashboardId: string;
│  initialName: string;
│  initialDescription: string;
⋮

web/src/features/datasets/lib/csv/types.ts:
⋮
│export type FieldMapping = FreeformField | SchemaField;
│
⋮
│export type ColumnType =
│  | "string"
│  | "number"
│  | "boolean"
│  | "null"
│  | "json"
│  | "array"
│  | "unknown"
⋮
│type RowProcessor = {
│  onHeader?: (headers: string[]) => void | Promise<void>;
│  onRow?: (
│    row: string[],
│    headers: string[],
│    index: number,
│  ) => void | Promise<void>;
⋮

web/src/features/datasets/store/datasetsTableStore.ts:
⋮
│export type DatasetsTableStore = StoreApi<DatasetsTableStoreState>;
│
⋮

web/src/features/entitlements/constants/entitlements.ts:
⋮
│export type EntitlementLimits = Record<
│  EntitlementLimit,
│  | number // if limited
│  | false // unlimited
⋮

web/src/features/evals/hooks/useEvalCapabilities.ts:
⋮
│export interface EvalCapabilities {
│  isNewCompatible: boolean;
│  compatibilityCheckWasPerformed: boolean;
│  allowLegacy: boolean;
│  allowPropagationFilters: boolean;
│  isLoading: boolean;
│  hasLegacyEvals: boolean;
⋮

web/src/features/evals/utils/code-eval-template-starter-examples.ts:
⋮
│export type CodeEvalSourceCodeLanguage = "PYTHON" | "TYPESCRIPT";
│
⋮

web/src/features/events/hooks/useV4Beta.ts:
⋮
│type SetV4EnabledOptions = {
│  onSuccess?: () => void | Promise<void>;
⋮

web/src/features/events/server/eventsService.ts:
⋮
│type TimeFilter = z.infer<typeof timeFilter>;
│
⋮

web/src/features/experiments/store/experimentsTableStore.ts:
⋮
│type RowSelectionUpdater = Updater<RowSelectionState>;
⋮

web/src/features/experiments/types/charts.ts:
⋮
│export type ScoreLevel = "obs" | "experiment";
│export type ScoreChartDataType = "numeric" | "categorical";
│
⋮

web/src/features/feature-flags/types.ts:
⋮
│export type Flag = (typeof availableFlags)[number];
│export type Flags = {
│  [key in (typeof availableFlags)[number]]: boolean;
⋮

web/src/features/filters/lib/filter-config.ts:
⋮
│interface CategoricalFacet extends BaseFacet {
│  type: "categorical";
│  /** Optional function to render an icon next to filter option labels */
│  renderIcon?: (value: string) => React.ReactNode;
│  /** When true, the sidebar hides the contains/does-not-contain text filter mode for this facet. *
│  disableTextFilter?: boolean;
⋮
│export type FilterStateMigration = (filters: FilterState) => FilterState;
│
│export interface FilterConfig {
│  tableName: string;
│  columnDefinitions: ColumnDefinition[];
│  defaultExpanded?: string[];
│  defaultSidebarCollapsed?: boolean;
│  facets: Facet[];
│  /** Runs after display-name normalization and before filter validation. */
│  migrateFilterState?: FilterStateMigration;
⋮

web/src/features/mcp/features/observations/tools/getObservationFilterValues.ts:
⋮
│type FilterValueColumn = z.infer<typeof FilterValueColumnSchema>;
│
⋮
│type FilterOption = {
│  value: string | boolean;
│  count?: number;
⋮

web/src/features/mcp/server/bootstrap.ts:
⋮
│export type McpToolName = McpFeature["tools"][number]["definition"]["name"];
│
⋮

web/src/features/mcp/types.ts:
⋮
│export interface ServerContext {
│  /**
│   * Project ID from authenticated API key
│   * MCP requires project-scoped access only (never null)
│   */
│  projectId: string;
│
│  /** Organization ID from authenticated API key */
│  orgId: string;
│
⋮
│export type InAppAgentContext =
│  | {
│      permissions: "read";
│    }
│  | {
│      permissions: "single-tool-override";
│      allowedToolName: McpToolName;
⋮

web/src/features/navigate-detail-pages/context.tsx:
⋮
│interface ListContextType {
│  detailPagelists: Record<string, Array<ListEntry>>;
│  setDetailPageList: <TEntry extends ListEntry>(
│    key: string,
│    list: Array<TEntry>,
│  ) => void;
⋮

web/src/features/onboarding/lib/surveyTypes.ts:
│export interface SurveyFormData {
⋮

web/src/features/prompts/components/PromptSelectionDialog.tsx:
⋮
│type PromptSelectionDialogProps = {
│  isOpen: boolean;
│  onClose: () => void;
│  onSelect?: (tag: string) => void;
│  projectId: string;
⋮

web/src/features/prompts/components/ProtectedLabelsSettings.tsx:
⋮
│type AddLabelFormSchemaType = z.infer<typeof AddLabelFormSchema>;
│
⋮

web/src/features/public-api/components/ApiKeyCreateDialogContent.tsx:
⋮
│type ApiKeyScope = "project" | "organization";
│
⋮

web/src/features/public-api/components/ApiKeyDetailContent.tsx:
⋮
│type ApiKeyScope = "project" | "organization";
│
⋮

web/src/features/public-api/components/ApiKeyList.tsx:
⋮
│type ApiKeyScope = "project" | "organization";
⋮

web/src/features/public-api/components/CreateApiKeyButton.tsx:
⋮
│type ApiKeyScope = "project" | "organization";
│
⋮

web/src/features/public-api/server/apiAuth.ts:
⋮
│export class ApiAuthService {
│  prisma: PrismaClient;
│  redis: Redis | Cluster | null;
│
│  constructor(prisma: PrismaClient, redis: Redis | Cluster | null) {
│    this.prisma = prisma;
│    this.redis = redis;
│  }
│
│  // this function needs to be called, when the organisation is updated
⋮

web/src/features/public-api/types/unstable-public-evals-contract.ts:
⋮
│type SupportedFilterFactory = keyof typeof filterSchemaFactories;
│
⋮

web/src/features/rbac/components/RoleSelectItem.tsx:
⋮
│            {formatRole(role)}
⋮
│          ) : (
│            <>
│              <div className="font-bold">Role: {formatRole(role)}</div>
│              <p className="mt-2 text-xs font-semibold">Organization Scopes</p>
│              <ul className="list-inside list-disc text-xs">{orgScopes}</ul>
│              <p className="mt-2 text-xs font-semibold">Project Scopes</p>
│              <ul className="list-inside list-disc text-xs">{projectScopes}</ul>
│              <p className="mt-2 border-t pt-2 text-xs">
│                Note:{" "}
│                <span className="text-muted-foreground">Muted scopes</span> are
⋮

web/src/features/rbac/constants/organizationAccessRights.ts:
⋮
│export type OrganizationScope = (typeof organizationScopes)[number];
│
⋮

web/src/features/rbac/constants/projectAccessRights.ts:
⋮
│export type ProjectScope = (typeof projectScopes)[number];
│
⋮

web/src/features/score-analytics/lib/statistics-utils.ts:
⋮
│export interface InterpretationResult {
│  strength: string;
│  color: string;
│  description: string;
⋮

web/src/features/scores/components/multi-select-key-values.tsx:
⋮
│type MultiSelectOptions = {
│  value: string;
│  key?: string;
│  count?: number;
│  disabled?: boolean;
│  isArchived?: boolean;
⋮

web/src/features/search-bar/lib/ast.ts:
⋮
│export type CompareOp =
│  | "="
│  | "exact"
│  | "~"
│  | "^"
│  | "$"
│  | ">"
│  | "<"
│  | ">="
⋮

web/src/features/search-bar/lib/fields.ts:
⋮
│export type FieldRef =
│  | { type: "field"; field: FieldDef }
│  | { type: "metadata"; key: string }
│  | { type: "scores"; key: string; level: "observation" | "trace" }
⋮
│function label(op: CompareOp): string {
│  return OP_LABEL[op] ?? op;
⋮

web/src/features/slack/components/SlackConnectionCard.tsx:
⋮
│interface SlackConnectionCardProps {
│  /** Project ID for the Slack integration */
│  projectId: string;
│  /** Whether the component is disabled */
│  disabled?: boolean;
│  /** Optional callback when connection status changes */
│  onConnectionChange?: (connected: boolean) => void;
│  /** Whether to show the connect button in the card */
│  showConnectButton?: boolean;
⋮

web/src/features/trace-graph-view/components/ElkGraphRenderer.tsx:
⋮
│type Transform = { x: number; y: number; k: number };
│
⋮

web/src/features/trace-graph-view/types.ts:
⋮
│export type GraphCanvasData = {
│  nodes: GraphNodeData[];
│  edges: { from: string; to: string }[];
⋮

web/src/features/web-callouts/components/WebCalloutSettingsPage.tsx:
⋮
│type WebCalloutEndpoint = RouterOutputs["webCallouts"]["all"][number];
│
⋮

web/src/features/widgets/components/WidgetForm.tsx:
⋮
│type ChartConfig = WidgetChartConfig;
│
⋮

web/src/pages/organization/[organizationId]/settings/index.tsx:
⋮
│const OrgSettingsPage = () => {
│  const organization = useQueryOrganization();
│  const router = useRouter();
⋮

web/src/pages/project/[projectId]/settings/integrations/blobstorage.tsx:
⋮
│                  <>
│                    <br />
│                    <span className="text-xs opacity-70">
│                      {new Date(state.data.config.lastErrorAt).toLocaleString()}
⋮

web/src/server/utils/cookies.ts:
⋮
│export type ProjectCookie = {
│  origin: string;
│  projectId: string;
⋮

web/src/utils/clientSideDomainTypes.ts:
⋮
│export type MetadataDomainClient = string | null;
│
⋮

web/src/utils/date-range-utils.ts:
⋮
│export type TimeRange = RelativeTimeRange | AbsoluteTimeRange;
│
⋮
│export type IntervalConfig = {
│  count: number;
│  unit: IntervalUnit;
⋮

web/src/workers/json-parser.worker.ts:
⋮
│export interface ParseResponse {
│  id: string;
│  parsedInput: unknown;
│  parsedOutput: unknown;
│  parsedMetadata: unknown;
│  parseTime: number;
⋮

web/types/next-auth.d.ts:
⋮
│declare module "next-auth" {
│  interface Session extends DefaultSession {
│    user: User | null; // null if user does not exist anymore in the database but has active jwt
│    environment: {
│      // Run-time environment variables that need to be available client-side
│      enableExperimentalFeatures: boolean;
│      // Enables features that are only available under an enterprise/commercial license when self-
│      selfHostedInstancePlan: Plan | null;
│      // V4 migration write mode. Mirrors LANGFUSE_MIGRATION_V4_WRITE_MODE so the
│      // client can tell whether the legacy traces/observations tables are still
│      // written and gate the V4 preview / legacy experiences accordingly.
⋮

worker/src/__tests__/periodicRunner.test.ts:
⋮
│class TestRunner extends PeriodicRunner {
│  public callCount = 0;
│  public shouldThrow = false;
│  public returnInterval: number | undefined = undefined;
│
│  protected get name(): string {
│    return "test-runner";
│  }
│
│  protected get defaultIntervalMs(): number {
⋮

worker/src/features/batch-trace-deletion-cleaner/index.ts:
⋮
│type TraceDeletionBackend = "postgres" | "clickhouse";
⋮

worker/src/features/blobstorage/byteCounters.ts:
⋮
│export type TimedByteCounterStats = {
│  sourceWaitMs: number;
│  backpressureMs: number;
⋮

worker/src/features/blobstorage/gzipStream.ts:
⋮
│export type GzipStats = {
│  level: number;
│  // Wall-clock time from handing a chunk to zlib until the write callback fires.
│  // Includes both compression CPU and downstream backpressure pauses.
│  activeMs: number;
│  // Time spent waiting for the downstream consumer (S3 upload) to drain.
│  // Measured independently as the gap between push() returning false
│  // (gzip.pause()) and the next _read() call (gzip.resume()).
│  // Pure gzip CPU ≈ max(0, activeMs - backpressureMs).
│  backpressureMs: number;
⋮

worker/src/features/queue-metrics-runner/index.ts:
⋮
│type DepthType = "waiting" | "failed" | "active";
│
│async function collectDepth(
│  queue: Queue,
⋮
│function emitDepth(
│  metricBase: string,
│  depths: Record<DepthType, number>,
│  tags?: Record<string, string>,
⋮
│export class QueueMetricsRunner extends PeriodicRunner {
│  protected get name(): string {
│    return "queue-metrics-runner";
│  }
│
│  protected get defaultIntervalMs(): number {
│    return env.LANGFUSE_QUEUE_METRICS_INTERVAL_MS;
│  }
│
│  protected async execute(): Promise<void> {
⋮

worker/src/features/tokenisation/usage.ts:
⋮
│interface Tokenizer {
│  [model: string]: Tiktoken;
⋮

worker/src/interfaces/MessageResponse.ts:
│export default interface MessageResponse {
⋮

worker/src/services/ClickhouseWriter/index.ts:
⋮
│export class ClickhouseWriter {
│  private static instance: ClickhouseWriter | null = null;
│  private static client: ClickhouseClientType | null = null;
│  batchSize: number;
│  writeInterval: number;
│  maxAttempts: number;
│  queue: ClickhouseQueue;
│
│  isIntervalFlushInProgress: boolean;
│  intervalId: NodeJS.Timeout | null = null;
│
⋮
│export enum TableName {
│  Traces = "traces",
│  TracesNull = "traces_null",
│  Scores = "scores",
│  Observations = "observations",
│  ObservationsBatchStaging = "observations_batch_staging",
│  BlobStorageFileLog = "blob_storage_file_log",
│  DatasetRunItems = "dataset_run_items_rmt",
│  EventsFull = "events_full", // Primary write target - MV auto-populates events_core
⋮
│type ClickhouseQueue = {
│  [T in TableName]: ClickhouseWriterQueueItem<T>[];
⋮

worker/src/utils/PeriodicExclusiveRunner.ts:
⋮
│export abstract class PeriodicExclusiveRunner extends PeriodicRunner {
│  protected readonly instanceName: string;
│  protected readonly lock: RedisLock;
│
│  constructor(params: {
│    name: string;
│    lockKey: string;
│    lockTtlSeconds: number;
│    onUnavailable?: OnUnavailableBehavior;
│  }) {
⋮
│  protected get name(): string {
│    return this.instanceName;
⋮

worker/src/utils/PeriodicRunner.ts:
⋮
│export abstract class PeriodicRunner {
│  private timeoutId: NodeJS.Timeout | null = null;
│  private isRunning = false;
│
│  protected abstract get name(): string;
│  protected abstract get defaultIntervalMs(): number;
│  protected abstract execute(): Promise<number | void>;
│
│  public start(): void {
│    if (this.isRunning) {
⋮

worker/src/utils/RedisLock.ts:
⋮
│export type OnUnavailableBehavior = "proceed" | "fail";
│
⋮
│export class RedisLock {
│  private readonly lockKey: string;
│  private readonly lockValue: string;
│  private readonly ttlSeconds: number;
│  private readonly name: string;
│  private readonly onUnavailable: OnUnavailableBehavior;
│
│  // Lua script for atomic check-and-delete (only delete if we own the lock)
│  private static readonly RELEASE_LOCK_SCRIPT = `
│    if redis.call("get", KEYS[1]) == ARGV[1] then
⋮
│  public get key(): string {
│    return this.lockKey;
⋮
```

### AST Map: `modules/langfuse-docs`

```python
app/(home)/page.tsx:
⋮
│export default function HomePage() {
│  return <Home />;
⋮

app/[section]/layout.tsx:
⋮
│type LayoutProps = {
│  children: React.ReactNode;
│  params: Promise<{ section: string }>;
⋮

app/changelog/page.tsx:
⋮
│type PageProps = {
│  searchParams: Promise<{ page?: string }>;
⋮

app/guides/[[...slug]]/page.tsx:
⋮
│type PageProps = {
│  params: Promise<{ slug?: string[] }>;
⋮

app/japan/layout.tsx:
⋮
│export default function JapanLayout({ children }: { children: ReactNode }) {
│  return (
│    <HomeLayout
│      showAside={false}
│      footerClassName="md:max-w-none xl:max-w-none px-4 sm:px-6 md:px-8"
│    >
│      {children}
│    </HomeLayout>
│  );
⋮

app/japan/page.tsx:
⋮
│export default function JapanPage() {
│  return <JapanLanding />;
⋮

app/launch-week-5/layout.tsx:
⋮
│export default function LaunchWeek5Layout({
│  children,
⋮

app/launch-week-5/page.tsx:
⋮
│export default function LaunchWeek5Page() {
│  return <LaunchWeek5Landing />;
⋮

app/layout.tsx:
⋮
│export default function RootLayout({
│  children,
⋮

components/AppRootProvider.tsx:
⋮
│export function AppRootProvider({
│  children,
│  theme,
│  ...props
⋮

components/Authors.tsx:
⋮
│export type Author = {
│  firstName: string;
│  name: string;
│  title: string;
│  image: string;
│  twitter?: string;
│  github?: string;
│  linkedin?: string;
⋮

components/Availability.tsx:
⋮
│export function AvailabilityBanner(props: {
│  availability: Record<
│    (typeof plans)[number]["id"],
│    (typeof availabilities)[number]["id"]
│  >;
⋮

components/BrandAssets.tsx:
⋮
│type BrandAssetVariant = "light" | "dark";
│
│interface BrandAssetCardProps {
│  src: string;
│  alt: string;
│  label: string;
│  variant?: BrandAssetVariant;
│  tall?: boolean;
⋮

components/BrokenLinkIssue.tsx:
⋮
│export function BrokenLinkIssue() {
│  const [href, setHref] = useState<string>(
│    `https://github.com/${REPO}/issues/new`,
│  );
│
│  useEffect(() => {
│    const path = window.location.pathname;
│    const title = encodeURIComponent(`Broken link: ${path}`);
│    const body = encodeURIComponent(
│      `The following page returned a 404:\n\n**URL:** \`${window.location.href}\`\n\nPlease update 
⋮

components/CTACard.tsx:
⋮
│interface CTACardProps {
│  title: string;
│  description: string;
│  children?: React.ReactNode;
│  className?: string;
│  showArrow?: boolean;
⋮

components/CursorLangfuseReadme.tsx:
⋮
│export function CursorLangfuseReadme() {
│  const [content, setContent] = useState<string | null>(null);
│  const [error, setError] = useState(false);
│
│  useEffect(() => {
│    fetch(
│      "https://raw.githubusercontent.com/naoufalelh/cursor-langfuse/refs/heads/main/README.md",
│    )
│      .then((r) => {
│        if (!r.ok) throw new Error(`HTTP ${r.status}`);
⋮

components/DocBodyChrome.tsx:
⋮
│type Props = {
│  children: ReactNode;
│  lang?: string;
│  /**
│   * When false, renders a plain flex-1 div without prose chrome.
│   * Used by wide/marketing sections (pricing, etc.).
│   */
│  withProse?: boolean;
│  /**
│   * Optional version label (e.g. "Version: v3") shown next to the copy button.
⋮

components/FetchReadme.tsx:
⋮
│export function FetchReadme({ url }: { url: string }) {
│  const [content, setContent] = useState<string | null>(null);
│  const [error, setError] = useState<string | null>(null);
│
│  useEffect(() => {
│    fetch(url)
│      .then((res) =>
│        res.ok ? res.text() : Promise.reject(new Error(res.statusText)),
│      )
│      .then(setContent)
⋮

components/Frame.tsx:
⋮
│export const Frame = ({
│  children,
│  className,
│  fullWidth = false,
│  transparent = false,
⋮
│}) => {
⋮
│  return (
│    <>
│      <div
│        ref={frameRef}
│        className={cn(
│          "mt-4 border rounded inline-block overflow-hidden",
│          className,
│        )}
│      >
│        <div
⋮
│        <ImageZoomModal
│          src={zoomedImage.src}
│          alt={zoomedImage.alt}
│          onClose={() => setZoomedImage(null)}
⋮

components/GitHubReadme.tsx:
⋮
│export function GitHubReadme({ url }: { url: string }) {
│  const [content, setContent] = useState<string | null>(null);
│  const [error, setError] = useState(false);
│
│  useEffect(() => {
│    fetch(url)
│      .then((r) => {
│        if (!r.ok) throw new Error(`HTTP ${r.status}`);
│        return r.text();
│      })
⋮

components/PageFooterNav.tsx:
⋮
│export type PageFooterNavItem = {
│  name: string;
│  description?: string;
│  url: string;
⋮

components/PropagationRestrictionsCallout.tsx:
⋮
│interface PropagationRestrictionsCalloutProps {
│  attributes?: (
│    | "userId"
│    | "sessionId"
│    | "metadata"
│    | "version"
│    | "tags"
│    | "traceName"
│  )[];
⋮

components/RenderedReadmeContent.tsx:
⋮
│export function RenderedReadmeContent({ content }: { content: string }) {
│  return (
│    <div className="[&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
│      <ReactMarkdown remarkPlugins={[remarkGfm]} components={readmeComponents}>
│        {content}
│      </ReactMarkdown>
│    </div>
│  );
⋮

components/TocCommunity.tsx:
⋮
│type TocCommunityProps = {
│  className?: string;
⋮

components/academy/ErrorAnalysisProcessDiagram.tsx:
⋮
│function estimateInitialScale(): number {
│  if (typeof window === "undefined") return 0.65;
│  const vw = document.documentElement.clientWidth;
│  return Math.min(1, Math.max(0.3, (vw - 32) / INNER_W));
⋮

components/academy/EvaluatorBlock.tsx:
⋮
│export interface EvaluatorBlockEvaluator {
│  name: string;
│  /** "LLM-as-a-judge" | "Code" | "Human" */
│  type: string;
│  /** The one-line check, shown in the collapsed row. */
│  check?: React.ReactNode;
│  /** Score output, e.g. "binary, on the trace". Shown with the type in the expanded meta line. */
│  returns?: string;
│  /**
│   * Narrative shown when the row is expanded: why it is this type of
⋮

components/academy/LoopDiagram.tsx:
⋮
│function estimateInitialScale(): number {
│  if (typeof window === "undefined") return 0.56;
│  const vw = document.documentElement.clientWidth;
│  if (vw < 768) {
│    return Math.max(0.25, (vw - 32) / INNER_W);
│  }
│  return 0.56;
⋮

components/academy/TraceViewDiagram.tsx:
│export interface TraceViewRow {
⋮

components/academy/japan/AgentPromptCallout.tsx:
⋮
│export interface AgentPromptCalloutProps {
│  /** Ribbon label, e.g. "Run with your agent". */
│  ribbon?: string;
│  /** Title shown above the lede. */
│  title?: string;
│  /** Lede paragraph beneath the title. */
│  lede?: React.ReactNode;
│  /** The exact text written to the clipboard. */
│  prompt: string;
⋮

components/academy/japan/ErrorAnalysisProcessDiagram.tsx:
⋮
│function estimateInitialScale(): number {
│  if (typeof window === "undefined") return 0.65;
│  const vw = document.documentElement.clientWidth;
│  return Math.min(1, Math.max(0.3, (vw - 32) / INNER_W));
⋮

components/academy/japan/LoopDiagram.tsx:
⋮
│function estimateInitialScale(): number {
│  if (typeof window === "undefined") return 0.56;
│  const vw = document.documentElement.clientWidth;
│  if (vw < 768) {
│    return Math.max(0.25, (vw - 32) / INNER_W);
│  }
│  return 0.56;
⋮

components/academy/japan/ManualGuideCallout.tsx:
⋮
│export interface ManualGuideCalloutProps {
│  /** Where the card links to (cookbook URL or similar). */
│  href: string;
│  /** Topic shown in the ribbon after the static "Guide:" prefix, e.g. "error analysis". */
│  topic: string;
│  /** Lede paragraph beneath the ribbon. */
│  lede?: React.ReactNode;
│  /** CTA button text, default "Open the guide". */
│  cta?: string;
⋮

components/ai-elements/code-block.tsx:
⋮
│export type CodeBlockProps = HTMLAttributes<HTMLDivElement> & {
│  code: string;
│  language: string;
│  showLineNumbers?: boolean;
│  children?: ReactNode;
│  customStyle?: React.CSSProperties;
⋮

components/ai-elements/conversation.tsx:
⋮
│export type ConversationProps = ComponentProps<typeof StickToBottom>;
│
⋮

components/ai-elements/image.tsx:
⋮
│export type ImageProps = Experimental_GeneratedImage & {
│  className?: string;
│  alt?: string;
⋮

components/ai-elements/message.tsx:
⋮
│export type MessageProps = HTMLAttributes<HTMLDivElement> & {
│  from: UIMessage["role"];
⋮

components/ai-elements/response.tsx:
⋮
│export type ResponseProps = HTMLAttributes<HTMLDivElement> & {
│  options?: Options;
│  children: Options["children"];
│  allowedImagePrefixes?: ComponentProps<
│    ReturnType<typeof hardenReactMarkdown>
│  >["allowedImagePrefixes"];
│  allowedLinkPrefixes?: ComponentProps<
│    ReturnType<typeof hardenReactMarkdown>
│  >["allowedLinkPrefixes"];
│  defaultOrigin?: ComponentProps<
⋮

components/analytics/ConversionTracker.tsx:
⋮
│export function ConversionTracker() {
│  useEffect(() => {
│    // Capture phase runs before button onClick handlers, so CTAs that
│    // preventDefault to navigate programmatically are still tracked.
│    const handler = (event: MouseEvent) => {
│      const target = event.target as Element | null;
│      if (!target?.closest(LAUNCH_APP_CTA_SELECTOR)) return;
│      reportLaunchAppConversion();
│    };
│
⋮

components/analytics/ahrefs.tsx:
⋮
│export function AhrefsAnalytics() {
│  return (
│    <Script
│      id="ahrefs-analytics"
│      src="https://analytics.ahrefs.com/analytics.js"
│      data-key={AHREFS_ANALYTICS_KEY}
│      strategy="afterInteractive"
│    />
│  );
⋮

components/analytics/common-room.tsx:
⋮
│export function CommonRoom() {
│  return (
│    <Script id="common-room" strategy="afterInteractive">
│      {`(function() {
│  if (typeof window === 'undefined') return;
│  if (typeof window.signals !== 'undefined') return;
│  var script = document.createElement('script');
│  script.src = 'https://cdn.cr-relay.com/v1/site/${COMMON_ROOM_SITE_ID}/signals.js';
│  script.async = true;
│  window.signals = Object.assign(
⋮

components/analytics/google-ads.tsx:
⋮
│export function GoogleAds() {
│  return (
│    <>
│      <Script
│        id="google-ads-gtag"
│        src={`https://www.googletagmanager.com/gtag/js?id=${GOOGLE_ADS_ID}`}
│        strategy="afterInteractive"
│      />
│      <Script id="google-ads-init" strategy="afterInteractive">
│        {`
⋮

components/analytics/linkedin-ads.tsx:
⋮
│export function LinkedInInsightTag() {
│  if (!isLinkedInEnabled) return null;
│
│  return (
│    <>
│      <Script id="linkedin-partner-id" strategy="afterInteractive">
│        {`_linkedin_partner_id = "${LINKEDIN_PARTNER_ID}";
│window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
│window._linkedin_data_partner_ids.push(_linkedin_partner_id);`}
│      </Script>
⋮

components/analytics/reddit-ads.tsx:
⋮
│export function RedditPixel() {
│  if (!isRedditEnabled) return null;
│
│  return (
│    <Script id="reddit-pixel" strategy="afterInteractive">
│      {`!function(w,d){if(!w.rdt){var p=w.rdt=function(){p.sendEvent?p.sendEvent.apply(p,arguments)
│    </Script>
│  );
⋮

components/analytics/scarf.tsx:
⋮
│export function ScarfPixel() {
│  const pathname = usePathname();
│
│  useEffect(() => {
│    if (typeof window === "undefined" || !pathname) return;
│
│    const pixel = new Image();
│    pixel.referrerPolicy = "no-referrer-when-downgrade";
│    pixel.src = `https://static.scarf.sh/a.png?x-pxid=${SCARF_PIXEL_ID}`;
│  }, [pathname]);
│
⋮

components/analytics/twitter-ads.tsx:
⋮
│export function TwitterPixel() {
│  if (!isTwitterEnabled) return null;
│
│  return (
│    <Script id="twitter-pixel" strategy="afterInteractive">
│      {`!function(e,t,n,s,u,a){e.twq||(s=e.twq=function(){s.exe?s.exe.apply(s,arguments):s.queue.pu
│    </Script>
│  );
⋮

components/blog/BlogFilterContext.tsx:
⋮
│type BlogFilterState = {
│  selectedTag: string | null;
│  searchQuery: string;
│  setSelectedTag: (tag: string | null) => void;
│  setSearchQuery: (q: string) => void;
│  tags: TagWithCount[];
│  allPosts: BlogPageItem[];
│  filteredPosts: BlogPageItem[];
│  highlightPosts: BlogPageItem[];
│  listPosts: BlogPageItem[];
⋮
│export function BlogFilterProvider({
│  pages,
│  children,
⋮

components/blog/BlogPageClient.tsx:
⋮
│export function BlogPageClient({
│  pages,
│  children,
⋮

components/careers/PolaroidFrame.tsx:
⋮
│export type PolaroidFrameProps = {
│  /** Image URL (local `/images/...` or remote). */
│  src: string;
│  /** Accessible description. Defaults to the caption (description, or location + year). */
│  alt?: string;
│  /** Handwritten-style caption (F37 Analog). Renders a muted placeholder when empty. */
│  description?: string;
│  /** Location shown as a small label next to the date, e.g. "Berlin". */
│  location?: string;
│  /** Year or date caption (Geist Mono). Renders a dashed blank line when empty. */
⋮

components/careers/careers-polaroids.ts:
⋮
│export type OrderedPolaroidGallery = {
│  /** "Langfuse is born" — always first. */
│  anchor: CareersPolaroid;
│  /** Most recent photo by date — shown beside the anchor when distinct. */
│  newest: CareersPolaroid | null;
│  /** Remaining photos, newest-first. */
│  rest: CareersPolaroid[];
⋮

components/customers/CustomerCarousel.tsx:
⋮
│interface CustomerCarouselProps {
│  stories: CustomerStory[];
│  title?: string;
│  description?: string;
│  showDots?: boolean;
│  loop?: boolean;
│  className?: string;
⋮

components/customers/CustomerQuote.tsx:
⋮
│interface CustomerQuoteProps {
│  quote: string;
│  name: string;
│  role: string;
│  company?: string;
│  image?: string;
│  className?: string;
⋮

components/demoTabs/index.tsx:
⋮
│type DemoTabsProps = HTMLAttributes<HTMLDivElement>;
│
⋮

components/docs-sidebar/SidebarFolderItem.tsx:
⋮
│export function sidebarNavPaddingInlineStart(depth: number) {
│  return `calc(${2 * depth} * var(--spacing) + 6px)`;
⋮
│function SidebarFolderBody({ children }: { children: ReactNode }) {
│  const depth = useFolderDepth();
│  return (
│    <SidebarFolderContent
│      className={cn(
│        "relative",
│        depth === 1 &&
│          "before:absolute before:inset-y-1 before:start-3 before:w-px before:bg-[var(--line-struct
│      )}
│      style={{
⋮

components/docs-sidebar/SidebarItem.tsx:
⋮
│export function SidebarItem({
│  item,
⋮

components/docs/cards.tsx:
⋮
│interface CardsProps extends React.HTMLAttributes<HTMLDivElement> {
│  /** Number of columns (1 | 2 | 3). Defaults to 2. */
│  num?: number;
│  className?: string;
│  children?: React.ReactNode;
⋮
│export type CardProps = Omit<FumadocsCardProps, "title"> & {
│  title?: React.ReactNode;
│  contentClassName?: string;
│  contentWrapperClassName?: string;
│  /** Legacy prop — ignored, fumadocs renders its own arrow. */
│  arrow?: boolean;
⋮

components/docs/playground.tsx:
⋮
│export function Playground({ source }: { source: string }) {
│  return (
│    <pre className="p-4 overflow-auto rounded-lg border bg-muted/50 text-sm max-h-[70vh]">
│      <code>{source}</code>
│    </pre>
│  );
⋮

components/faq/FaqPreview.tsx:
⋮
│          <li
│            className="my-2"
│            id={page.url.replace("/faq/all/", "")}
│            key={page.url.replace("/faq/all/", "")}
⋮

components/gh-discussions/GhDiscussionsPreviewInternal.tsx:
⋮
│type SortType = "upvotes" | "recent";
│
⋮

components/home/AllTheTools.tsx:
⋮
│type ToolEntry = {
│  title: string;
│  description: string;
│  href: string;
│  tooltip: string;
│  span: string;
│  visual: StaticImageData;
⋮

components/home/FeatureTabsSection.tsx:
⋮
│export function FeatureTabsSection() {
│  return (
│    <HomeSection id="overview" className="pt-[120px]">
│      <div className="flex items-start mb-6 md:hidden">
│        <Heading className="text-left">
│          Gain{" "}
│          <TextHighlight className="whitespace-nowrap">
│            deep visibility
│          </TextHighlight>{" "}
│          into your traces
⋮

components/home/GetStartedSection.tsx:
⋮
│type LangId = keyof typeof MANUAL_SNIPPETS;
│
⋮

components/home/HeroStatsStrip.tsx:
⋮
│function StatItems() {
│  return (
│    <>
│      <Text size="s" className="whitespace-nowrap shrink-0">
│        Used by <b className="text-primary">19</b> of Fortune 50
│      </Text>
│      <Dot />
│      <Text size="s" className="whitespace-nowrap shrink-0">
│        <b className="text-primary">10+ billion</b> observations/month
│      </Text>
⋮

components/home/HomeSection.tsx:
⋮
│        else if (ref)
⋮

components/home/RiveSection.tsx:
⋮
│type RiveLabel = {
│  heading: string;
│  body: string;
⋮

components/home/feature-tabs/types.ts:
⋮
│export type CodeSnippets = {
│  python?: string;
│  javascript?: string;
⋮
│export type TabDisplayMode =
│  | "default"
│  | "code-only"
│  | "feature-only"
⋮

components/home/layout/HomeLayout.tsx:
⋮
│type ContentColumnsProps = {
│  children: ReactNode;
│  showAside?: boolean;
│  leftSidebar?: ReactNode;
│  rightSidebar?: ReactNode;
│  className?: string;
│  footerClassName?: string;
⋮

components/home/layout/HomeMainArea.tsx:
⋮
│export function HomeMainArea({ children }: { children: ReactNode }) {
│  const ref = useRef<HTMLDivElement>(null);
│  const spotlightState = useMemo(() => createPatternSpotlightState(), []);
│
│  useEffect(
│    () => () => disposePatternSpotlight(spotlightState),
│    [spotlightState],
│  );
│
│  const handleMouseMove = useCallback(
⋮

components/home/layout/RightSidebarHiringAndCommunity.tsx:
⋮
│type RightSidebarHiringAndCommunityProps = {
│  /**
│   * When the block is not under a previous section with `pb-px bg-line-structure`
│   * (e.g. blog right aside: spacer + footer), a full-width top rule is needed so
│   * the community row does not look flush next to the main nav surface. Home
│   * `HomeAside` already gets a 1px rule from the TOC block above, so keep false.
│   */
│  withTopRule?: boolean;
⋮

components/icons/book-bookmark.tsx:
⋮
│function IconBookBookmark(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="16"
│      height="16"
│      viewBox="0 0 16 16"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/book.tsx:
⋮
│function IconBook(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="16"
│      height="16"
│      viewBox="0 0 16 16"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/chatgpt.tsx:
⋮
│function IconChatGPT(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 20 20"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <title>ChatGPT</title>
⋮

components/icons/claude.tsx:
⋮
│function IconClaude(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 100 101"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <title>Claude</title>
⋮

components/icons/compass.tsx:
⋮
│function IconCompass(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="16"
│      height="16"
│      viewBox="0 0 16 16"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/desktop-tower.tsx:
⋮
│function IconDesktopTower(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="16"
│      height="16"
│      viewBox="0 0 16 16"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/discord.tsx:
⋮
│function IconDiscord(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 640 512"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <title>Discord</title>
⋮

components/icons/error.tsx:
⋮
│function IconError(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="14"
│      height="14"
│      viewBox="0 0 14 14"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/github.tsx:
⋮
│function IconGithub(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      width="17"
│      height="17"
│      viewBox="0 0 17 17"
│      fill="currentColor"
│      {...props}
│    >
│      <title>GitHub</title>
⋮

components/icons/idea.tsx:
⋮
│function IconIdea(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="14"
│      height="14"
│      viewBox="0 0 14 14"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/info.tsx:
⋮
│function IconInfo(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="14"
│      height="14"
│      viewBox="0 0 14 14"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/linkedin.tsx:
│function IconLinkedin(props: React.SVGProps<SVGSVGElement>) {
⋮

components/icons/mcp.tsx:
⋮
│function IconMCP(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 24 24"
│      fill="currentColor"
│      fillRule="evenodd"
│      height="1em"
│      width="1em"
│      {...props}
│    >
⋮

components/icons/message.tsx:
⋮
│function IconMessage(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 24 24"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <path d="M20 2H4c-1.103 0-2 .897-2 2v12c0 1.103.897 2 2 2h3v3.767L13.277 18H20c1.103 0 2-.897
⋮

components/icons/openai.tsx:
⋮
│function IconOpenai(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 24 24"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <title>OpenAI</title>
⋮

components/icons/python.tsx:
⋮
│function IconPython(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 32 32"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <title>Python</title>
⋮

components/icons/search.tsx:
⋮
│function IconSearch(props: React.SVGProps<SVGSVGElement>) {
│  return (
⋮

components/icons/sort.tsx:
⋮
│function IconSort(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      fill="none"
│      stroke="currentColor"
│      strokeLinecap="round"
│      strokeLinejoin="round"
│      strokeWidth={2}
│      viewBox="0 0 24 24"
│      height="1em"
⋮

components/icons/success.tsx:
⋮
│function IconSuccess(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="14"
│      height="14"
│      viewBox="0 0 14 14"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/typescript.tsx:
⋮
│function IconTypescript(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      viewBox="0 0 24 24"
│      fill="currentColor"
│      height="1em"
│      width="1em"
│      {...props}
│    >
│      <title>Typescript</title>
⋮

components/icons/warning.tsx:
⋮
│function IconWarning(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <svg
│      xmlns="http://www.w3.org/2000/svg"
│      width="14"
│      height="14"
│      viewBox="0 0 14 14"
│      fill="none"
│      {...props}
│    >
⋮

components/icons/x.tsx:
│function IconX(props: React.SVGProps<SVGSVGElement>) {
⋮

components/icons/youtube.tsx:
⋮
│function IconYoutube(props: React.SVGProps<SVGSVGElement>) {
│  return (
│    <>
│      <svg
│        viewBox="0 0 640 640"
│        fill="currentColor"
│        height="1em"
│        width="1em"
│        {...props}
│      >
⋮

components/imageGenerator/index.tsx:
⋮
│type ImageGeneratorProps = HTMLAttributes<HTMLDivElement>;
│
⋮

components/inkeep/InkeepSearchBar.tsx:
⋮
│type InkeepSearchProps = {
│  className?: string;
⋮
│type InkeepSearchButtonProps = {
│  className?: string;
⋮

components/inkeep/markdown.tsx:
⋮
│export interface Processor {
│  process: (content: string) => Promise<ReactNode>;
⋮

components/inkeep/useInkeepSettings.ts:
⋮
│type InkeepSharedSettings = {
│  baseSettings: InkeepBaseSettings;
│  aiChatSettings: InkeepAIChatSettings;
│  searchSettings: InkeepSearchSettings;
│  modalSettings: InkeepModalSettings;
⋮

components/japan/styles.tsx:
│export function JapanStyles() {
⋮

components/launch-week-5/styles.tsx:
│export function LaunchWeek5Styles() {
⋮

components/layout/DocsContentArea.tsx:
⋮
│export function DocsPatternTracker() {
│  useEffect(() => {
│    const spotlightState = createPatternSpotlightState();
│    const getPage = () => document.getElementById("nd-page");
│
│    const handler = (e: MouseEvent) => {
│      const page = getPage();
│      if (!page) return;
│      const rect = page.getBoundingClientRect();
│      // Only update when cursor is inside the content area
⋮

components/layout/DocsLayoutWrapper.tsx:
⋮
│export function DocsLayoutWrapper({ children }: { children: ReactNode }) {
│  return <div className="layout-wrapper flex-1">{children}</div>;
⋮

components/layout/Layout.tsx:
⋮
│type LayoutProps = {
│  children: React.ReactNode;
⋮

components/qaChatbot/FeedbackPopover.tsx:
⋮
│interface FeedbackDialogProps {
│  messageId: string;
│  feedbackType: "positive" | "negative";
│  currentFeedback: number | null;
│  onFeedback: (messageId: string, value: number, comment?: string) => void;
⋮

components/qaChatbot/index.tsx:
⋮
│type ChatProps = HTMLAttributes<HTMLDivElement>;
│
⋮

components/resources/ResourcesIndex.tsx:
⋮
│type ResourcePage = ReturnType<typeof resourcesSource.getPages>[number];
│
⋮

components/role-finder/role-finder-data.ts:
⋮
│export type RoleKey =
│  | "product"
│  | "growth"
│  | "integrations"
│  | "sdk"
│  | "data_infra"
│  | "iam_billing"
│  | "cloud"
⋮

components/shared/EnterpriseLogoGrid.tsx:
⋮
│interface EnterpriseLogoGridProps {
│  className?: string;
│  small?: boolean;
⋮

components/ui/badge.tsx:
⋮
│export interface BadgeProps
│  extends
│    React.HTMLAttributes<HTMLDivElement>,
│    VariantProps<typeof badgeVariants> {
│  className?: string;
│  children?: React.ReactNode;
⋮

components/ui/corner-box.tsx:
⋮
│export type BoxCorners = Partial<Record<BoxCornerKey, boolean>>;
│
⋮
│export type BoxNeighbors = {
│  top?: boolean;
│  right?: boolean;
│  bottom?: boolean;
│  left?: boolean;
⋮

components/ui/dropdown-button.tsx:
⋮
│type DropdownButtonSize = "default" | "small";
│
⋮

components/ui/heading.tsx:
⋮
│export type HeadingSize = "big" | "large" | "normal" | "small";
│export type HeadingLevel = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
│
⋮

components/ui/integration-label.tsx:
⋮
│interface IntegrationLabelProps {
│  icon?: ReactNode;
│  label: string;
│  href?: string;
│  className?: string;
│  onMouseEnter?: MouseEventHandler;
│  onMouseLeave?: MouseEventHandler;
⋮

components/ui/link-box.tsx:
⋮
│export type LinkBoxTooltipPlacement =
│  | "follow"
│  | "bottom-center"
⋮

components/ui/link.tsx:
⋮
│export type LinkProps = AnchorHTMLAttributes<HTMLAnchorElement> &
⋮
│export function Link({
│  href,
│  variant,
│  className,
│  children,
│  target,
│  rel,
│  ...props
⋮

components/ui/text.tsx:
⋮
│export type TextProps<T extends React.ElementType = "p"> =
│  React.ComponentPropsWithoutRef<T> & {
│    /** Body-M (15px), Body-S (13px), or Body-XS Mono (10px). Default `"m"`. */
│    size?: "m" | "s" | "xs";
│    /** Render as a different element. Default `"p"`. */
│    as?: T;
⋮

components/watchOrBookDemo/WatchWalkthroughs.tsx:
⋮
│interface VideoPlayerProps {
│  videoId: string;
│  title: string;
⋮

components/wrapped/Launches.tsx:
⋮
│interface LaunchItemProps {
│  title: string;
│  route: string;
⋮

components/wrapped/Metrics.tsx:
⋮
│interface MetricCardProps {
│  value: number | string;
│  label: string;
│  description?: string;
│  suffix?: string;
│  isFullWidth?: boolean;
│  decimals?: number;
│  ratePerSecond?: number;
│  icon?: LucideIcon;
⋮

components/wrapped/OSS.tsx:
⋮
│interface MetricCardProps {
│  value: number;
│  label: string;
│  suffix?: string;
│  icon?: LucideIcon;
⋮

components/wrapped/WrappedDataContext.tsx:
⋮
│export type WrappedData = {
│  usersPages: PageData[];
│  changelogPages: PageData[];
⋮

components/wrapped/components/HoverStars.tsx:
⋮
│interface HoverStarsProps {
│  className?: string;
⋮

components/wrapped/components/SectionHeading.tsx:
⋮
│interface SectionHeadingProps {
│  title: string;
│  subtitle?: string;
│  className?: string;
│  children?: React.ReactNode;
⋮

data/testimonials.ts:
│export interface Testimonial {
⋮

global.d.ts:
⋮
│declare module "@modelcontextprotocol/sdk/client/streamableHttp" {
│  export class StreamableHTTPError extends Error {
│    readonly code: number | undefined;
│    constructor(code: number | undefined, message: string | undefined);
│  }
│  export type StreamableHTTPClientTransportOptions = {
│    authProvider?: unknown;
│    requestInit?: RequestInit;
│    sessionId?: string;
│  };
⋮

lib/ai/inkeep-qa-schema.ts:
⋮
│export type InkeepUIMessage = UIMessage<
│  never,
│  {
│    client: {
│      location: string;
│    };
│  }
⋮

lib/cloud-regions.ts:
⋮
│export type CloudRegionKey = keyof typeof cloudRegions;
│
⋮

lib/contact-sales-form.ts:
⋮
│export type ContactFormData = z.infer<typeof contactFormSchema>;
│
⋮

lib/content-width.ts:
⋮
│export type ContentWidthType = "docs" | "full";
│
⋮
│export type ResolvedContentWidth = ContentWidthType | "default";
│
⋮

lib/github-stars.ts:
⋮
│export function getGitHubStars(): number {
│  return GITHUB_STARS;
⋮

lib/google-ads.ts:
⋮
│type ConversionOptions = {
│  value?: number;
│  currency?: string;
⋮

lib/inkeep-search-backend.ts:
⋮
│export type InkeepSearchResponse = {
│  answer: string;
│  metadata: unknown;
⋮

lib/integrations-meta.ts:
⋮
│type MetaEntry = { href?: string; title?: string; logo?: string };
⋮

lib/linkedin-ads.ts:
⋮
│export function reportLinkedInConversion(conversionId: number) {
│  if (
│    !conversionId ||
│    typeof window === "undefined" ||
│    typeof window.lintrk !== "function"
│  ) {
│    return;
│  }
│
│  window.lintrk("track", { conversion_id: conversionId });
⋮

lib/mdx-page.ts:
⋮
│type AnySource = {
│  getPage: (slug: string[]) => any;
│  getPages: () => any[];
│  generateParams: () => { slug: string[] }[];
⋮

lib/nav-links.tsx:
⋮
│export type NavPanelLink = {
│  name: string;
│  href: string;
│  icon: LucideIcon;
⋮

lib/nav-tree.ts:
│export interface SectionNavData {
⋮

lib/rateLimit.ts:
⋮
│export function rateLimit(
│  req: Request,
│  opts: { limit: number; windowMs: number },
⋮

lib/reddit-ads.ts:
⋮
│export function reportRedditConversion(eventName: string) {
│  if (
│    !eventName ||
│    !REDDIT_PIXEL_ID ||
│    typeof window === "undefined" ||
│    typeof window.rdt !== "function"
│  ) {
│    return;
│  }
│
⋮

lib/remark-to-markdown-extensions.mjs:
⋮
│export function remarkToMarkdownExtensions() {
│  const self = this;
│  const data = self.data();
│  data.toMarkdownExtensions = [
│    ...(data.toMarkdownExtensions ?? []),
│    mdxJsxToMarkdown(),
│  ];
│  return function () {
│    /* no-op transformer; we only set processor data */
│  };
⋮

lib/twitter-ads.ts:
⋮
│type TwitterEventOptions = {
│  value?: number;
│  currency?: string;
⋮

scripts/update-github-stars.js:
⋮
│async function updateGitHubStars() {
│  try {
│    console.log("Fetching GitHub stars...");
│
│    // Prepare headers for the GitHub API request
│    const headers = {
│      Accept: "application/vnd.github.v3+json",
│      "User-Agent": "langfuse-docs",
│    };
│
⋮
```

### AST Map: `modules/langfuse-python`

```python
langfuse/_client/attributes.py:
⋮
│def _serialize(obj: Any) -> Optional[str]:
⋮
│def _flatten_and_serialize_metadata_values(
│    metadata: Optional[Dict[str, Any]],
│) -> Optional[Dict[str, str]]:
│    if metadata is None:
⋮
│    def flatten_value(path: str, value: Any) -> None:
⋮

langfuse/_client/client.py:
⋮
│class Langfuse:
│    """Main client for Langfuse tracing and platform features.
│
│    This class provides an interface for creating and managing traces, spans,
│    and generations in Langfuse as well as interacting with the Langfuse API.
│
│    The client features a thread-safe singleton pattern for each unique public API key,
│    ensuring consistent trace context propagation across your application. It implements
│    efficient batching of spans with configurable flush settings and includes background
│    thread management for media uploads and score ingestion.
│
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["generation"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["span"] = "span",
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["agent"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["tool"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["chain"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["retriever"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["evaluator"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["embedding"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: Literal["guardrail"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    def start_observation(
│        self,
│        *,
│        trace_context: Optional[TraceContext] = None,
│        name: str,
│        as_type: ObservationTypeLiteralNoEvent = "span",
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
⋮
│    @overload
│    def create_score(
│        self,
│        *,
│        name: str,
│        value: float,
│        session_id: Optional[str] = None,
│        dataset_run_id: Optional[str] = None,
│        trace_id: Optional[str] = None,
│        observation_id: Optional[str] = None,
│        score_id: Optional[str] = None,
⋮
│    @overload
│    def create_score(
│        self,
│        *,
│        name: str,
│        value: str,
│        session_id: Optional[str] = None,
│        dataset_run_id: Optional[str] = None,
│        trace_id: Optional[str] = None,
│        score_id: Optional[str] = None,
│        observation_id: Optional[str] = None,
⋮
│    def create_score(
│        self,
│        *,
│        name: str,
│        value: Union[float, str],
│        session_id: Optional[str] = None,
│        dataset_run_id: Optional[str] = None,
│        trace_id: Optional[str] = None,
│        observation_id: Optional[str] = None,
│        score_id: Optional[str] = None,
⋮
│    def run_experiment(
│        self,
│        *,
│        name: str,
│        run_name: Optional[str] = None,
│        description: Optional[str] = None,
│        data: ExperimentData,
│        task: TaskFunction,
│        evaluators: List[EvaluatorFunction] = [],
│        composite_evaluator: Optional[CompositeEvaluatorFunction] = None,
⋮

langfuse/_client/constants.py:
⋮
│def get_observation_types_list(
│    literal_type: Any,
⋮

langfuse/_client/datasets.py:
⋮
│class DatasetClient:
│    """Class for managing datasets in Langfuse.
│
│    Attributes:
│        id (str): Unique identifier of the dataset.
│        name (str): Name of the dataset.
│        description (Optional[str]): Description of the dataset.
│        metadata (Optional[typing.Any]): Additional metadata of the dataset.
│        project_id (str): Identifier of the project to which the dataset belongs.
│        created_at (datetime): Timestamp of dataset creation.
│        updated_at (datetime): Timestamp of the last update to the dataset.
⋮
│    def run_experiment(
│        self,
│        *,
│        name: str,
│        run_name: Optional[str] = None,
│        description: Optional[str] = None,
│        task: TaskFunction,
│        evaluators: List[EvaluatorFunction] = [],
│        composite_evaluator: Optional[CompositeEvaluatorFunction] = None,
│        run_evaluators: List[RunEvaluatorFunction] = [],
⋮

langfuse/_client/get_client.py:
⋮
│def get_client(*, public_key: Optional[str] = None) -> Langfuse:
⋮

langfuse/_client/resource_manager.py:
⋮
│class LangfuseResourceManager:
│    """Thread-safe singleton that provides access to the OpenTelemetry tracer and processors.
│
│    This class implements a thread-safe singleton pattern keyed by the public API key,
│    ensuring that only one tracer instance exists per API key combination. It manages
│    the lifecycle of the OpenTelemetry tracer provider, span processors, and resource
│    attributes, as well as background threads for media uploads and score ingestion.
│
│    The tracer is responsible for:
│    1. Setting up the OpenTelemetry tracer with appropriate sampling and configuration
│    2. Managing the span processor for exporting spans to the Langfuse API
⋮
│    @staticmethod
│    def get_current_span() -> Any:
⋮

langfuse/_client/span.py:
⋮
│class LangfuseObservationWrapper:
│    """Abstract base class for all Langfuse span types.
│
│    This class provides common functionality for all Langfuse span types, including
│    media processing, attribute management, and scoring. It wraps an OpenTelemetry
│    span and extends it with Langfuse-specific features.
│
│    Attributes:
│        _otel_span: The underlying OpenTelemetry span
│        _langfuse_client: Reference to the parent Langfuse client
│        trace_id: The trace ID for this span
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["span"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["generation"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["agent"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["tool"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["chain"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["retriever"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["evaluator"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["embedding"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["guardrail"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    @overload
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: Literal["event"],
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮
│    def start_observation(
│        self,
│        *,
│        name: str,
│        as_type: ObservationTypeLiteral = "span",
│        input: Optional[Any] = None,
│        output: Optional[Any] = None,
│        metadata: Optional[Any] = None,
│        version: Optional[str] = None,
│        level: Optional[SpanLevel] = None,
⋮

langfuse/_client/span_filter.py:
⋮
│def is_langfuse_span(span: ReadableSpan) -> bool:
⋮
│def is_genai_span(span: ReadableSpan) -> bool:
⋮
│def is_known_llm_instrumentor(span: ReadableSpan) -> bool:
⋮

langfuse/_task_manager/media_upload_queue.py:
⋮
│class UploadMediaJob(TypedDict):
⋮

langfuse/_utils/__init__.py:
⋮
│def _create_prompt_context(
│    prompt: typing.Optional[PromptClient] = None,
⋮

langfuse/_utils/environment.py:
⋮
│common_release_envs = [
│    # Render
│    "RENDER_GIT_COMMIT",
│    # GitLab CI
│    "CI_COMMIT_SHA",
│    # CircleCI
│    "CIRCLE_SHA1",
│    # Heroku
│    "SOURCE_VERSION",
│    # Travis CI
⋮
│def get_common_release_envs() -> Optional[str]:
⋮

langfuse/_utils/json_path.py:
⋮
│def parse_path(json_path: str) -> List[Union[str, int]]:
⋮

langfuse/_utils/parse_error.py:
⋮
│def generate_error_message_fern(error: Error) -> str:
⋮
│def generate_error_message(exception: Union[APIError, APIErrors, Exception]) -> str:
⋮

langfuse/_utils/prompt_cache.py:
⋮
│class PromptCacheItem:
│    def __init__(self, prompt: PromptClient, ttl_seconds: int):
│        self.value = prompt
⋮
│    def is_expired(self) -> bool:
⋮
│    @staticmethod
│    def get_epoch_seconds() -> int:
⋮

langfuse/_utils/request.py:
⋮
│class APIError(Exception):
⋮

langfuse/_utils/serializer.py:
⋮
│class EventSerializer(JSONEncoder):
│    _MAX_DEPTH = 20
│
⋮
│    @staticmethod
│    def is_js_safe_integer(value: int) -> bool:
⋮
│def serialize_datetime(v: dt.datetime) -> str:
│    def _serialize_zoned_datetime(v: dt.datetime) -> str:
│        if v.tzinfo is not None and v.tzinfo.tzname(None) == dt.timezone.utc.tzname(
│            None
│        ):
│            # UTC is a special case where we use "Z" at the end instead of "+00:00"
│            return v.isoformat().replace("+00:00", "Z")
│        else:
│            # Delegate to the typical +/- offset format
⋮

langfuse/_version.py:
⋮
│@lru_cache(maxsize=1)
│def get_langfuse_version() -> str:
⋮

langfuse/api/annotation_queues/types/delete_annotation_queue_assignment_response.py:
⋮
│class DeleteAnnotationQueueAssignmentResponse(UniversalBaseModel):
⋮

langfuse/api/annotation_queues/types/delete_annotation_queue_item_response.py:
⋮
│class DeleteAnnotationQueueItemResponse(UniversalBaseModel):
⋮

langfuse/api/annotation_queues/types/paginated_annotation_queue_items.py:
⋮
│class PaginatedAnnotationQueueItems(UniversalBaseModel):
⋮

langfuse/api/annotation_queues/types/paginated_annotation_queues.py:
⋮
│class PaginatedAnnotationQueues(UniversalBaseModel):
⋮

langfuse/api/annotation_queues/types/update_annotation_queue_item_request.py:
⋮
│class UpdateAnnotationQueueItemRequest(UniversalBaseModel):
⋮

langfuse/api/blob_storage_integrations/types/blob_storage_integration_deletion_response.py:
⋮
│class BlobStorageIntegrationDeletionResponse(UniversalBaseModel):
⋮

langfuse/api/blob_storage_integrations/types/blob_storage_integrations_response.py:
⋮
│class BlobStorageIntegrationsResponse(UniversalBaseModel):
⋮

langfuse/api/comments/client.py:
⋮
│class CommentsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self,
│        *,
│        page: typing.Optional[int] = None,
│        limit: typing.Optional[int] = None,
│        object_type: typing.Optional[str] = None,
│        object_id: typing.Optional[str] = None,
│        author_user_id: typing.Optional[str] = None,
│        request_options: typing.Optional[RequestOptions] = None,
⋮
│class AsyncCommentsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self,
│        *,
│        page: typing.Optional[int] = None,
│        limit: typing.Optional[int] = None,
│        object_type: typing.Optional[str] = None,
│        object_id: typing.Optional[str] = None,
│        author_user_id: typing.Optional[str] = None,
│        request_options: typing.Optional[RequestOptions] = None,
⋮

langfuse/api/comments/types/create_comment_response.py:
⋮
│class CreateCommentResponse(UniversalBaseModel):
⋮

langfuse/api/comments/types/get_comments_response.py:
⋮
│class GetCommentsResponse(UniversalBaseModel):
⋮

langfuse/api/commons/errors/access_denied_error.py:
⋮
│class AccessDeniedError(ApiError):
⋮

langfuse/api/commons/errors/method_not_allowed_error.py:
⋮
│class MethodNotAllowedError(ApiError):
⋮

langfuse/api/commons/errors/not_found_error.py:
⋮
│class NotFoundError(ApiError):
⋮

langfuse/api/commons/errors/unauthorized_error.py:
⋮
│class UnauthorizedError(ApiError):
⋮

langfuse/api/commons/types/config_category.py:
⋮
│class ConfigCategory(UniversalBaseModel):
⋮

langfuse/api/commons/types/create_score_value.py:
⋮
│CreateScoreValue = typing.Union[float, str]

langfuse/api/commons/types/map_value.py:
⋮
│MapValue = typing.Union[
│    typing.Optional[str],
│    typing.Optional[int],
│    typing.Optional[float],
│    typing.Optional[bool],
│    typing.Optional[typing.List[str]],
⋮

langfuse/api/commons/types/model_price.py:
⋮
│class ModelPrice(UniversalBaseModel):
⋮

langfuse/api/commons/types/numeric_score.py:
⋮
│class NumericScore(BaseScore):
⋮

langfuse/api/commons/types/numeric_score_v1.py:
⋮
│class NumericScoreV1(BaseScoreV1):
⋮

langfuse/api/commons/types/session_with_traces.py:
⋮
│class SessionWithTraces(Session):
⋮

langfuse/api/core/api_error.py:
⋮
│class ApiError(Exception):
⋮

langfuse/api/core/datetime_utils.py:
⋮
│def serialize_datetime(v: dt.datetime) -> str:
│    """
│    Serialize a datetime including timezone info.
│
│    Uses the timezone info provided if present, otherwise uses the current runtime's timezone info.
│
│    UTC datetimes end in "Z" while all other timezones are represented as offset from UTC, e.g. +05
⋮
│    def _serialize_zoned_datetime(v: dt.datetime) -> str:
⋮

langfuse/api/core/enum.py:
⋮
│if sys.version_info >= (3, 11):
│    from enum import StrEnum
│else:
│
│    class StrEnum(str, enum.Enum):
⋮

langfuse/api/core/file.py:
⋮
│FileContent = Union[IO[bytes], bytes, str]
│File = Union[
│    # file (or bytes)
│    FileContent,
│    # (filename, file (or bytes))
│    Tuple[Optional[str], FileContent],
│    # (filename, file (or bytes), content_type)
│    Tuple[Optional[str], FileContent, Optional[str]],
│    # (filename, file (or bytes), content_type, headers)
│    Tuple[
│        Optional[str],
⋮
│def with_content_type(*, file: File, default_content_type: str) -> File:
⋮

langfuse/api/core/force_multipart.py:
⋮
│class ForceMultipartDict(Dict[str, Any]):
⋮

langfuse/api/core/http_response.py:
⋮
│class HttpResponse(Generic[T], BaseHttpResponse):
⋮
│class AsyncHttpResponse(Generic[T], BaseHttpResponse):
⋮

langfuse/api/core/http_sse/_exceptions.py:
⋮
│class SSEError(httpx.TransportError):
⋮

langfuse/api/core/http_sse/_models.py:
⋮
│@dataclass(frozen=True)
│class ServerSentEvent:
│    event: str = "message"
⋮
│    def json(self) -> Any:
⋮

langfuse/api/core/jsonable_encoder.py:
⋮
│def jsonable_encoder(
│    obj: Any, custom_encoder: Optional[Dict[Any, Callable[[Any], Any]]] = None
│) -> Any:
│    custom_encoder = custom_encoder or {}
⋮
│    def fallback_serializer(o: Any) -> Any:
⋮

langfuse/api/core/pydantic_utilities.py:
⋮
│def parse_obj_as(type_: Type[T], object_: Any) -> T:
⋮
│class UniversalBaseModel(pydantic.BaseModel):
│    if IS_PYDANTIC_V2:
│        model_config: ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(  # type: ignore[typeddic
│            # Allow fields beginning with `model_` to be used in the model
│            protected_namespaces=(),
│        )
│
│        @pydantic.model_serializer(mode="plain", when_used="json")  # type: ignore[attr-defined]
│        def serialize_model(self) -> Any:  # type: ignore[name-defined]
│            serialized = self.dict()  # type: ignore[attr-defined]
│            data = {
⋮
│    @classmethod
│    def model_construct(
│        cls: Type["Model"], _fields_set: Optional[Set[str]] = None, **values: Any
⋮
│    def dict(self, **kwargs: Any) -> Dict[str, Any]:
⋮
│def deep_union_pydantic_dicts(
│    source: Dict[str, Any], destination: Dict[str, Any]
⋮
│def update_forward_refs(model: Type["Model"], **localns: Any) -> None:
⋮

langfuse/api/core/query_encoder.py:
⋮
│def traverse_query_dict(
│    dict_flat: Dict[str, Any], key_prefix: Optional[str] = None
⋮
│def single_query_encoder(query_key: str, query_value: Any) -> List[Tuple[str, Any]]:
⋮

langfuse/api/core/request_options.py:
⋮
│class RequestOptions(typing.TypedDict, total=False):
⋮

langfuse/api/core/serialization.py:
⋮
│class FieldMetadata:
⋮
│def convert_and_respect_annotation_metadata(
│    *,
│    object_: typing.Any,
│    annotation: typing.Any,
│    inner_type: typing.Optional[typing.Any] = None,
│    direction: typing.Literal["read", "write"],
⋮
│def _convert_mapping(
│    object_: typing.Mapping[str, object],
│    expected_type: typing.Any,
│    direction: typing.Literal["read", "write"],
⋮
│def _get_annotation(type_: typing.Any) -> typing.Optional[typing.Any]:
⋮
│def _remove_annotations(type_: typing.Any) -> typing.Any:
⋮
│def _get_alias_to_field_name(
│    field_to_hint: typing.Dict[str, typing.Any],
⋮
│def _get_field_to_alias_name(
│    field_to_hint: typing.Dict[str, typing.Any],
⋮
│def _get_alias_from_type(type_: typing.Any) -> typing.Optional[str]:
⋮
│def _alias_key(
│    key: str,
│    type_: typing.Any,
│    direction: typing.Literal["read", "write"],
│    aliases_to_field_names: typing.Dict[str, str],
⋮

langfuse/api/dataset_items/client.py:
⋮
│class DatasetItemsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
⋮
│class AsyncDatasetItemsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
⋮

langfuse/api/dataset_items/raw_client.py:
⋮
│class RawDatasetItemsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
⋮
│class AsyncRawDatasetItemsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
⋮

langfuse/api/dataset_items/types/delete_dataset_item_response.py:
⋮
│class DeleteDatasetItemResponse(UniversalBaseModel):
⋮

langfuse/api/dataset_items/types/paginated_dataset_items.py:
⋮
│class PaginatedDatasetItems(UniversalBaseModel):
⋮

langfuse/api/dataset_run_items/types/paginated_dataset_run_items.py:
⋮
│class PaginatedDatasetRunItems(UniversalBaseModel):
⋮

langfuse/api/datasets/raw_client.py:
⋮
│class RawDatasetsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self,
│        dataset_name: str,
│        *,
│        request_options: typing.Optional[RequestOptions] = None,
⋮
│class AsyncRawDatasetsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self,
│        dataset_name: str,
│        *,
│        request_options: typing.Optional[RequestOptions] = None,
⋮

langfuse/api/datasets/types/delete_dataset_run_response.py:
⋮
│class DeleteDatasetRunResponse(UniversalBaseModel):
⋮

langfuse/api/datasets/types/paginated_dataset_runs.py:
⋮
│class PaginatedDatasetRuns(UniversalBaseModel):
⋮

langfuse/api/datasets/types/paginated_datasets.py:
⋮
│class PaginatedDatasets(UniversalBaseModel):
⋮

langfuse/api/experiments/types/experiment_items_response.py:
⋮
│class ExperimentItemsResponse(UniversalBaseModel):
⋮

langfuse/api/experiments/types/experiments_response.py:
⋮
│class ExperimentsResponse(UniversalBaseModel):
⋮

langfuse/api/experiments/types/experiments_response_meta.py:
⋮
│class ExperimentsResponseMeta(UniversalBaseModel):
⋮

langfuse/api/health/types/health_response.py:
⋮
│class HealthResponse(UniversalBaseModel):
⋮

langfuse/api/ingestion/types/base_event.py:
⋮
│class BaseEvent(UniversalBaseModel):
⋮

langfuse/api/ingestion/types/create_event_body.py:
⋮
│class CreateEventBody(OptionalObservationBody):
⋮

langfuse/api/ingestion/types/create_event_event.py:
⋮
│class CreateEventEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/create_generation_event.py:
⋮
│class CreateGenerationEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/create_observation_event.py:
⋮
│class CreateObservationEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/create_span_event.py:
⋮
│class CreateSpanEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/ingestion_error.py:
⋮
│class IngestionError(UniversalBaseModel):
⋮

langfuse/api/ingestion/types/ingestion_response.py:
⋮
│class IngestionResponse(UniversalBaseModel):
⋮

langfuse/api/ingestion/types/ingestion_success.py:
⋮
│class IngestionSuccess(UniversalBaseModel):
⋮

langfuse/api/ingestion/types/score_event.py:
⋮
│class ScoreEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/sdk_log_body.py:
⋮
│class SdkLogBody(UniversalBaseModel):
⋮

langfuse/api/ingestion/types/sdk_log_event.py:
⋮
│class SdkLogEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/trace_event.py:
⋮
│class TraceEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/update_event_body.py:
⋮
│class UpdateEventBody(OptionalObservationBody):
⋮

langfuse/api/ingestion/types/update_generation_event.py:
⋮
│class UpdateGenerationEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/update_observation_event.py:
⋮
│class UpdateObservationEvent(BaseEvent):
⋮

langfuse/api/ingestion/types/update_span_event.py:
⋮
│class UpdateSpanEvent(BaseEvent):
⋮

langfuse/api/legacy/metrics_v1/types/metrics_response.py:
⋮
│class MetricsResponse(UniversalBaseModel):
⋮

langfuse/api/legacy/observations_v1/types/observations.py:
⋮
│class Observations(UniversalBaseModel):
⋮

langfuse/api/legacy/observations_v1/types/observations_views.py:
⋮
│class ObservationsViews(UniversalBaseModel):
⋮

langfuse/api/legacy/score_v1/types/create_score_response.py:
⋮
│class CreateScoreResponse(UniversalBaseModel):
⋮

langfuse/api/llm_connections/types/delete_llm_connection_response.py:
⋮
│class DeleteLlmConnectionResponse(UniversalBaseModel):
⋮

langfuse/api/llm_connections/types/paginated_llm_connections.py:
⋮
│class PaginatedLlmConnections(UniversalBaseModel):
⋮

langfuse/api/media/raw_client.py:
⋮
│class RawMediaClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self, media_id: str, *, request_options: typing.Optional[RequestOptions] = None
⋮
│class AsyncRawMediaClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self, media_id: str, *, request_options: typing.Optional[RequestOptions] = None
⋮

langfuse/api/metrics/types/metrics_v2response.py:
⋮
│class MetricsV2Response(UniversalBaseModel):
⋮

langfuse/api/models/types/paginated_models.py:
⋮
│class PaginatedModels(UniversalBaseModel):
⋮

langfuse/api/observations/types/observations_v2meta.py:
⋮
│class ObservationsV2Meta(UniversalBaseModel):
⋮

langfuse/api/observations/types/observations_v2response.py:
⋮
│class ObservationsV2Response(UniversalBaseModel):
⋮

langfuse/api/opentelemetry/types/otel_attribute.py:
⋮
│class OtelAttribute(UniversalBaseModel):
⋮

langfuse/api/opentelemetry/types/otel_resource.py:
⋮
│class OtelResource(UniversalBaseModel):
⋮

langfuse/api/opentelemetry/types/otel_scope.py:
⋮
│class OtelScope(UniversalBaseModel):
⋮

langfuse/api/opentelemetry/types/otel_scope_span.py:
⋮
│class OtelScopeSpan(UniversalBaseModel):
⋮

langfuse/api/opentelemetry/types/otel_trace_response.py:
⋮
│class OtelTraceResponse(UniversalBaseModel):
⋮

langfuse/api/organizations/types/memberships_response.py:
⋮
│class MembershipsResponse(UniversalBaseModel):
⋮

langfuse/api/organizations/types/organization_projects_response.py:
⋮
│class OrganizationProjectsResponse(UniversalBaseModel):
⋮

langfuse/api/projects/client.py:
⋮
│class ProjectsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self, *, request_options: typing.Optional[RequestOptions] = None
⋮
│class AsyncProjectsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self, *, request_options: typing.Optional[RequestOptions] = None
⋮

langfuse/api/projects/raw_client.py:
⋮
│class RawProjectsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self, *, request_options: typing.Optional[RequestOptions] = None
⋮
│class AsyncRawProjectsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self, *, request_options: typing.Optional[RequestOptions] = None
⋮

langfuse/api/projects/types/api_key_deletion_response.py:
⋮
│class ApiKeyDeletionResponse(UniversalBaseModel):
⋮

langfuse/api/projects/types/organization.py:
⋮
│class Organization(UniversalBaseModel):
⋮

langfuse/api/projects/types/project_deletion_response.py:
⋮
│class ProjectDeletionResponse(UniversalBaseModel):
⋮

langfuse/api/projects/types/projects.py:
⋮
│class Projects(UniversalBaseModel):
⋮

langfuse/api/prompts/raw_client.py:
⋮
│class RawPromptsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self,
│        prompt_name: str,
│        *,
│        version: typing.Optional[int] = None,
│        label: typing.Optional[str] = None,
│        resolve: typing.Optional[bool] = None,
│        request_options: typing.Optional[RequestOptions] = None,
⋮
│class AsyncRawPromptsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self,
│        prompt_name: str,
│        *,
│        version: typing.Optional[int] = None,
│        label: typing.Optional[str] = None,
│        resolve: typing.Optional[bool] = None,
│        request_options: typing.Optional[RequestOptions] = None,
⋮

langfuse/api/prompts/types/chat_prompt.py:
⋮
│class ChatPrompt(BasePrompt):
⋮

langfuse/api/prompts/types/prompt_meta_list_response.py:
⋮
│class PromptMetaListResponse(UniversalBaseModel):
⋮

langfuse/api/prompts/types/text_prompt.py:
⋮
│class TextPrompt(BasePrompt):
⋮

langfuse/api/scim/types/empty_response.py:
⋮
│class EmptyResponse(UniversalBaseModel):
⋮

langfuse/api/scim/types/schema_resource.py:
⋮
│class SchemaResource(UniversalBaseModel):
⋮

langfuse/api/scim/types/scim_email.py:
⋮
│class ScimEmail(UniversalBaseModel):
⋮

langfuse/api/scim/types/scim_feature_support.py:
⋮
│class ScimFeatureSupport(UniversalBaseModel):
⋮

langfuse/api/scim/types/scim_name.py:
⋮
│class ScimName(UniversalBaseModel):
⋮

langfuse/api/score_configs/types/score_configs.py:
⋮
│class ScoreConfigs(UniversalBaseModel):
⋮

langfuse/api/scores/types/get_scores_response.py:
⋮
│class GetScoresResponse(UniversalBaseModel):
⋮

langfuse/api/scores/types/get_scores_response_data_boolean.py:
⋮
│class GetScoresResponseDataBoolean(BooleanScore):
⋮

langfuse/api/scores/types/get_scores_response_data_categorical.py:
⋮
│class GetScoresResponseDataCategorical(CategoricalScore):
⋮

langfuse/api/scores/types/get_scores_response_data_correction.py:
⋮
│class GetScoresResponseDataCorrection(CorrectionScore):
⋮

langfuse/api/scores/types/get_scores_response_data_numeric.py:
⋮
│class GetScoresResponseDataNumeric(NumericScore):
⋮

langfuse/api/scores/types/get_scores_response_data_text.py:
⋮
│class GetScoresResponseDataText(TextScore):
⋮

langfuse/api/scores_v3/types/boolean_score_v3.py:
⋮
│class BooleanScoreV3(BaseScoreV3):
⋮

langfuse/api/scores_v3/types/categorical_score_v3.py:
⋮
│class CategoricalScoreV3(BaseScoreV3):
⋮

langfuse/api/scores_v3/types/correction_score_v3.py:
⋮
│class CorrectionScoreV3(BaseScoreV3):
⋮

langfuse/api/scores_v3/types/get_scores_v3meta.py:
⋮
│class GetScoresV3Meta(UniversalBaseModel):
⋮

langfuse/api/scores_v3/types/get_scores_v3response.py:
⋮
│class GetScoresV3Response(UniversalBaseModel):
⋮

langfuse/api/scores_v3/types/numeric_score_v3.py:
⋮
│class NumericScoreV3(BaseScoreV3):
⋮

langfuse/api/scores_v3/types/score_subject_experiment_v3.py:
⋮
│class ScoreSubjectExperimentV3(UniversalBaseModel):
⋮

langfuse/api/scores_v3/types/score_subject_session_v3.py:
⋮
│class ScoreSubjectSessionV3(UniversalBaseModel):
⋮

langfuse/api/scores_v3/types/score_subject_trace_v3.py:
⋮
│class ScoreSubjectTraceV3(UniversalBaseModel):
⋮

langfuse/api/scores_v3/types/text_score_v3.py:
⋮
│class TextScoreV3(BaseScoreV3):
⋮

langfuse/api/sessions/raw_client.py:
⋮
│class RawSessionsClient:
│    def __init__(self, *, client_wrapper: SyncClientWrapper):
⋮
│    def get(
│        self,
│        session_id: str,
│        *,
│        request_options: typing.Optional[RequestOptions] = None,
⋮
│class AsyncRawSessionsClient:
│    def __init__(self, *, client_wrapper: AsyncClientWrapper):
⋮
│    async def get(
│        self,
│        session_id: str,
│        *,
│        request_options: typing.Optional[RequestOptions] = None,
⋮

langfuse/api/sessions/types/paginated_sessions.py:
⋮
│class PaginatedSessions(UniversalBaseModel):
⋮

langfuse/api/trace/types/delete_trace_response.py:
⋮
│class DeleteTraceResponse(UniversalBaseModel):
⋮

langfuse/api/trace/types/sort.py:
⋮
│class Sort(UniversalBaseModel):
⋮

langfuse/api/trace/types/traces.py:
⋮
│class Traces(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/array_options_evaluation_rule_filter.py:
⋮
│class ArrayOptionsEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/boolean_evaluation_rule_filter.py:
⋮
│class BooleanEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/category_options_evaluation_rule_filter.py:
⋮
│class CategoryOptionsEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/date_time_evaluation_rule_filter.py:
⋮
│class DateTimeEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/evaluator_model_config.py:
⋮
│class EvaluatorModelConfig(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/evaluator_output_field_definition.py:
⋮
│class EvaluatorOutputFieldDefinition(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/null_evaluation_rule_filter.py:
⋮
│class NullEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/number_evaluation_rule_filter.py:
⋮
│class NumberEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/number_object_evaluation_rule_filter.py:
⋮
│class NumberObjectEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/string_evaluation_rule_filter.py:
⋮
│class StringEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/string_object_evaluation_rule_filter.py:
⋮
│class StringObjectEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/commons/types/string_options_evaluation_rule_filter.py:
⋮
│class StringOptionsEvaluationRuleFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/dashboard_widgets/types/dashboard_widget_default_sort.py:
⋮
│class DashboardWidgetDefaultSort(UniversalBaseModel):
⋮

langfuse/api/unstable/dashboard_widgets/types/dashboard_widget_dimension.py:
⋮
│class DashboardWidgetDimension(UniversalBaseModel):
⋮

langfuse/api/unstable/dashboard_widgets/types/dashboard_widget_filter.py:
⋮
│class DashboardWidgetFilter(UniversalBaseModel):
⋮

langfuse/api/unstable/dashboard_widgets/types/dashboard_widget_metric.py:
⋮
│class DashboardWidgetMetric(UniversalBaseModel):
⋮

langfuse/api/unstable/errors/errors/access_denied_error.py:
⋮
│class AccessDeniedError(ApiError):
⋮

langfuse/api/unstable/errors/errors/method_not_allowed_error.py:
⋮
│class MethodNotAllowedError(ApiError):
⋮

langfuse/api/unstable/errors/errors/not_found_error.py:
⋮
│class NotFoundError(ApiError):
⋮

langfuse/api/unstable/errors/errors/unauthorized_error.py:
⋮
│class UnauthorizedError(ApiError):
⋮

langfuse/api/unstable/errors/types/public_api_error.py:
⋮
│class PublicApiError(UniversalBaseModel):
⋮

langfuse/api/unstable/errors/types/public_api_validation_issue.py:
⋮
│class PublicApiValidationIssue(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/code_evaluation_rule_evaluator_reference.py:
⋮
│class CodeEvaluationRuleEvaluatorReference(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/delete_evaluation_rule_response.py:
⋮
│class DeleteEvaluationRuleResponse(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/evaluation_rule_evaluator.py:
⋮
│class EvaluationRuleEvaluator(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/evaluation_rule_evaluator_reference.py:
⋮
│class EvaluationRuleEvaluatorReference(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/evaluation_rules.py:
⋮
│class EvaluationRules(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/llm_as_judge_evaluation_rule_evaluator_reference.py:
⋮
│class LlmAsJudgeEvaluationRuleEvaluatorReference(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluation_rules/types/update_evaluation_rule_request.py:
⋮
│class UpdateEvaluationRuleRequest(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluators/types/delete_evaluator_response.py:
⋮
│class DeleteEvaluatorResponse(UniversalBaseModel):
⋮

langfuse/api/unstable/evaluators/types/evaluators.py:
⋮
│class Evaluators(UniversalBaseModel):
⋮

langfuse/experiment.py:
⋮
│class RunnerContext:
│    """Wraps :meth:`Langfuse.run_experiment` with CI-injected defaults.
│
│    Intended for use with the ``langfuse/experiment-action`` GitHub Action
│    (https://github.com/langfuse/experiment-action). The action builds a
│    ``RunnerContext`` before invoking the user's ``experiment(context)``
│    function. Defaults set here (dataset, metadata tags) are applied when
│    the user omits them on the :meth:`run_experiment` call; users can
│    override any default by passing the corresponding argument explicitly.
⋮
│    def run_experiment(
│        self,
│        *,
│        name: str,
│        run_name: Optional[str] = None,
│        description: Optional[str] = None,
│        data: Optional[ExperimentData] = None,
│        task: TaskFunction,
│        evaluators: List[EvaluatorFunction] = [],
│        composite_evaluator: Optional["CompositeEvaluatorFunction"] = None,
⋮

langfuse/langchain/CallbackHandler.py:
⋮
│class _PendingResumeTraceContextStore:
│    def __init__(self, max_size: int) -> None:
│        self._max_size = max_size
⋮
│    def keys(self) -> List[str]:
⋮

langfuse/media.py:
⋮
│class LangfuseMedia:
⋮

langfuse/model.py:
⋮
│class TemplateParser:
│    OPENING = "{{"
⋮
│    @staticmethod
│    def compile_template(content: str, data: Optional[Dict[str, Any]] = None) -> str:
⋮

langfuse/openai.py:
⋮
│@dataclass
│class OpenAiDefinition:
⋮
│class OpenAiArgsExtractor:
│    def __init__(
│        self,
│        metadata: Optional[Any] = None,
│        name: Optional[str] = None,
│        langfuse_prompt: Optional[
│            Any
│        ] = None,  # we cannot use prompt because it's an argument of the old OpenAI completions AP
│        langfuse_public_key: Optional[str] = None,
│        trace_id: Optional[str] = None,
│        parent_observation_id: Optional[str] = None,
⋮
│    def get_langfuse_args(self) -> Any:
⋮
│    def get_openai_args(self) -> Any:
⋮
│def _instrument_openai_stream(
│    *,
│    resource: OpenAiDefinition,
│    response: Any,
│    generation: LangfuseGeneration,
│) -> Any:
│    if not hasattr(response, "_iterator"):
│        return LangfuseResponseGeneratorSync(
│            resource=resource,
│            response=response,
│            generation=generation,
⋮
│    def finalize_once() -> None:
⋮
│def _instrument_openai_async_stream(
│    *,
│    resource: OpenAiDefinition,
│    response: Any,
│    generation: LangfuseGeneration,
│) -> Any:
│    if not hasattr(response, "_iterator"):
│        return LangfuseResponseGeneratorAsync(
│            resource=resource,
│            response=response,
│            generation=generation,
⋮
│    async def finalize_once() -> None:
⋮

langfuse/types.py:
⋮
│SpanLevel = Literal["DEBUG", "DEFAULT", "WARNING", "ERROR"]
│
│ScoreDataType = Literal["NUMERIC", "CATEGORICAL", "BOOLEAN", "TEXT", "CORRECTION"]
│
⋮
│ExperimentScoreType = Literal["NUMERIC", "CATEGORICAL", "BOOLEAN"]
│
⋮
│class MaskFunction(Protocol):
│    """A function that masks data.
│
│    Keyword Args:
│        data: The data to mask.
│
│    Returns:
│        The masked data that must be serializable to JSON.
⋮
│    def __call__(self, *, data: Any, **kwargs: Dict[str, Any]) -> Any: ...
│
⋮
│class MaskOtelSpansFunction(Protocol):
│    """Function protocol for export-stage OpenTelemetry span masking.
│
│    `mask_otel_spans` runs after Langfuse decides which spans this client should
│    export and after export-stage media handling has converted supported media
│    payloads into Langfuse media references. It affects only the spans exported
│    by this Langfuse client. If the same OpenTelemetry spans are sent to another
│    exporter, that exporter receives its own unmodified copy.
│
│    The function is synchronous. It usually runs on the OpenTelemetry batch span
│    processor worker thread; during `flush()` and shutdown it may run on the
⋮
│    def __call__(
│        self, *, params: MaskOtelSpansParams
⋮
│class TraceContext(TypedDict):
⋮

tests/support/retry.py:
⋮
│def retry_until_ready(
│    operation: Callable[[], T],
│    *,
│    is_retryable_error: Callable[[Exception], bool] = is_eventual_consistency_error,
│    is_result_ready: Callable[[T], bool] | None = None,
│    timeout_seconds: float = DEFAULT_RETRY_TIMEOUT_SECONDS,
│    interval_seconds: float = DEFAULT_RETRY_INTERVAL_SECONDS,
⋮

tests/unit/test_openai_prompt_extraction.py:
⋮
│def test_openai_value_serialization_fallback_stays_json_safe():
│    class UnknownLeaf:
│        def __str__(self):
⋮
│    class FallbackModel(BaseModel):
│        created_at: datetime
⋮
│        def model_dump(self, *args, **kwargs):
⋮

tests/unit/test_otel.py:
⋮
│class InMemorySpanExporter(SpanExporter):
│    """Simple in-memory exporter to collect spans for testing."""
│
⋮
│    def get_finished_spans(self) -> List[ReadableSpan]:
⋮

tests/unit/test_version.py:
⋮
│def test_package_version_matches_distribution_metadata():
⋮
```