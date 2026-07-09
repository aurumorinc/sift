import os
import uuid
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()

WINDMILL_ACCESS_TOKEN = os.getenv("WINDMILL_ACCESS_TOKEN")
WINDMILL_BASE_URL = os.getenv("WINDMILL_BASE_URL")

pytestmark = pytest.mark.manual


@pytest.fixture(autouse=True)
def check_token():
    if not WINDMILL_ACCESS_TOKEN:
        pytest.skip("WINDMILL_ACCESS_TOKEN is not set")


def test_windmill_full_configuration():
    agent_name = f"test_windmill_agent_{uuid.uuid4().hex[:8]}"
    url = f"{WINDMILL_BASE_URL}/jobs/run_wait_result/p/f/sift/agents"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_name": agent_name,
        "agent_card_params": {},
        "litellm_params": {"model": "gemini/gemini-3.1-flash-lite"},
        "dspy_params": {
            "optimizer": "BootstrapFewShot",
            "state": {
                "predict": {
                    "signature": {
                        "instructions": "You are a helpful assistant.",
                        "fields": [
                            {"name": "messages", "description": "Input messages"},
                            {"name": "response", "description": "Output response"}
                        ]
                    },
                    "train": [
                        {"messages": "Hello", "response": "Hi there!"},
                        {"messages": "How are you?", "response": "I'm doing well, thanks!"}
                    ]
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
    # Wait for the job or if it's synchronous wait result. 
    # Windmill /run endpoint is usually async (returns a job ID). 
    # We should use `/run/wait` to get synchronous results.
    pass


def test_windmill_zero_config():
    agent_name = f"test_windmill_agent_{uuid.uuid4().hex[:8]}"
    url = f"{WINDMILL_BASE_URL}/jobs/run_wait_result/p/f/sift/agents"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_name": agent_name,
        "dspy_params": {
            "state": {
                "predict": {
                    "train": [
                        {"messages": "What is 2+2?", "response": "4"},
                        {"messages": "What is 3+3?", "response": "6"}
                    ]
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
    
    
def test_windmill_multimodal():
    agent_name = f"test_windmill_agent_{uuid.uuid4().hex[:8]}"
    url = f"{WINDMILL_BASE_URL}/jobs/run_wait_result/p/f/sift/agents"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_name": agent_name,
        "dspy_params": {
            "state": {
                "predict": {
                    "train": [
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": "Describe this image."},
                                        {"type": "image_url", "image_url": "https://raw.githubusercontent.com/aurumorinc/sift/main/README.md"}
                                    ]
                                }
                            ],
                            "response": "This is a document."
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"


def test_windmill_deep_merge():
    agent_name = f"test_windmill_agent_{uuid.uuid4().hex[:8]}"
    url = f"{WINDMILL_BASE_URL}/jobs/run_wait_result/p/f/sift/agents"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Create
    payload1 = {
        "agent_name": agent_name,
        "litellm_params": {"model": "gemini/gemini-3.1-flash-lite"}
    }
    requests.post(url, headers=headers, json=payload1)
    
    # Update
    payload2 = {
        "agent_name": agent_name,
        "dspy_params": {
            "state": {
                "predict": {
                    "train": [
                        {"messages": "Update test", "response": "Passed"}
                    ]
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload2)
    assert response.status_code == 200, f"Failed: {response.text}"


def test_windmill_async_webhook():
    agent_name = f"test_windmill_agent_{uuid.uuid4().hex[:8]}"
    url = f"{WINDMILL_BASE_URL}/jobs/run_wait_result/p/f/sift/agents"
    headers = {
        "Authorization": f"Bearer {WINDMILL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_name": agent_name,
        "webhook": {
            "url": "https://httpbin.org/post",
            "token": "dummy_token"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
