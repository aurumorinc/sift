# Sift

Sift is an API-driven platform for defining, managing, and executing DSPy-based AI agents. It acts as an integration layer between your application, LLMs (via LiteLLM), advanced agentic workflows (via DSPy), and prompt management/observability (via Langfuse).

Sift allows you to define agent configurations, save them to Langfuse, and perform inference against these agents programmatically through a standard Responses API format, complete with built-in asynchronous webhook dispatching capabilities.

## Architecture & Project Structure

Sift is structured as a monorepo consisting of a core Python SDK and a Windmill-based API layer:

- **`packages/sift`**: The core Python SDK containing business logic, integrations, DSPy state hydration, Langfuse persistence, and webhook dispatching.
- **`apps/sift-api`**: The Windmill application layer that exposes the core SDK as HTTP endpoints (`f/sift/agents.py` and `f/sift/responses.py`).

## Core Concepts

1. **Agents**: DSPy predictors defined by a signature (instructions and fields). Sift stores the compiled state (including training data, demos, and instructions) in Langfuse for versioning, clean UI extraction, and observability.
2. **Responses**: Executing an agent configuration against dynamic input, processed through DSPy + LiteLLM, and mapped to standard API responses.
3. **Webhooks**: An event-driven mechanism to receive asynchronous updates on the lifecycle of your API requests (`started`, `completed`, `failed`).

---

## Configuration

Set the following environment variables (which can also be loaded via a `.env` file):

```env
LANGFUSE_PUBLIC_KEY="your-public-key"
LANGFUSE_SECRET_KEY="your-secret-key"
LANGFUSE_HOST="https://cloud.langfuse.com" # Defaults to cloud if not provided
```

---

## API Reference

The API is exposed via Windmill webhooks or script endpoints (e.g., `POST /api/w/workspace/f/sift/agents`).

### 1. Agents API

**Endpoint**: `f/sift/agents`

Used to compile, save, and configure new DSPy agents to Langfuse.

#### Request Payload (`AgentRequest`)

```json
{
  "agent_name": "support_agent",
  "agent_card_params": {},
  "litellm_params": {
    "model": "gpt-4o",
    "temperature": 0.7
  },
  "dspy_params": {
    "optimizer": null,
    "state": {
      "default_predictor": {
        "traces": [],
        "train": [
          {
            "messages": "How do I reset my password?",
            "response": "Please click the 'Forgot Password' link on the login page."
          },
          {
            "messages": "Where are my billing settings?",
            "response": "Billing settings can be found under Account > Billing."
          }
        ],
        "demos": [],
        "signature": {
          "instructions": "You are a helpful customer support agent.",
          "fields": {
            "messages": {"description": "User input"},
            "response": {"description": "Agent output"}
          }
        },
        "lm": null
      }
    }
  },
  "labels": ["support", "production"],
  "webhook": {
    "url": "https://your-server.com/webhook",
    "events": ["started", "completed", "failed"],
    "headers": {"Authorization": "Bearer token"},
    "metadata": {"job_id": "12345"}
  }
}
```

- **`agent_name`** *(str)*: Unique identifier for the agent (saved to Langfuse).
- **`agent_card_params`** *(dict)*: Extraneous metadata for the agent.
- **`litellm_params`** *(dict)*: Configuration for LiteLLM (model, temperature, etc.).
- **`dspy_params`** *(dict)*: The serialized DSPy state representing predictors and instructions.
- **`labels`** *(list, optional)*: Langfuse labels.
- **`webhook`** *(object, optional)*: Webhook configuration for lifecycle events.

#### Response Payload (`AgentResponse`)

Returns the original agent configuration appended with execution success/error state.

```json
{
  "agent_name": "support_agent",
  "agent_card_params": {},
  "litellm_params": {},
  "dspy_params": {},
  "labels": [],
  "webhook": {
    "url": "https://your-server.com/webhook",
    "events": ["started", "completed", "failed"],
    "headers": {"Authorization": "Bearer token"},
    "metadata": {"job_id": "12345"}
  },
  "success": true,
  "error": null
}
```

### 2. Responses API

**Endpoint**: `f/sift/responses`

Executes an existing agent against user input.

#### Request Payload (`ResponseRequest`)

```json
{
  "model": "a2a_agent/support_agent",
  "input": "How do I reset my password?",
  "background": false,
  "webhook": {
    "url": "https://your-server.com/webhook",
    "events": ["completed", "failed"]
  }
}
```

- **`model`** *(str)*: The ID of the agent to execute (matches the `agent_name` saved via Agents API). The prefix `a2a_agent/` is optionally supported and automatically stripped.
- **`input`** *(str | list)*: The input data sent to the agent.
- **`background`** *(bool, optional)*: Whether the inference is running as a background task. Defaults to `false`.
- **`webhook`** *(object, optional)*: Webhook configuration for execution lifecycle.

#### Response Payload (`ResponseResponse`)

Returns a LiteLLM compliant `ResponsesAPIResponse` wrapper.

```json
{
  "success": true,
  "error": null,
  "webhook": {
    "url": "https://your-server.com/webhook",
    "events": ["completed", "failed"]
  },
  "response": {
    "id": "resp_abc123",
    "object": "response",
    "created_at": 1718000000,
    "model": "support_agent",
    "status": "completed",
    "output": [
      {
        "content": [
          {
            "type": "output_text",
            "text": "To reset your password, click the 'Forgot Password' link on the login page."
          }
        ]
      }
    ],
    "usage": {
      "input_tokens": 0,
      "output_tokens": 0,
      "total_tokens": 0
    }
  }
}
```

---

## Webhooks

Sift utilizes an event-driven webhook decorator (`@webhook_dispatch`) to handle asynchronous lifecycle notifications.

If a `webhook` object is provided in a request payload, Sift will `POST` lifecycle events to the target `url`.

### Webhook Event Types

- **`started`**: Dispatched before the API begins processing the request.
- **`completed`**: Dispatched upon successful completion, containing the full response payload.
- **`failed`**: Dispatched if an exception occurs, containing the error message.

### Webhook Payload Format

```json
{
  "event": "completed",
  "payload": {
     // The full ResponseResponse or AgentResponse object
  },
  "metadata": {
     // User-defined data echoed back from the original webhook request definition
  }
}
```

---

## Python Client SDK

For internal programmatic usage or extension, Sift provides a Python facade client:

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
    # ... other AgentRequest params
}
client.compile_and_save_agent(agent_payload)
```
