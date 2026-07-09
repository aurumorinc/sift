# Changelog v0.8.0

## Breaking Changes

*   **Unsafe LM State Loading Support**
    The `load_state` method has been updated to require explicit permission for unsafe state loading.
    *   **Migration:** Update existing calls to `load_state` to include the new `allow_unsafe_lm_state` parameter. If your implementation requires unsafe state loading, you must explicitly set `allow_unsafe_lm_state=True`.
    *   Commit: [498a1fd](https://github.com/aurumorinc/sift/commit/498a1fd91)

## Improvements

*   **Centralization of Metric Logic**
    Consolidated metric logic and LLM judge evaluation into dedicated service modules to improve modularity.
    *   Commits: [9b09f87](https://github.com/aurumorinc/sift/commit/9b09f87d), [1995940](https://github.com/aurumorinc/sift/commit/1995940e), [1965a21](https://github.com/aurumorinc/sift/commit/1965a2171)
*   **Codebase Structural Refactoring**
    Reorganized type definitions and file structure to enhance maintainability and code navigation.
    *   Commits: [df078db](https://github.com/aurumorinc/sift/commit/df078dbe), [1422d4c](https://github.com/aurumorinc/sift/commit/1422d4cc14), [1783bad](https://github.com/aurumorinc/sift/commit/1783badc76)
*   **Agent Logic Restructuring**
    Moved webhook-decorated functions to `use_cases` and consolidated core agent logic.
    *   Commit: [18d92ce](https://github.com/aurumorinc/sift/commit/18d92ce834)

## Bug Fixes

*   **Robust Model Serialization**
    Updated test assertions to ensure compatibility with both Pydantic v1 and v2, and improved internal type hints.
    *   Commits: [5f99d6c](https://github.com/aurumorinc/sift/commit/5f99d6c04), [6034937](https://github.com/aurumorinc/sift/commit/6034937e6), [77c74f8](https://github.com/aurumorinc/sift/commit/77c74f8a56)

## Infrastructure

*   **Dependency Management Updates**
    Added `pytest-asyncio` and `pytest-cov` to the test suite and updated project lock files.
    *   Commits: [11e417c](https://github.com/aurumorinc/sift/commit/11e417c20a), [1281bf5](https://github.com/aurumorinc/sift/commit/1281bf586f)

## Documentation

*   **API Examples and Variations**
    Added documentation covering multimodal training workflows and dynamic optimizer selection.
    *   Commits: [13cf0f6](https://github.com/aurumorinc/sift/commit/13cf0f6079), [15ae4bd](https://github.com/aurumorinc/sift/commit/15ae4bd2d0), [163da26](https://github.com/aurumorinc/sift/commit/163da26956)

## Other

*   **Comprehensive Testing Suite**
    Added new unit and integration tests covering client operations and multimodal data handling.
    *   Commits: [3299594](https://github.com/aurumorinc/sift/commit/32995940e), [8269c5b](https://github.com/aurumorinc/sift/commit/8269c5bdd), [108d412](https://github.com/aurumorinc/sift/commit/108d412d5e)
