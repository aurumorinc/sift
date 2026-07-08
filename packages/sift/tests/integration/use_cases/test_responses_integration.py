import pytest
import dspy
from unittest.mock import patch, MagicMock

from sift.use_cases.responses.service import main as responses_main
from sift.modules.agents.schema import Agent, DSPyParams, DSPyPredictorState, DSPySignatureState
from sift.modules.responses.schema import ResponseResponse

@patch("sift.modules.responses.service.get_agent")
def test_responses_main_structured_format_integration(mock_get_agent):
    mock_agent = Agent(
        agent_name="structured_agent",
        agent_card_params={},
        litellm_params={"model": "openai/gpt-3.5-turbo"},
        dspy_params=DSPyParams(
            state={
                "prog": DSPyPredictorState(
                    signature=DSPySignatureState(
                        instructions="Extract details",
                        fields=[{"name": "messages", "json_schema_extra": {"__dspy_field_type": "input"}}]
                    ),
                    lm=None
                )
            }
        )
    )
    mock_get_agent.return_value = mock_agent

    with patch("dspy.LM") as mock_lm_class:
        mock_lm_instance = MagicMock()
        mock_lm_class.return_value = mock_lm_instance

        with patch("sift.modules.agents.service.AgentModule.forward") as mock_forward:
            mock_forward.return_value = dspy.Prediction(response='{"extracted": True}')
            
            resp: ResponseResponse = responses_main(
                model="structured_agent",
                input="Do extraction",
                text={"format": {"type": "json_object"}},
                temperature=0.3
            )
            
            assert resp.success is True
            assert resp.response.output[0]["content"][0]["text"] == '{"extracted": True}'
            
            # verify the dspy.LM was instantiated with response_format and temperature
            mock_lm_class.assert_called_once()
            lm_kwargs = mock_lm_class.call_args.kwargs
            assert lm_kwargs.get("temperature") == 0.3
            assert lm_kwargs.get("response_format") == {"type": "json_object"}
            assert "text" not in lm_kwargs
