from typing import Any, Optional
import dspy

def dynamic_api_metric(example: dspy.Example, pred: dspy.Prediction, trace: Optional[Any] = None) -> float | dspy.Prediction:
    if getattr(example, "feedback", None) is not None:
        return dspy.Prediction(
            score=getattr(example, "score", None),
            feedback=example.feedback
        )
    
    if getattr(example, "score", None) is not None:
        return float(example.score)

    output_keys = [k for k in example.labels().keys() if k not in ("score", "feedback")]
    if not output_keys:
        return 1.0

    for output_key in output_keys:
        ex_val = str(getattr(example, output_key, "")).strip().lower()
        pr_val = str(getattr(pred, output_key, "")).strip().lower()
        if ex_val != pr_val:
            return 0.0
            
    return 1.0
