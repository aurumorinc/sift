# Changelog v0.12.0

## Breaking Changes

*   **API Endpoint Renaming**
    The endpoint `/jobs/run/wait/result/` has been renamed to `/jobs/run_wait_result/`. Please update all client-side integrations to point to the new route. ([88a33c1](https://github.com/aurumorinc/sift/commit/88a33c11))

*   **LLM Request Schema Updates**
    The LLM provider request payload now requires the following parameters: `instructions`, `max_output_tokens`, `metadata`, and `parallel_tool_calls`. Ensure your request bodies are updated to include these fields to avoid validation errors. ([88a33c1](https://github.com/aurumorinc/sift/commit/88a33c11))

## New Features

*   **Expanded LLM Request Parameters**
    Added support for `instructions`, `max_output_tokens`, `metadata`, and `parallel_tool_calls` in LLM requests to provide greater control over model behavior. ([88a33c1](https://github.com/aurumorinc/sift/commit/88a33c11))

*   **Langfuse Configuration Support**
    Added `langfuse_base_url` to the configuration options to support custom Langfuse instances. ([1de142a](https://github.com/aurumorinc/sift/commit/1de142ae), [3d02acc](https://github.com/aurumorinc/sift/commit/3d02acc9))

*   **Parameterized Windmill Integration**
    Added support for parameterized Windmill base URL and workspace configuration. ([1de142a](https://github.com/aurumorinc/sift/commit/1de142ae), [3d02acc](https://github.com/aurumorinc/sift/commit/3d02acc9))

## Documentation

*   **API Reference Updates**
    Updated documentation to reflect the endpoint migration from `/jobs/run/wait/result/` to `/jobs/run_wait_result/`. ([1de142a](https://github.com/aurumorinc/sift/commit/1de142ae), [3d02acc](https://github.com/aurumorinc/sift/commit/3d02acc9))

## Other

*   **Dependency Updates**
    Updated the OpenAI library from version 2.44.0 to 2.45.0. ([1de142a](https://github.com/aurumorinc/sift/commit/1de142ae), [3d02acc](https://github.com/aurumorinc/sift/commit/3d02acc9))

*   **Internal Dependency Updates**
    Updated internal sift dependencies to ensure compatibility with the latest changes. ([1de142a](https://github.com/aurumorinc/sift/commit/1de142ae), [3d02acc](https://github.com/aurumorinc/sift/commit/3d02acc9))
