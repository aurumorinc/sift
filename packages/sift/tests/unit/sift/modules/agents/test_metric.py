import dspy
from sift.modules.agents.metric import dynamic_api_metric


def test_feedback_metric():
    example = dspy.Example(score=0.8, feedback="Great job", answer="42").with_inputs("question")
    pred = dspy.Prediction(answer="42")
    
    result = dynamic_api_metric(example, pred)
    assert isinstance(result, dspy.Prediction)
    assert result.score == 0.8
    assert result.feedback == "Great job"


def test_pre_scored_metric():
    example = dspy.Example(score=0.9, answer="42").with_inputs("question")
    pred = dspy.Prediction(answer="42")
    
    result = dynamic_api_metric(example, pred)
    assert isinstance(result, float)
    assert result == 0.9


def test_fallback_metric():
    example_match = dspy.Example(answer="42", other_field="hello").with_inputs("question")
    pred_match = dspy.Prediction(answer="42", other_field="HELLO ")
    
    result_match = dynamic_api_metric(example_match, pred_match)
    assert isinstance(result_match, float)
    assert result_match == 1.0

    pred_mismatch = dspy.Prediction(answer="43", other_field="hello")
    result_mismatch = dynamic_api_metric(example_match, pred_mismatch)
    assert isinstance(result_mismatch, float)
    assert result_mismatch == 0.0


def test_fallback_metric_no_output_keys():
    example = dspy.Example().with_inputs("question")
    pred = dspy.Prediction()
    
    result = dynamic_api_metric(example, pred)
    assert result == 1.0
