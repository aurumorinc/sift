import pytest
from unittest.mock import MagicMock, patch

from sift.use_cases.agents.service import main


@patch("dspy.teleprompt.BootstrapFewShot")
@patch("sift.modules.agents.repository.langfuse.get_langfuse_client")
def test_full_optimization_flow_existing_agent(mock_get_langfuse_client, mock_bootstrap):
    # This integration test verifies that `agents.py` calls `get_agent_safe` correctly,
    # merges the payload, dynamically infers fields (via `compile_and_save_agent`),
    # compiles using DSPy, and finally saves to Langfuse.

    # 1. Mock Langfuse to return an existing agent
    mock_client = MagicMock()
    mock_get_langfuse_client.return_value = mock_client

    mock_prompt = MagicMock()
    mock_prompt.config = {
        "agent_name": "integration-agent",
        "agent_card_params": {"role": "Integration Bot"},
        "litellm_params": {"model": "openai/gpt-4"},
        "dspy_params": {
            "optimizer": "BootstrapFewShot",
            "state": {
                "predict": {
                    "signature": {"instructions": "Answer questions", "fields": []},
                    "train": [{"question": "Q1", "answer": "A1"}],
                    "traces": [],
                    "demos": []
                }
            }
        },
    }
    mock_client.get_prompt.return_value = mock_prompt

    # 2. Mock DSPy compilation
    mock_optimizer = MagicMock()
    mock_compiled_module = MagicMock()
    mock_compiled_module.dump_state.return_value = {
        "predict": {
            "signature": {
                "instructions": "Optimized instructions.",
                "fields": []
            },
            "train": [{"question": "Q1", "answer": "A1"}, {"question": "Q2", "answer": "A2"}], # Overwritten train
            "traces": [],
            "demos": [{"question": "Q1", "answer": "A1", "augmented": True}],
            "lm": None,
        }
    }
    mock_optimizer.compile.return_value = mock_compiled_module
    mock_bootstrap.return_value = mock_optimizer

    # 3. Act: Provide a new trainset but keep everything else identical.
    response = main(
        agent_name="integration-agent",
        dspy_params={
            "state": {
                "predict": {
                    "train": [{"question": "Q1", "answer": "A1"}, {"question": "Q2", "answer": "A2"}],
                }
            }
        }
    )

    # 4. Assert
    assert response.success is True
    assert response.agent_name == "integration-agent"

    # Langfuse GET was called
    mock_client.get_prompt.assert_called_once_with(name="integration-agent", version=None)

    # DSPy compiler was called
    mock_bootstrap.assert_called_once()
    mock_optimizer.compile.assert_called_once()
    
    # Langfuse CREATE was called
    mock_client.create_prompt.assert_called_once()
    
    # Verify the payload saved
    saved_kwargs = mock_client.create_prompt.call_args[1]
    assert saved_kwargs["name"] == "integration-agent"
    
    # Since we started with empty fields, our field inference logic in service.py
    # should have populated the original fields to be retained in the save.
    saved_config = saved_kwargs["config"]
    assert saved_config["agent_card_params"] == {"role": "Integration Bot"} # retained
    
    predict_state = saved_config["dspy_params"]["state"]["predict"]
    assert predict_state["signature"]["instructions"] == "Optimized instructions."
    
    # Inferred fields should have 2 fields (question, answer)
    saved_fields = predict_state["signature"]["fields"]
    assert len(saved_fields) == 2
    names = [f["name"] for f in saved_fields]
    assert "question" in names
    assert "answer" in names

    # Verify overwritten train data is present
    assert len(predict_state["train"]) == 2
    assert predict_state["train"][1]["question"] == "Q2"
