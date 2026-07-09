# Changelog v0.10.0

## Breaking Changes

* **API Endpoint Structure Update**
  All API endpoints now require a workspace identifier in the URL path. You must update your API client calls to include this identifier (e.g., `/api/v1/resource` becomes `/api/v1/{workspace}/resource`). Ensure the `WINDMILL_WORKSPACE` environment variable is configured in your deployment environment.
  Commit: [4d45212](https://github.com/aurumorinc/sift/commit/4d452129)

* **Fixture Renaming**
  The `check_token` fixture has been renamed to `check_env`. Please update your test suites to reference the new fixture name.
  Commit: [4d45212](https://github.com/aurumorinc/sift/commit/4d452129)

## Fixes

* **Test Validation Assertions**
  Added explicit Content-Type JSON assertions to all test cases to ensure strict API response validation.
  Commit: [4d45212](https://github.com/aurumorinc/sift/commit/4d452129)

## Other

* **Dependency Updates**
  Updated `huggingface-hub` to 1.23.0 and `sift` to the latest version.
  Commits: [0cb1790](https://github.com/aurumorinc/sift/commit/0cb17900), [745f3bc](https://github.com/aurumorinc/sift/commit/745f3bc2), [559072f](https://github.com/aurumorinc/sift/commit/559072f2)

* **New Dependency Additions**
  Added `wmill` 1.753.0 and `windmill-api` to the project dependencies.
  Commits: [0cb1790](https://github.com/aurumorinc/sift/commit/0cb17900), [745f3bc](https://github.com/aurumorinc/sift/commit/745f3bc2), [559072f](https://github.com/aurumorinc/sift/commit/559072f2)

* **Code Import Corrections**
  Added missing `os` module imports to the agents and responses modules to resolve runtime import errors.
  Commits: [0cb1790](https://github.com/aurumorinc/sift/commit/0cb17900), [745f3bc](https://github.com/aurumorinc/sift/commit/745f3bc2), [559072f](https://github.com/aurumorinc/sift/commit/559072f2)
