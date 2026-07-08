import dspy
import pytest
from unittest.mock import patch, MagicMock
from sift.modules.responses.service import predict_response


@patch("sift.modules.responses.service.get_agent")
@patch("dspy.LM")
def test_predict_response_multimodal_passthrough(mock_lm, mock_get_agent):
    mock_agent = MagicMock()
    mock_agent.litellm_params = {"model": "openai/gpt-4o"}
    
    mock_agent.dspy_params.state = {
        "prog": MagicMock(
            model_dump=lambda: {
                "signature": {
                    "instructions": "test instructions",
                    "fields": [
                        {"name": "messages", "json_schema_extra": {"__dspy_field_type": "input"}}
                    ]
                },
                "lm": None
            }
        )
    }
    mock_get_agent.return_value = mock_agent

    mock_lm_instance = MagicMock()
    mock_lm.return_value = mock_lm_instance

    multimodal_input = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image."},
                {"type": "image_url", "image_url": {"url": "https://example.com/test.jpg"}}
            ]
        }
    ]

    with patch("sift.modules.agents.service.AgentModule.forward") as mock_forward:
        mock_forward.return_value = dspy.Prediction(response="It is an image.")
        
        response = predict_response("agent_id_test", multimodal_input)
        
        assert response.status == "completed"
        assert response.output[0]["content"][0]["text"] == "It is an image."
        
        mock_forward.assert_called_once()
        called_kwargs = mock_forward.call_args.kwargs
        assert "messages" in called_kwargs
        
        passed_messages = called_kwargs["messages"]
        assert isinstance(passed_messages, list)
        assert len(passed_messages) == 1
        
        content = passed_messages[0]["content"]
        assert isinstance(content, list)
        assert len(content) == 2
        assert content[0]["type"] == "text"
        
        # This checks if _hydrate_multimodal_messages was successful
        assert isinstance(content[1], dspy.Image)
        assert content[1].url == "https://example.com/test.jpg"
