# Changelog v0.9.0

## Breaking Changes

*   **Windmill API Endpoint Path Update**
    The Windmill API endpoints have been updated to the new path format `/jobs/run_wait_result/p/f/...`. You must update all existing calls to the Windmill API to reflect this new structure.
    *   Commit: [0376d14](https://github.com/aurumorinc/sift/commit/0376d148)

*   **Removal of Windmill Base URL Fallback**
    The default fallback for `WINDMILL_BASE_URL` has been removed. You must now explicitly set the `WINDMILL_BASE_URL` environment variable in your configuration to ensure successful API connectivity.
    *   Commit: [0376d14](https://github.com/aurumorinc/sift/commit/0376d148)

## Features

*   **Workspace Configuration Schema**
    Added formal schema definitions for environment variables to improve configuration validation.
    *   Commits: [e3ed77b](https://github.com/aurumorinc/sift/commit/e3ed77b1), [85d7ca3](https://github.com/aurumorinc/sift/commit/85d7ca3b), [8aa56dd](https://github.com/aurumorinc/sift/commit/8aa56ddc)

*   **Automatic Environment Variable Propagation**
    Implemented automatic propagation for workspace configuration variables to streamline environment setup.
    *   Commits: [e3ed77b](https://github.com/aurumorinc/sift/commit/e3ed77b1), [85d7ca3](https://github.com/aurumorinc/sift/commit/85d7ca3b), [8aa56dd](https://github.com/aurumorinc/sift/commit/8aa56ddc)

## Fixes

*   **Codebase Standardization**
    Resolved missing imports and standardized code formatting across the repository to improve maintainability.
    *   Commit: [1faa062](https://github.com/aurumorinc/sift/commit/1faa062e)

## Other

*   **Integration Testing Suite**
    Implemented comprehensive integration tests, including the use of VCR cassettes to ensure reliable and reproducible test scenarios.
    *   Commit: [9831244](https://github.com/aurumorinc/sift/commit/98312440)
