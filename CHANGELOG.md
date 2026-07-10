# Changelog v0.14.0

## Breaking Changes

*   **Webhook Dispatch Refactor**
    The webhook dispatching mechanism has transitioned from an event-based model to a payload-based approach using `WebhookRequest` and `WebhookResponse` objects. Additionally, the `webhook` field has been removed from `AgentResponse` and `ResponseResponse` objects.
    *   **Migration Path:** Update all webhook consumers to accept the new `WebhookRequest` payload structure. Remove any references to the `webhook` field in `AgentResponse` and `ResponseResponse` objects. If you are using the `webhook_dispatch` decorator, update your implementations to utilize the new `event_prefix` parameter for routing.
    *   **Commits:** [8ecdd2b](https://github.com/aurumorinc/sift/commit/8ecdd2b4), [7844674](https://github.com/aurumorinc/sift/commit/78446742), [4497cbc](https://github.com/aurumorinc/sift/commit/4497cbcf)

## Infrastructure

*   **Codebase Restructuring**
    Reorganized test directories and relocated type definitions and utilities to resolve circular dependency issues.
    *   **Commits:** [4f8eefe](https://github.com/aurumorinc/sift/commit/4f8eefe7)

## Docs

*   **API Documentation Updates**
    Created `docs/api-reference.md` and updated `openapi.yaml` to accurately reflect the schema changes introduced in this release.
    *   **Commits:** [19db9c0](https://github.com/aurumorinc/sift/commit/19db9c0f)
