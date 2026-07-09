import pytest
from sift.modules.responses.schema import ResponseRequest


def test_response_request_allows_litellm_fields():
    req = ResponseRequest(
        model="test_model",
        input="test_input",
        temperature=0.7,
        max_output_tokens=100,
        text={"format": {"type": "json_object"}},
        stream=True
    )
    assert req.model == "test_model"
    assert req.input == "test_input"
    assert req.temperature == 0.7
    assert req.max_output_tokens == 100
    assert req.text == {"format": {"type": "json_object"}}
    assert req.stream is True

def test_response_request_extra_fields():
    req = ResponseRequest(
        model="test_model",
        input="test_input",
        extra_param="extra_value"
    )
    assert req.model_extra is not None and req.model_extra.get("extra_param") == "extra_value"
