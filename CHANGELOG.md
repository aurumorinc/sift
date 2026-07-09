# Changelog v0.13.0

## Breaking Changes

*   **Flattened API Response Structure**
    The intermediate `response` key has been removed from all API responses, promoting nested fields to the top level of the JSON payload.
    *   **Migration:** Update your API client integrations to access fields directly at the root level of the response object instead of nesting them under `response`.
    *   **Commits:** [1a9a5c1](https://github.com/aurumorinc/sift/commit/1a9a5c1a), [4005e42](https://github.com/aurumorinc/sift/commit/4005e423), [adfd078](https://github.com/aurumorinc/sift/commit/adfd0785)

## Features

*   **Agent Configuration Support**
    Added support for granular agent configuration, including rate limiting (TPM/RPM), custom header configuration, and DSPy parameters.
    *   **Commits:** [1a9a5c1](https://github.com/aurumorinc/sift/commit/1a9a5c1a), [4005e42](https://github.com/aurumorinc/sift/commit/4005e423), [adfd078](https://github.com/aurumorinc/sift/commit/adfd0785)

*   **Enhanced Webhook Schema**
    Added an optional `data` field to the webhook schema to support `AgentResponse` and `ResponseResponse` objects, including improved type hinting for better integration support.
    *   **Commits:** [4e57266](https://github.com/aurumorinc/sift/commit/4e57266e)
