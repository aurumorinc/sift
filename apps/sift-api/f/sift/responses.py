# /// script
# dependencies = [
#   "sift @ git+https://github.com/aurumorinc/sift.git@0.10.0#subdirectory=packages/sift",
#   "wmill",
# ]
# ///

import os
import wmill
from typing import Dict, List, Optional, Union

from sift.modules.responses.schema import ResponseResponse
from sift.use_cases.responses.service import main as responses_main


os.environ["GEMINI_API_KEY"] = wmill.get_variable("f/sift/gemini_api_key")
os.environ["LANGFUSE_SECRET_KEY"] = wmill.get_variable("f/sift/langfuse_secret_key")
os.environ["LANGFUSE_PUBLIC_KEY"] = wmill.get_variable("f/sift/langfuse_public_key")
os.environ["LANGFUSE_BASE_URL"] = wmill.get_variable("f/sift/langfuse_base_url")
os.environ["LANGFUSE_HOST"] = wmill.get_variable("f/sift/langfuse_host")


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
