"""Version-zero shared data contracts; authorization belongs to the server."""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

Identifier = Annotated[str, Field(min_length=1, max_length=256)]
Version = Annotated[int, Field(strict=True, ge=1)]
Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ActorType(StrEnum):
    USER = "user"
    SERVICE = "service"


class RunStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING_INPUT = "WAITING_INPUT"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    WAITING_AUTH = "WAITING_AUTH"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WaitType(StrEnum):
    QUESTION = "QUESTION"
    TOOL_APPROVAL = "TOOL_APPROVAL"
    PURCHASE_APPROVAL = "PURCHASE_APPROVAL"
    DELEGATED_TOOL = "DELEGATED_TOOL"
    SUPPLIER_RESPONSE = "SUPPLIER_RESPONSE"


class PurchaseStatus(StrEnum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    CANCELLED = "CANCELLED"


class Decision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VERSION_CONFLICT = "VERSION_CONFLICT"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    APPROVAL_EXPIRED = "APPROVAL_EXPIRED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    TRANSIENT_FAILURE = "TRANSIENT_FAILURE"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"


class ActorContext(Contract):
    tenant_id: Identifier
    subject_id: Identifier
    actor_type: ActorType
    client_id: Identifier
    scopes: tuple[Identifier, ...]
    app_roles: tuple[Identifier, ...]
    memberships: tuple[Identifier, ...]


class Money(Contract):
    amount: Annotated[Decimal, Field(ge=0, allow_inf_nan=False)]
    currency: Literal["EUR"] = "EUR"

    @field_validator("amount", mode="before")
    @classmethod
    def reject_float(cls, value: object) -> object:
        if isinstance(value, (float, bool)):
            raise ValueError("amount must not be a binary float or boolean")
        return value


class EvidenceRef(Contract):
    artifact_id: Identifier
    content_hash: Hash
    page: Annotated[int, Field(strict=True, ge=1)] | None = None
    cell: Identifier | None = None
    extractor_version: Identifier
    extracted_at: datetime

    @model_validator(mode="after")
    def has_location(self) -> "EvidenceRef":
        if (self.page is None) == (self.cell is None):
            raise ValueError("exactly one of page or cell is required")
        return self


class QuoteLine(Contract):
    id: Identifier
    description: Identifier
    quantity: Annotated[Decimal, Field(gt=0, allow_inf_nan=False)]
    unit_price: Money
    tax: Money | None = None
    discount: Money | None = None
    evidence: tuple[EvidenceRef, ...]


class Quote(Contract):
    id: Identifier
    supplier_id: Identifier
    project_id: Identifier
    issued_on: date
    valid_until: date
    lines: Annotated[tuple[QuoteLine, ...], Field(min_length=1)]
    transport: Money | None = None
    conditions: str
    source: EvidenceRef
    version: Version

    @model_validator(mode="after")
    def valid_dates(self) -> "Quote":
        if self.valid_until < self.issued_on:
            raise ValueError("valid_until precedes issued_on")
        return self


class PurchaseRequest(Contract):
    project_id: Identifier
    requester_id: Identifier
    quote_version_ids: Annotated[tuple[Identifier, ...], Field(min_length=1)]
    total: Money
    status: PurchaseStatus
    version: Version
    justification: Identifier


class Run(Contract):
    id: Identifier
    thread_id: Identifier
    tenant_id: Identifier
    owner_id: Identifier
    project_id: Identifier
    status: RunStatus
    version: Version
    commit: Identifier
    image_digest: Identifier
    model_config_hash: Hash
    skill_set_version: Identifier
    policy_version: Identifier
    dataset_version: Identifier
    schema_version: Identifier


class PendingAction(Contract):
    id: Identifier
    run_id: Identifier
    interrupt_id: Identifier
    type: WaitType
    response_schema: dict[str, JsonValue]
    allowed_recipient: Identifier | None = None
    allowed_role: Identifier | None = None
    arguments: dict[str, JsonValue]
    payload_hash: Hash
    artifact_hash: Hash | None = None
    expires_at: datetime

    @model_validator(mode="after")
    def has_recipient(self) -> "PendingAction":
        if self.allowed_recipient is None and self.allowed_role is None:
            raise ValueError("allowed_recipient or allowed_role is required")
        return self


class ActionApproval(Contract):
    pending_action_id: Identifier
    decision: Decision
    actor: ActorContext
    payload_hash: Hash
    artifact_hash: Hash | None = None
    destination: Identifier
    expires_at: datetime
    consumption_id: Identifier

    @model_validator(mode="after")
    def human_actor(self) -> "ActionApproval":
        if self.actor.actor_type != ActorType.USER:
            raise ValueError("approval requires a user actor")
        return self


class PurchaseDecision(Contract):
    purchase_request_id: Identifier
    expected_version: Version
    decision: Decision
    actor: ActorContext
    comment: str

    @model_validator(mode="after")
    def human_actor(self) -> "PurchaseDecision":
        if self.actor.actor_type != ActorType.USER:
            raise ValueError("purchase decision requires a user actor")
        return self


class Artifact(Contract):
    id: Identifier
    project_id: Identifier
    internal_location: Identifier
    content_hash: Hash
    mime_type: Identifier
    size_bytes: Annotated[int, Field(strict=True, ge=0)]
    visibility: Identifier
    source_run: Identifier


class ExecutionCommand(Contract):
    schema_version: Identifier
    command_id: Identifier
    environment_id: Identifier
    run_id: Identifier
    thread_id: Identifier
    expected_version: Version
    operation: Literal["start", "resume"]
    response_ref: Identifier | None = None
    correlation_id: Identifier

    @model_validator(mode="after")
    def valid_response(self) -> "ExecutionCommand":
        if (self.operation == "resume") != (self.response_ref is not None):
            raise ValueError("response_ref is required only for resume")
        return self


class ContractError(Contract):
    code: ErrorCode
    message: Identifier


class ToolResult(Contract):
    result: JsonValue = None
    evidence: tuple[EvidenceRef, ...] = ()
    error: ContractError | None = None

    @model_validator(mode="after")
    def one_outcome(self) -> "ToolResult":
        if self.error is not None and self.result is not None:
            raise ValueError("result and error are mutually exclusive")
        return self
