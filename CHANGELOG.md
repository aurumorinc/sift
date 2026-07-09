# Changelog v0.11.0

## Features

* **Sparse Payload Support**
  Implemented support for Agent schema and DSPy states while maintaining backward compatibility.
  Commits: [d34fbd0](https://github.com/aurumorinc/sift/commit/d34fbd01), [3b04c61](https://github.com/aurumorinc/sift/commit/3b04c612), [9bba7fe](https://github.com/aurumorinc/sift/commit/9bba7feb)

* **Model Fallbacks**
  Added `gemini/gemini-3.1-flash-lite` as a default model to prevent validation errors during model initialization.
  Commits: [d34fbd0](https://github.com/aurumorinc/sift/commit/d34fbd01), [3b04c61](https://github.com/aurumorinc/sift/commit/3b04c612), [9bba7fe](https://github.com/aurumorinc/sift/commit/9bba7feb)

## Improvements

* **Schema Refactoring**
  Updated model fields to utilize `default_factory` and simplified the internal agent initialization logic.
  Commits: [d34fbd0](https://github.com/aurumorinc/sift/commit/d34fbd01), [3b04c61](https://github.com/aurumorinc/sift/commit/3b04c612), [9bba7fe](https://github.com/aurumorinc/sift/commit/9bba7feb)

* **Integration Testing**
  Added comprehensive test coverage for edge cases, specifically targeting empty payloads and null overrides.
  Commits: [d34fbd0](https://github.com/aurumorinc/sift/commit/d34fbd01), [3b04c61](https://github.com/aurumorinc/sift/commit/3b04c612), [9bba7fe](https://github.com/aurumorinc/sift/commit/9bba7feb)

## Fixes

* **Windmill Integration Compatibility**
  Resolved platform-specific bugs to ensure stability when running within the Windmill environment.
  Commits: [d34fbd0](https://github.com/aurumorinc/sift/commit/d34fbd01), [3b04c61](https://github.com/aurumorinc/sift/commit/3b04c612), [9bba7fe](https://github.com/aurumorinc/sift/commit/9bba7feb)
