# Changelog v0.14.2

## Improvements

### Codebase Architecture
*   Refactored type definitions and utility functions to resolve circular dependency issues within the core package.
    *   Commits: [31f6fbd](https://github.com/aurumorinc/sift/commit/31f6fbd6), [45c1098](https://github.com/aurumorinc/sift/commit/45c10980), [6d9edb9](https://github.com/aurumorinc/sift/commit/6d9edb98)
*   Replaced the `worldline` structlog re-export with direct imports to improve dependency clarity and reduce package coupling.
    *   Commits: [31f6fbd](https://github.com/aurumorinc/sift/commit/31f6fbd6), [45c1098](https://github.com/aurumorinc/sift/commit/45c10980), [6d9edb9](https://github.com/aurumorinc/sift/commit/6d9edb98)
