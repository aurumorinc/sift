import pytest
from unittest.mock import MagicMock

from sift.modules.agents.repository.langfuse import get_agent, get_agent_safe, save_agent
from sift.modules.agents.schema import (
    Agent,
    DSPyParams,
    DSPyPredictorState,
    DSPySignatureState,
)


@pytest.fixture
def mock_langfuse_client(mocker):
    client = MagicMock()
    mocker.patch(
        "sift.modules.agents.repository.langfuse.get_langfuse_client",
        return_value=client,
    )
    return client


def test_save_agent_instruction_extraction(mock_langfuse_client):
    # Setup test agent with multiple predictor states
    agent = Agent(
        agent_name="test-agent",
        agent_card_params={},
        litellm_params={},
        dspy_params=DSPyParams(
            state={
                "predict1": DSPyPredictorState(
                    signature=DSPySignatureState(
                        instructions="First instruction", fields=[]
                    )
                ),
                "predict2": DSPyPredictorState(
                    signature=DSPySignatureState(
                        instructions="Second instruction", fields=[]
                    )
                ),
            }
        ),
        labels=["test-label"],
    )

    save_agent(agent)

    # Verify create_prompt was called correctly
    mock_langfuse_client.create_prompt.assert_called_once()

    _, kwargs = mock_langfuse_client.create_prompt.call_args
    assert kwargs["name"] == "test-agent"
    assert kwargs["prompt"] == "First instruction\n\nSecond instruction"
    assert kwargs["type"] == "text"
    assert kwargs["labels"] == ["test-label"]

    # Ensure config gets the full dumped agent dictionary
    assert isinstance(kwargs["config"], dict)
    assert kwargs["config"]["agent_name"] == "test-agent"
    assert "dspy_params" in kwargs["config"]
    assert "predict1" in kwargs["config"]["dspy_params"]["state"]


def test_save_agent_empty_state(mock_langfuse_client):
    # Setup test agent with no states
    agent = Agent(
        agent_name="test-agent",
        agent_card_params={},
        litellm_params={},
        dspy_params=DSPyParams(state={}),
    )

    save_agent(agent)

    _, kwargs = mock_langfuse_client.create_prompt.call_args
    assert kwargs["prompt"] == ""
    assert isinstance(kwargs["config"], dict)


def test_get_agent_reads_from_config(mock_langfuse_client):
    # Setup mock prompt response
    mock_prompt = MagicMock()
    mock_prompt.prompt = "Some ignored text prompt"
    mock_prompt.config = {
        "agent_name": "retrieved-agent",
        "agent_card_params": {},
        "litellm_params": {},
        "dspy_params": {"state": {}},
    }
    mock_langfuse_client.get_prompt.return_value = mock_prompt

    agent = get_agent("retrieved-agent", version=1)

    # Verify get_prompt was called correctly
    mock_langfuse_client.get_prompt.assert_called_once_with(
        name="retrieved-agent", version=1
    )

    # Verify agent was instantiated from config
    assert isinstance(agent, Agent)
    assert agent.agent_name == "retrieved-agent"


def test_get_agent_defaults_agent_name(mock_langfuse_client):
    # Setup mock prompt response missing agent_name
    mock_prompt = MagicMock()
    mock_prompt.prompt = "ignored"
    mock_prompt.config = {
        "agent_card_params": {},
        "litellm_params": {},
        "dspy_params": {"state": {}},
    }
    mock_langfuse_client.get_prompt.return_value = mock_prompt

    agent = get_agent("missing-name-agent")

    assert agent.agent_name == "missing-name-agent"


def test_legacy_config_parsing(mock_langfuse_client):
    # Setup mock prompt response with MISSING required fields (simulating legacy config)
    mock_prompt = MagicMock()
    mock_prompt.prompt = "ignored"
    mock_prompt.config = {
        "agent_name": "legacy-agent"
        # missing agent_card_params, litellm_params, and dspy_params
    }
    mock_langfuse_client.get_prompt.return_value = mock_prompt

    agent = get_agent("legacy-agent")

    assert agent.agent_name == "legacy-agent"
    # Ensure it didn't throw a validation error and defaults were set
    assert isinstance(agent.agent_card_params, dict)
    assert isinstance(agent.litellm_params, dict)
    assert isinstance(agent.dspy_params, DSPyParams)


def test_get_agent_safe_returns_agent(mock_langfuse_client):
    mock_prompt = MagicMock()
    mock_prompt.config = {
        "agent_name": "existing-agent",
        "agent_card_params": {},
        "litellm_params": {},
        "dspy_params": {"state": {}},
    }
    mock_langfuse_client.get_prompt.return_value = mock_prompt

    agent = get_agent_safe("existing-agent")
    assert isinstance(agent, Agent)
    assert agent.agent_name == "existing-agent"


def test_get_agent_safe_returns_none_on_exception(mock_langfuse_client):
    mock_langfuse_client.get_prompt.side_effect = Exception("Not found")

    agent = get_agent_safe("non-existent-agent")
    assert agent is None
