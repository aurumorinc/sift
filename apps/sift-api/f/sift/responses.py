# /// script
# dependencies = [
#   "sift @ git+https://github.com/aurumorinc/sift.git@0.7.0#subdirectory=packages/sift",
# ]
# ///

from typing import Dict, List, Optional, Union

from sift.modules.responses.schema import ResponseResponse
from sift.use_cases.responses.service import main as responses_main


def main(
    model: str,
    input: Union[str, List[Dict]],
    background: bool = False,
    webhook: Optional[Dict] = None,
) -> ResponseResponse:
    """Inference endpoint mapping standard Responses API payload."""
    return responses_main(
        model=model,
        input=input,
        background=background,
        webhook=webhook,
    )
