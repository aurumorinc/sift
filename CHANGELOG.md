# Changelog v0.7.0

## Breaking Changes

* **Refactored `predict_response` API**
  The `predict_response` method has been refactored to utilize a `ResponseRequest` object, enabling support for arbitrary keyword arguments and flexible message/response types.
  * **Migration Guide:** Replace direct positional argument calls to `predict_response(arg1, arg2)` with `predict_response(ResponseRequest(arg1=..., arg2=...))`. Additionally, update any downstream logic handling return types to accommodate the new flexible string/dict response format.
  * **Commits:** [f5e4fc4](https://github.com/aurumorinc/sift/commit/f5e4fc4d), [0c27423](https://github.com/aurumorinc/sift/commit/0c27423c), [c0f6626](https://github.com/aurumorinc/sift/commit/c0f66262)

## Documentation

* **Updated `AGENTS.md` file organization**
  Refined the structure of `AGENTS.md` to improve navigation and clarity for developers.
  * **Commits:** [6760214](https://github.com/aurumorinc/sift/commit/6760214a)

* **Added Python rule files and JSON output examples**
  Expanded the README documentation to include new Python rule file definitions and concrete JSON output examples.
  * **Commits:** [7ae3559](https://github.com/aurumorinc/sift/commit/7ae3559f)
