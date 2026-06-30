from sift.modules.agents.schema import DSPyTrainingExample


def test_dspy_training_example_valid_schema():
    example = DSPyTrainingExample(score=0.9, feedback="Good", question="Hi")
    assert example.score == 0.9
    assert example.feedback == "Good"
    assert example.model_extra is not None
    assert example.model_extra["question"] == "Hi"
    assert getattr(example, "question") == "Hi"


def test_dspy_training_example_missing_extras():
    example = DSPyTrainingExample(score=0.5)
    assert example.score == 0.5
    assert example.feedback is None
    assert example.trace_id is None
    assert example.model_extra is None or len(example.model_extra) == 0
