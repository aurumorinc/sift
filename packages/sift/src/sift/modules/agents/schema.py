import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from sift.utils.webhook.schema import Webhook


class DSPySignatureState(BaseModel):
    instructions: str
    fields: Any
    model_config = ConfigDict(extra="allow")


class DSPyTrainingExample(BaseModel):
    trace_id: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    model_config = ConfigDict(extra="allow")


class DSPyPredictorState(BaseModel):
    traces: List[Any] = Field(default_factory=list)
    train: List[DSPyTrainingExample] = Field(default_factory=list)
    demos: List[Dict[str, Any]] = Field(default_factory=list)
    signature: DSPySignatureState
    lm: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="allow")


class DSPyParams(BaseModel):
    optimizer: Optional[str] = None
    optimizer_params: Optional[Dict[str, Any]] = None
    state: Dict[str, DSPyPredictorState]


class Agent(BaseModel):
    agent_name: str = Field(default_factory=lambda: uuid.uuid4().hex)
    agent_card_params: Dict[str, Any]
    litellm_params: Dict[str, Any]
    object_permission: Optional[Dict[str, Any]] = None
    dspy_params: DSPyParams
    labels: Optional[List[str]] = None


class AgentRequest(Agent):
    webhook: Optional[Webhook] = None


class AgentResponse(Agent):
    success: bool
    error: Optional[str] = None
    webhook: Optional[Webhook] = None


class AgentpredictRequest(BaseModel):
    # Payload sent to execute the agent (e.g. standard message history or inputs)
    messages: List[Dict[str, Any]]
    model_config = ConfigDict(extra="allow")
