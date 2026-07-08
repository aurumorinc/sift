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

Sift is hosted via Windmill, making it fully accessible through HTTP endpoints. Below you will find the detailed documentation for all supported endpoints, data models, and webhooks.

### Generating the OpenAPI Schema
A static, machine-readable OpenAPI schema is provided in the repository root at [`openapi.yaml`](openapi.yaml). 
If you update the python scripts, you can fetch the live, dynamically generated OpenAPI specification directly from the Windmill API using `curl`:

```bash
curl -H "Authorization: Bearer $WML_TOKEN" \
     https://windmill.aurumor.com/api/w/aurumor/openapi.yaml > openapi.yaml
```

### Authentication & Base URL
- **Authentication**: All API requests to Windmill require a Bearer token. Provide it via the `Authorization: Bearer <TOKEN>` header.
- **Base URL**: The default Sift deployment is located at `https://windmill.aurumor.com/api/w/aurumor`.
- **Windmill Job Runs**: To run a Windmill script synchronously and wait for the result, use the path format: `/jobs/run/wait/result/p/f/sift/<script-name>`.

---

### 1. Create / Compile Agent

**Endpoint:** `POST /jobs/run/wait/result/p/f/sift/agents`

Compiles, saves, and configures new DSPy agents to Langfuse. **All fields in the payload are optional.**
- If `agent_name` is omitted, Sift will auto-generate a new UUID for the agent.
- If `agent_name` matches an existing agent, Sift will perform a **deep merge** with the agent's historical state. This means you only need to provide the fields you want to override (e.g., just updating the `optimizer`, `litellm_params`, or `train` dataset), and Sift will preserve the rest of your agent's configuration and trigger re-optimization automatically.
- If creating a new agent with only `train` data and no explicit `signature.fields`, Sift will automatically infer the inputs and outputs from your dataset.

#### Example Request: Synchronous (cURL)

```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/agents" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "support_agent",
    "agent_card_params": {},
    "litellm_params": {
      "model": "gpt-4o",
      "temperature": 0.7
    },
    "dspy_params": {
      "optimizer": "BootstrapFewShot",
      "optimizer_params": {
        "max_bootstrapped_demos": 4,
        "max_labeled_demos": 16
      },
      "state": {
        "default_predictor": {
          "traces": [],
          "train": [
            {
              "messages": "How do I reset my password?",
              "response": "Please click the '\''Forgot Password'\'' link on the login page.",
              "score": 1.0,
              "feedback": "Clear and concise."
            }
          ],
          "demos": [],
          "signature": {
            "instructions": "You are a helpful customer support agent.",
            "fields": [
              {"name": "messages", "json_schema_extra": {"desc": "User input", "__dspy_field_type": "input"}},
              {"name": "response", "json_schema_extra": {"desc": "Agent output", "__dspy_field_type": "output"}}
            ]
          },
          "lm": null
        }
      }
    },
    "labels": ["support", "production"]
  }'
```

#### Example Request: Compile/Optimize using only Train Data (Python)

If you omit the `optimizer` configurations and only provide `train` data, Sift automatically defaults to compiling your agent using those static examples (via `BootstrapFewShot`).

```python
import requests

url = "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/agents"
headers = {"Authorization": "Bearer YOUR_WML_TOKEN", "Content-Type": "application/json"}

# Because of the deep merge and auto-inference features, you only need to provide
# the fields you actually want to configure or override.
payload = {
    "agent_name": "train_data_agent",
    "dspy_params": {
        "state": {
            "default_predictor": {
                "train": [
                    {
                        "messages": "What is the capital of France?",
                        "response": "Paris.",
                        "score": 1.0
                    },
                    {
                        "messages": "How many ounces in a cup?",
                        "response": "There are 8 fluid ounces in a cup.",
                        "score": 1.0
                    }
                ],
                # If creating a brand new agent, Sift can infer fields if omitted.
                # If updating an existing agent, Sift will deep-merge this train
                # data and automatically re-optimize using the existing signature.
            }
        }
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

#### Example Request: Asynchronous with Webhook (Python)

```python
import requests

url = "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/agents"
headers = {
    "Authorization": "Bearer YOUR_WML_TOKEN",
    "Content-Type": "application/json"
}

payload = {
    "agent_name": "async_support_agent",
    "agent_card_params": {},
    "litellm_params": {"model": "gpt-4o"},
    "dspy_params": {
        "state": {
            "default_predictor": {
                "signature": {
                    "instructions": "You are a helpful assistant.",
                    "fields": {}
                }
            }
        }
    },
    "webhook": {
        "url": "https://your-server.com/webhook",
        "events": ["started", "completed", "failed"],
        "headers": {"Authorization": "Bearer internal-secret-token"},
        "metadata": {"user_id": "123"}
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

#### Example Response
Returns the original agent configuration appended with execution success/error state.

```json
{
  "agent_name": "support_agent",
  "agent_card_params": {},
  "litellm_params": {
    "model": "gpt-4o",
    "temperature": 0.7
  },
  "dspy_params": {
    "optimizer": "BootstrapFewShot",
    "state": {}
  },
  "labels": ["support", "production"],
  "webhook": null,
  "success": true,
  "error": null
}
```

---

### 2. Predict Response

**Endpoint:** `POST /jobs/run/wait/result/p/f/sift/responses`

Executes an existing agent against user input and returns a standard API response.

#### Example Request: Synchronous Text Input (cURL)

```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/responses" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "a2a_agent/support_agent",
    "input": "How do I reset my password?",
    "background": false
  }'
```

#### Example Request: Synchronous Messages Array Input (cURL)

```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/responses" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "support_agent",
    "input": [
      {"role": "system", "content": "You are a support bot."},
      {"role": "user", "content": "Where are my billing settings?"}
    ],
    "background": false
  }'
```

#### Example Request: Synchronous Multimodal Input (cURL)

```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/responses" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vision_agent",
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What is the primary color in this image?"},
          {
            "type": "image_url",
            "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Synthese%2B.svg/200px-Synthese%2B.svg.png"}
          }
        ]
      }
    ],
    "background": false
  }'
```

#### Example Request: Asynchronous Background Request (Python)

If `background` is true, the server can acknowledge the request quickly, and the heavy processing will send the result back to your webhook URL.

```python
import requests

url = "https://windmill.aurumor.com/api/w/aurumor/jobs/run/wait/result/p/f/sift/responses"
headers = {"Authorization": "Bearer YOUR_WML_TOKEN"}

payload = {
    "model": "a2a_agent/support_agent",
    "input": "Can you generate a massive report?",
    "background": True,
    "webhook": {
        "url": "https://your-server.com/webhook",
        "events": ["completed", "failed"]
    }
}

requests.post(url, json=payload, headers=headers)
```

#### Example Response
Returns a wrapper containing success states and a LiteLLM/OpenAI-compliant response object.

```json
{
  "success": true,
  "error": null,
  "webhook": null,
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
      "input_tokens": 12,
      "output_tokens": 18,
      "total_tokens": 30
    }
  }
}
```

---

## 🪝 Webhooks Reference

Sift utilizes an event-driven webhook decorator (`@webhook_dispatch`) to handle asynchronous lifecycle notifications. When you provide a `webhook` object in your request payload, Sift will `POST` lifecycle events to the target `url`.

### Lifecycle Events
- **`started`**: Dispatched immediately before the API begins processing the request. Contains the original request arguments.
- **`completed`**: Dispatched upon successful completion. Contains the full response payload (e.g., `AgentResponse` or `ResponseResponse`).
- **`failed`**: Dispatched if an exception occurs during execution. Contains the error message and the failed response payload.

### Webhook Payload Example

When Sift fires a webhook to your server, the `POST` payload will look like this:

```json
{
  "event": "completed",
  "payload": {
    "success": true,
    "error": null,
    "response": {
       "id": "resp_123",
       "output": [{"content": [{"text": "Completed task!"}]}]
    },
    "webhook": {
      "url": "https://your-server.com/webhook",
      "events": ["started", "completed", "failed"],
      "metadata": {"job_id": "999"}
    }
  },
  "metadata": {
    "job_id": "999"
  }
}
```

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
            "default_predictor": {
                "signature": {
                    "instructions": "You are a comedian.",
                    "fields": {}
                }
            }
        }
    },
    "litellm_params": {},
    "agent_card_params": {}
}
client.compile_and_save_agent(agent_payload)
```
