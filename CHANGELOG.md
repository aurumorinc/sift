# Changelog v0.15.0

## Breaking Changes

*   **Removal of Webhook Utilities**
    The following classes and functions have been removed from the public API: `WebhookRequest`, `WebhookEvent`, `dispatch_webhook`, and `webhook_dispatch`.
    *   **Migration Path:** Replace all instances of these utilities with the equivalent functionality provided by the newly integrated `oort` package.
    *   **Commits:** [0c715a3](https://github.com/aurumorinc/sift/commit/0c715a36), [c4fd44d](https://github.com/aurumorinc/sift/commit/c4fd44da), [5a1f136](https://github.com/aurumorinc/sift/commit/5a1f1369)

## Features

*   **Oort Integration**
    Integrated the `oort-python` dependency to provide enhanced capabilities for AST mapping, S3 file handling, and configuration management.
    *   **Commits:** [84b6bef](https://github.com/aurumorinc/sift/commit/84b6befc), [f420fba](https://github.com/aurumorinc/sift/commit/f420fbab), [b457838](https://github.com/aurumorinc/sift/commit/b4578382)

## Infrastructure

*   **VCR Cassette Implementation**
    Added VCR cassettes to the test suite to enable reliable, offline integration testing.
    *   **Commits:** [64e4390](https://github.com/aurumorinc/sift/commit/64e4390b)
*   **Gemini API Configuration**
    Configured necessary headers for the Gemini API to support secure and authenticated requests.
    *   **Commits:** [7965821](https://github.com/aurumorinc/sift/commit/79658212)
