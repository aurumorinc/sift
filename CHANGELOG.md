# Changelog v0.11.1

## Documentation

*   **Simplified API Documentation Examples**
    Removed optional and empty fields (`agent_card_params`, `litellm_params`, `fields`) from documentation examples to improve clarity and reduce noise.
    Commits: [c52fa80](https://github.com/aurumorinc/sift/commit/c52fa80f)

*   **Updated OpenAPI Schema Definitions**
    Explicitly marked `agent_card_params`, `litellm_params`, and `fields` as optional within the OpenAPI schema to ensure client-side code generators handle these fields correctly.
    Commits: [92f5e28](https://github.com/aurumorinc/sift/commit/92f5e284)
