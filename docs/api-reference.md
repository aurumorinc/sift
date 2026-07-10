# API Reference

Sift is hosted via Windmill, making it fully accessible through HTTP endpoints. Below you will find the detailed documentation for all supported endpoints, data models, and webhooks.

## Generating the OpenAPI Schema
A static, machine-readable OpenAPI schema is provided in the repository root at [`openapi.yaml`](../openapi.yaml). 
If you update the python scripts, you can fetch the live, dynamically generated OpenAPI specification directly from the Windmill API using `curl`:

```bash
curl -H "Authorization: Bearer $WML_TOKEN" \
     <WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/openapi.yaml > openapi.yaml
```

## Authentication & Base URL
- **Authentication**: All API requests to Windmill require a Bearer token. Provide it via the `Authorization: Bearer <TOKEN>` header.
- **Base URL**: The default Sift deployment is located at `<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>`.

## Executing Windmill Jobs

You can execute Windmill jobs either synchronously or asynchronously.

### Synchronous Execution
To run a script synchronously and wait for the result, use the `/jobs/run_wait_result/` path prefix.

```bash
TOKEN='your-wml-token'
BODY='{"model":"","input":null,"background":false,"webhook":null}'
URL='<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/responses'
RESULT=$(curl -s -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" -X POST -d "$BODY" $URL)

echo -E $RESULT | jq
```

### Asynchronous Execution & Polling
To run a script asynchronously, use the `/jobs/run/` path prefix. This returns a Job UUID which you can then poll using the `/jobs_u/completed/get_result_maybe/` endpoint.

```bash
TOKEN='your-wml-token'
BODY='{"model":"","input":null,"background":false,"webhook":null}'
URL='<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run/p/f/sift/responses'
UUID=$(curl -s -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" -X POST -d "$BODY" $URL)

POLL_URL="<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs_u/completed/get_result_maybe/$UUID"
while true; do
  curl -s -H "Authorization: Bearer $TOKEN" $POLL_URL -o res.json
  COMPLETED=$(cat res.json | jq .completed)
  if [ "$COMPLETED" = "true" ]; then
    cat res.json | jq .result
    break
  else
    sleep 1
  fi
done
```

---

## Data Schemas

### Webhook Request Schema
```json
{
  "url": "https://your-domain.com/webhook",
  "headers": {
    "Authorization": "Bearer token"
  },
  "metadata": {
    "custom_trace_id": "12345"
  },
  "events": ["started", "completed", "failed"]
}
```

### Agent Request Schema (`f/sift/agents.py`)
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
    "optimizer_params": {},
    "state": {
      "predict": {
        "traces": [],
        "train": [],
        "demos": [],
        "signature": {
          "instructions": "System prompt here",
          "fields": []
        }
      }
    }
  },
  "labels": ["production"],
  "webhook": { /* Webhook Request */ }
}
```

### Agent Response Schema
```json
{
  "success": true,
  "error": null,
  "agent_id": "support_agent",
  "agent_name": "support_agent",
  "agent_card_params": {},
  "litellm_params": { "model": "gpt-4o", "temperature": 0.7 },
  "dspy_params": { /* ... */ },
  "labels": ["production"]
}
```

### Response Request Schema (`f/sift/responses.py`)
```json
{
  "model": "support_agent",
  "input": "How do I reset my password?",
  "background": false,
  "webhook": { /* Webhook Request */ },
  
  // LiteLLM passthrough parameters
  "temperature": 0.5,
  "response_format": {
    "type": "json_schema",
    "json_schema": { /* ... */ }
  }
}
```

### Response Response Schema
```json
{
  "success": true,
  "error": null,
  "id": "resp_123456789",
  "object": "response",
  "created_at": 1718000000,
  "model": "support_agent",
  "status": "completed",
  "output": [
    {
      "content": [
        {
          "type": "output_text",
          "text": "Click the forgot password link."
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 10,
    "output_tokens": 15,
    "total_tokens": 25
  }
}
```

---

## 1. Create / Compile Agent

**Endpoint:** `POST /jobs/run_wait_result/p/f/sift/agents`

Compiles, saves, and configures new DSPy agents to Langfuse. **All fields in the payload are optional.**
- If `agent_name` is omitted, Sift will auto-generate a new UUID for the agent.
- If `agent_name` matches an existing agent, Sift will perform a **deep merge** with the agent's historical state. This means you only need to provide the fields you want to override (e.g., just updating the `optimizer`, `litellm_params`, or `train` dataset), and Sift will preserve the rest of your agent's configuration and trigger re-optimization automatically.
- If creating a new agent with only `train` data and no explicit `signature.fields`, Sift will automatically infer the inputs and outputs from your dataset.
- **Dynamic Optimizer Selection:** If an `optimizer` is not explicitly provided, Sift will automatically select the best strategy based on your `train` dataset size:
  - `BootstrapFewShot` for datasets ≤ 5 examples
  - `BootstrapFewShotWithRandomSearch` for datasets between 6 and 20 examples
  - `MIPROv2` for datasets > 20 examples
- **LLM-as-a-Judge Evaluation:** Sift will automatically route the evaluation of predictions during the DSPy optimization loop to an LLM Judge that scores the model based on expected output, original scores, and feedback defined in your training examples.

### Variation 1: Full Configuration (cURL)
Explicitly configure a detailed agent with signatures, optimizer settings, and LiteLLM parameters.

```bash
curl -X POST "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/agents" \
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
        "predict": {
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

### Variation 2: Zero-Config Auto Inference (Python)
If you omit the `optimizer` configurations and only provide `train` data, Sift automatically defaults to compiling your agent using those static examples (via `BootstrapFewShot`) and infers the signature fields.

```python
import requests

url = "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/agents"
headers = {"Authorization": "Bearer YOUR_WML_TOKEN", "Content-Type": "application/json"}

payload = {
    "agent_name": "train_data_agent",
    "dspy_params": {
        "state": {
            "predict": {
                "train": [
                    {
                        "messages": "What is the capital of France?",
                        "response": "Paris.",
                        "score": 1.0
                    },
                    {
                        "messages": "Extract: Alice is a 30yo doctor.",
                        "response": {
                            "name": "Alice",
                            "age": 30,
                            "profession": "doctor"
                        },
                        "score": 1.0
                    }
                ]
            }
        }
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Variation 3: Multimodal Vision Training Data (Python)
You can directly pass conversational arrays or multimodal image URLs inside the `messages` array of your training data. Sift natively hydrates these arrays for DSPy.

```python
import requests

url = "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/agents"
headers = {"Authorization": "Bearer YOUR_WML_TOKEN", "Content-Type": "application/json"}

payload = {
    "agent_name": "vision_agent",
    "litellm_params": {"model": "gpt-4o"},
    "dspy_params": {
        "state": {
            "predict": {
                "train": [
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "What is the primary color in this image?"},
                                    {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Synthese%2B.svg/200px-Synthese%2B.svg.png"}}
                                ]
                            }
                        ],
                        "response": "Red",
                        "score": 1.0
                    }
                ]
            }
        }
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Variation 4: Update Agent with Deep Merge (cURL)
Provide just your `agent_name` and new `train` data. Sift will preserve your existing configurations, append the new training data, and re-optimize.

```bash
curl -X POST "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/agents" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "existing_support_agent",
    "dspy_params": {
      "state": {
        "predict": {
          "train": [
            {
              "messages": "Can I get a refund?",
              "response": "Refunds are processed within 5-7 business days.",
              "score": 1.0
            }
          ]
        }
      }
    }
  }'
```

### Variation 5: Async Compilation with Webhook (Python)
Heavy optimizers (like `MIPROv2`) can take a long time. Pass a `webhook` configuration to process the agent compilation in the background.

```python
import requests

url = "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/agents"
headers = {
    "Authorization": "Bearer YOUR_WML_TOKEN",
    "Content-Type": "application/json"
}

payload = {
    "agent_name": "async_support_agent",
    "litellm_params": {"model": "gpt-4o"},
    "dspy_params": {
        "state": {
            "predict": {
                "signature": {
                    "instructions": "You are a helpful assistant."
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

### Example Response
Returns the original agent configuration appended with execution success/error state.

```json
{
  "agent_id": "support_agent",
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
  "success": true,
  "error": null
}
```

---

## 2. Predict Response

**Endpoint:** `POST /jobs/run_wait_result/p/f/sift/responses`

Executes an existing agent against user input and returns a standard API response.

### Variation 1: Simple Text Input (cURL)
Standard single-shot prompt.

```bash
curl -X POST "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/responses" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "a2a_agent/support_agent",
    "input": "How do I reset my password?",
    "background": false
  }'
```

### Variation 2: Conversational Messages Array Input (cURL)
Multi-turn chat history utilizing OpenAI-style role definitions.

```bash
curl -X POST "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/responses" \
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

### Variation 3: Multimodal Vision Input (cURL)
Pass an image URL within the message content array for analysis (e.g., receipt extraction or image classification).

```bash
curl -X POST "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/responses" \
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

### Variation 4: Structured JSON Schema Output (cURL)
Sift supports LiteLLM's parameters, allowing you to enforce strict JSON schemas via `response_format`.

```bash
curl -X POST "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/responses" \
  -H "Authorization: Bearer YOUR_WML_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "extraction_agent",
    "input": "Extract details: John Doe is 28 years old.",
    "temperature": 0.2,
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "UserDetails",
        "schema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
          },
          "required": ["name", "age"]
        }
      }
    }
  }'
```

### Variation 5: Asynchronous Background Request (Python)
Execute a slow inference task in the background using `background: true` and a `webhook`.

```python
import requests

url = "<WINDMILL_BASE_URL>/api/w/<WINDMILL_WORKSPACE>/jobs/run_wait_result/p/f/sift/responses"
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

### Example Response
Returns a wrapper containing success states and a LiteLLM/OpenAI-compliant response object.

```json
{
  "success": true,
  "error": null,
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
```

---

## 🪝 Webhooks Reference

Sift utilizes an event-driven webhook decorator (`@webhook_dispatch`) to handle asynchronous lifecycle notifications. When you provide a `webhook` object in your request payload, Sift will `POST` lifecycle events to the target `url` mimicking Firecrawl's flat, strongly-typed event structure.

### Lifecycle Events
- **`started`**: Dispatched immediately before the API begins processing the request. `data` is an empty array `[]`.
- **`completed`**: Dispatched upon successful completion. `data` contains the pure output items directly, stripped of the outer response wrapper.
- **`failed`**: Dispatched if an exception occurs during execution. `error` contains the exception string, and `data` is an empty array `[]`.

### Webhook Payload Schema
When Sift fires a webhook to your server, the `POST` payload will follow this strict schema (`WebhookResponse`):

**Example Response: `response.started`**
Triggered immediately when the inference request begins.
```json
{
  "success": true,
  "type": "response.started",
  "id": "resp_pending...",
  "webhookId": "987fcdeb-51a2-43d7-9012-34567890abcd",
  "data": [],
  "metadata": {
    "custom_trace_id": "12345"
  }
}
```

**Example Response: `response.completed`**
Triggered when the LLM finishes and returns the payload. The `data` array contains the pure output items directly, stripped of the outer response wrapper.
```json
{
  "success": true,
  "type": "response.completed",
  "id": "resp_123456789",
  "webhookId": "11111111-2222-3333-4444-555555555555",
  "data": [
     {
       "content": [
          { "type": "output_text", "text": "Password reset link sent." }
       ]
     }
  ],
  "metadata": {
    "custom_trace_id": "12345"
  }
}
```

**Example Response: `agent.failed`**
Triggered when an agent compilation fails.
```json
{
  "success": false,
  "type": "agent.failed",
  "id": "support_agent",
  "webhookId": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "error": "ValueError: Invalid DSPy parameters provided.",
  "metadata": {
    "custom_trace_id": "12345"
  }
}
```