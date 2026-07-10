# Sift

Sift is an API-driven platform for defining, managing, and executing DSPy-based AI agents. It acts as an integration layer between your application, LLMs (via LiteLLM), advanced agentic workflows (via DSPy), and prompt management/observability (via Langfuse).

Sift allows you to define agent configurations, save them to Langfuse, and perform inference against these agents programmatically through a standard Responses API format, complete with built-in asynchronous webhook dispatching capabilities.

---

## 🏗️ Architecture & Project Structure

Sift is structured as a monorepo consisting of a core Python SDK and a Windmill-based API layer:

- **`packages/sift`**: The core Python SDK containing business logic, integrations, DSPy state hydration, Langfuse persistence, and webhook dispatching.
- **`apps/sift-api`**: The Windmill application layer that exposes the core SDK as HTTP endpoints ([`f/sift/agents.py`](apps/sift-api/f/sift/agents.py) and [`f/sift/responses.py`](apps/sift-api/f/sift/responses.py)).

## 🧠 Core Concepts

1. **Agents**: DSPy predictors defined by a signature (instructions and fields). Sift stores the compiled state (including training data, demos, and instructions) in Langfuse for versioning, clean UI extraction, and observability.
2. **Responses**: Executing an agent configuration against dynamic input, processed through DSPy + LiteLLM, and mapped to standard API responses.
3. **Webhooks**: An event-driven mechanism to receive asynchronous updates on the lifecycle of your API requests (`started`, `completed`, `failed`).

---

## ⚙️ Configuration & Getting Started

Set the following environment variables (which can also be loaded via a `.env` file):

```env
LANGFUSE_PUBLIC_KEY="your-public-key"
LANGFUSE_SECRET_KEY="your-secret-key"
LANGFUSE_HOST="https://cloud.langfuse.com" # Defaults to cloud if not provided
```

---

## 📖 API Reference

For detailed documentation on the available API endpoints, full JSON data schemas (for Agents, Responses, and Webhooks), and exact request/response webhook callback examples, please see the [**API Reference Guide**](docs/api-reference.md).

---

## 🐍 Python Client SDK

For internal programmatic usage or deep extension, Sift provides a Python facade client built directly into the SDK:

```python
from sift import SiftClient
from sift.modules.agents.schema import AgentRequest

client = SiftClient()

# Execute Response Inference
response = client.predict_response(
    agent_id="support_agent",
    input="Tell me a joke",
    background=False
)
print(response.output[0]["content"][0]["text"])

# Compile and Save Agent
agent_payload = {
    "agent_name": "joke_agent",
    "dspy_params": {
        "state": {
            "predict": {
                "signature": {
                    "instructions": "You are a comedian."
                }
            }
        }
    }
}
client.compile_and_save_agent(agent_payload)
```
