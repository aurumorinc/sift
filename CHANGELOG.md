# Changelog v0.4.0

## Features

* **Agent Name Auto-generation**
  The `Agent` model now automatically assigns a default UUID to the `agent_name` field upon initialization, ensuring unique identifiers without requiring manual input. (Commit: [7c3835a](https://github.com/aurumorinc/sift/commit/7c3835a3))

## Improvements

* **Webhook Decorator Robustness**
  Refactored the webhook decorator to utilize `inspect.signature` for more reliable argument binding and consistent payload extraction. (Commits: [01a18fa](https://github.com/aurumorinc/sift/commit/01a18fa3), [2da438e](https://github.com/aurumorinc/sift/commit/2da438ef), [e1e20c4](https://github.com/aurumorinc/sift/commit/e1e20c45))
