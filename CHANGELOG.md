# Changelog v0.2.0

## Breaking Changes

*   **Namespace Refactor: Renamed project namespace from `lume` to `worldline`**
    The project namespace has been migrated from `lume` to `worldline` across all source files.
    *   **Migration Path:** Update all import statements, configuration files, and references in your codebase from `lume` to `worldline`.
    *   Commit: [ddee120](https://github.com/aurumorinc/sift/commit/ddee1206)

## New Features

*   **Sift API Implementation**
    Introduced the `SiftClient` to facilitate core API interactions.
    *   Commit: [866ae9b](https://github.com/aurumorinc/sift/commit/866ae9b2)
*   **DSPy Agent Modules**
    Added support for DSPy agent modules to enhance agentic workflows.
    *   Commit: [9b81da2](https://github.com/aurumorinc/sift/commit/9b81da23)
*   **Langfuse Observability**
    Integrated Langfuse for improved tracing and observability of agent operations.
    *   Commit: [812e187](https://github.com/aurumorinc/sift/commit/812e1877)
*   **Webhook Support**
    Added native webhook support for event-driven integrations.
    *   Commit: [812e187](https://github.com/aurumorinc/sift/commit/812e1877)

## Improvements

*   **Runtime Configuration Namespace**
    Defined the `RT` namespace to provide type-safe handling for external service integrations and authentication.
    *   Commit: [180c9de](https://github.com/aurumorinc/sift/commit/180c9dea)

## Infrastructure

*   **Project Workspace Initialization**
    Initialized the workspace with PDM lockfiles and standardized dependency management.
    *   Commit: [c98d77a](https://github.com/aurumorinc/sift/commit/c98d77ad)
*   **Dependency Management Configuration**
    Completed initial PDM lockfile and dependency setup.
    *   Commit: [e35228e](https://github.com/aurumorinc/sift/commit/e35228e7)
*   **Workspace Dependency Structure**
    Finalized workspace dependency management configurations.
    *   Commit: [175a529](https://github.com/aurumorinc/sift/commit/175a5295)
*   **Windmill Workspace Settings**
    Configured Windmill workspace settings and folder permissions.
    *   Commit: [ca62ade](https://github.com/aurumorinc/sift/commit/ca62ade3)
*   **Windmill Ignore Patterns**
    Implemented ignore patterns for Windmill workspace synchronization.
    *   Commit: [8ae71e0](https://github.com/aurumorinc/sift/commit/8ae71e02)
*   **Windmill Configuration Refinement**
    Refined Windmill workspace configuration and permissions.
    *   Commit: [c1528f9](https://github.com/aurumorinc/sift/commit/c1528f9c)
*   **CI/CD Release Workflow**
    Configured the automated release workflow.
    *   Commit: [e340591](https://github.com/aurumorinc/sift/commit/e3405910)
*   **Gemini API Secret Management**
    Updated secret management protocols for Gemini API integrations.
    *   Commit: [a56d408](https://github.com/aurumorinc/sift/commit/a56d408f)
*   **CI/CD Pipeline Updates**
    General updates to CI/CD pipeline configurations.
    *   Commit: [595d1c6](https://github.com/aurumorinc/sift/commit/595d1c69)
*   **Package Versioning**
    Added package versioning metadata.
    *   Commit: [ef7c02a](https://github.com/aurumorinc/sift/commit/ef7c02a7)
*   **Runemodule Registration**
    Implemented runemodule registration for the package.
    *   Commit: [786f098](https://github.com/aurumorinc/sift/commit/786f0985)
*   **Gitignore Updates**
    Updated `.gitignore` to support new project structure.
    *   Commit: [96cf310](https://github.com/aurumorinc/sift/commit/96cf3104)

## Documentation

*   **Project Documentation**
    Added foundational project documentation.
    *   Commit: [494286f](https://github.com/aurumorinc/sift/commit/494286f5)
*   **Engineering Standards and PR Templates**
    Added pull request templates and defined engineering standards.
    *   Commit: [498d006](https://github.com/aurumorinc/sift/commit/498d006d)
*   **Agent Skill Definitions**
    Documented agent skill definitions for developer reference.
    *   Commit: [2a7c4d5](https://github.com/aurumorinc/sift/commit/2a7c4d5f)
