# Changelog v0.5.0

## Features

### Agent Compilation
*   Implemented new services for agent creation and compilation, featuring native DSPy integration.
    *   Commits: [e95a715](https://github.com/aurumorinc/sift/commit/e95a715c), [930019e](https://github.com/aurumorinc/sift/commit/930019e9)

### Inference Services
*   Added a new inference endpoint designed for streamlined response processing.
    *   Commit: [025c79a](https://github.com/aurumorinc/sift/commit/025c79a2)
*   Implemented safe agent retrieval logic within the inference service layer.
    *   Commits: [7af8723](https://github.com/aurumorinc/sift/commit/7af87236), [72cb680](https://github.com/aurumorinc/sift/commit/72cb680c)

### Webhook Dispatching
*   Added dedicated services for webhook dispatching to support external event triggers.
    *   Commit: [e95a715](https://github.com/aurumorinc/sift/commit/e95a715c)
*   Implemented configuration merging logic for webhook payloads.
    *   Commit: [930019e](https://github.com/aurumorinc/sift/commit/930019e9)

## Improvements

### API Architecture
*   Refactored API handlers to delegate business logic to dedicated use case services, improving modularity and maintainability.
    *   Commit: [6aff563](https://github.com/aurumorinc/sift/commit/6aff563e)

## Infrastructure

### API Documentation
*   Added OpenAPI specification to provide structured API documentation.
    *   Commit: [539eb1a](https://github.com/aurumorinc/sift/commit/539eb1a4)
*   Included initial agent and response script definitions within the OpenAPI schema.
    *   Commit: [5fb0e8c](https://github.com/aurumorinc/sift/commit/5fb0e8c8)

## Other

### Testing
*   Added comprehensive unit and integration tests covering core agent workflows.
    *   Commit: [a123198](https://github.com/aurumorinc/sift/commit/a1231989)
*   Updated pytest configuration to support the new testing architecture.
    *   Commit: [6081844](https://github.com/aurumorinc/sift/commit/60818448)
