"""LLM-facing inputs only; effective identity is supplied by trusted server code."""

from typing import Annotated

from pydantic import Field

from packages.contracts.models import Contract, Identifier, Version


class ProjectInput(Contract):
    project_id: Identifier


class CompareQuotesInput(ProjectInput):
    quote_version_ids: Annotated[tuple[Identifier, ...], Field(min_length=1)]


class SaveComparisonReportInput(Contract):
    comparison_id: Identifier


class CreatePurchaseRequestInput(CompareQuotesInput):
    justification: Identifier


class RequestSupplierClarificationInput(Contract):
    quote_id: Identifier
    message: Identifier


class SubmitPurchaseRequestInput(Contract):
    purchase_request_id: Identifier
    expected_version: Version


class ProposeSkillRevisionInput(Contract):
    feedback_id: Identifier


TOOL_INPUTS: dict[str, type[Contract]] = {
    "get_inventory": ProjectInput,
    "get_purchasing_policy": ProjectInput,
    "get_project_quotes": ProjectInput,
    "compare_quotes": CompareQuotesInput,
    "save_comparison_report": SaveComparisonReportInput,
    "create_purchase_request": CreatePurchaseRequestInput,
    "request_supplier_clarification": RequestSupplierClarificationInput,
    "submit_purchase_request": SubmitPurchaseRequestInput,
    "propose_skill_revision": ProposeSkillRevisionInput,
}
