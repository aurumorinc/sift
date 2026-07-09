import os
import uuid
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()

WINDMILL_ACCESS_TOKEN = os.getenv("WINDMILL_ACCESS_TOKEN")
WINDMILL_BASE_URL = os.getenv("WINDMILL_BASE_URL", "https://windmill.aurumor.com")
WORKSPACE = "sift"

pytestmark = pytest.mark.manual


@pytest.fixture(autouse=True)
def check_token():
    if not WINDMILL_ACCESS_TOKEN:
        pytest.skip("WINDMILL_ACCESS_TOKEN is not set")


@pytest.fixture(scope="module")
def setup_test_agent():
    agent_name = f"test_windmill_resp_agent_{uuid.uuid4().hex[:8]}"
    url = f"{WINDMILL_BASE_URL}/api/w/{WORKSPACE}/jobs/run/wait/f/sift/agents"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_name": agent_name,
        "litellm_params": {"model": "gemini/gemini-3.1-flash-lite"},
        "dspy_params": {
            "state": {
                "predict": {
                    "train": [
                        {"messages": "What is 2+2?", "response": "4"}
                    ]
                }
            }
        }
    }
    requests.post(url, headers=headers, json=payload)
    return agent_name


def test_windmill_simple_text(setup_test_agent):
    url = f"{WINDMILL_BASE_URL}/api/w/{WORKSPACE}/jobs/run/wait/f/sift/responses"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": setup_test_agent,
        "input": "What is 2+2?"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"


def test_windmill_conversational(setup_test_agent):
    url = f"{WINDMILL_BASE_URL}/api/w/{WORKSPACE}/jobs/run/wait/f/sift/responses"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": setup_test_agent,
        "input": [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi! How can I help you?"},
            {"role": "user", "content": "What is 3+3?"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"


def test_windmill_multimodal(setup_test_agent):
    url = f"{WINDMILL_BASE_URL}/api/w/{WORKSPACE}/jobs/run/wait/f/sift/responses"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": setup_test_agent,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image."},
                    {"type": "image_url", "image_url": "https://raw.githubusercontent.com/aurumorinc/sift/main/README.md"}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"


def test_windmill_structured_json(setup_test_agent):
    url = f"{WINDMILL_BASE_URL}/api/w/{WORKSPACE}/jobs/run/wait/f/sift/responses"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": setup_test_agent,
        "input": "Give me a random user profile.",
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "UserProfile",
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
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"


def test_windmill_async_background(setup_test_agent):
    # This one we use standard /run because it's in the background anyway, or /run/wait?
    # If we want the wait for the background trigger, we can use /run/wait
    url = f"{WINDMILL_BASE_URL}/api/w/{WORKSPACE}/jobs/run/wait/f/sift/responses"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": setup_test_agent,
        "input": "Hello",
        "background": True,
        "webhook": {
            "url": "https://httpbin.org/post",
            "token": "dummy"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
