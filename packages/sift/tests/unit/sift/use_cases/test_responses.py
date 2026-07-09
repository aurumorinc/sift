import pytest
from unittest.mock import patch, MagicMock
from sift.use_cases.responses.service import main

@patch("sift.use_cases.responses.service.client")
def test_responses_main_extracts_agent_name(mock_client):
    # Setup mock return value for predict_response
    from sift.modules.responses.schema import ResponsesAPIResponse, ResponseAPIUsage
    mock_response_data = ResponsesAPIResponse(
        id="resp_123",
        object="response",
        created_at=12345,
        model="target_agent",
        status="completed",
        output=[{"content": [{"type": "output_text", "text": "Hi"}]}],
        usage=ResponseAPIUsage(input_tokens=0, output_tokens=0, total_tokens=0)
    )
    mock_client.predict_response.return_value = mock_response_data
    
    # Test stripping "a2a_agent/" prefix
    response = main(
        model="a2a_agent/target_agent",
        input="Hello"
    )
    
    assert response.success is True
    assert response.response is not None
    assert response.response.id == "resp_123"
    
    mock_client.predict_response.assert_called_once()
    # The first positional arg should be the agent_id
    agent_id_called = mock_client.predict_response.call_args[0][0]
    assert agent_id_called == "target_agent"


@patch("sift.use_cases.responses.service.client")
@patch("sift.utils.webhook.service.dispatch_webhook")
def test_responses_main_catches_exception(mock_dispatch_webhook, mock_client):
    mock_client.predict_response.side_effect = ValueError("Mocked response error")
    
    response = main(
        model="test_agent",
        input="Hello",
        webhook={"url": "http://example.com"}
    )
    
    assert response.success is False
    assert response.error == "Mocked response error"
    assert response.response is None
    assert response.webhook is not None
    assert str(response.webhook.url) == "http://example.com/"
