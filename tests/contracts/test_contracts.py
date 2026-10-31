import json
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from packages.contracts.canonical import canonical_json, payload_hash
from packages.contracts.models import (
    ActionApproval,
    ExecutionCommand,
    Money,
    PurchaseDecision,
    Run,
)
from packages.contracts.tool_inputs import TOOL_INPUTS

FIXTURE = Path(__file__).parent / "fixtures" / "contracts-v0.json"
ROOT = Path(__file__).resolve().parents[2] / "packages" / "contracts" / "schemas"


def test_round_trip_fixture() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for name, cls in (("money", Money), ("run", Run), ("command", ExecutionCommand)):
        model = cls.model_validate(data[name])
        assert cls.model_validate_json(model.model_dump_json()) == model
    assert Money.model_validate(data["money"]).amount == Decimal("123.4500")
    assert json.loads(Money.model_validate(data["money"]).model_dump_json())["amount"] == "123.4500"
    assert Run.model_validate(data["run"]).version == 7


@pytest.mark.parametrize("amount", [-1, "NaN", float("inf"), 0.1, True])
def test_invalid_money(amount: object) -> None:
    with pytest.raises(ValidationError):
        Money.model_validate({"amount": amount})


def test_reject_invalid_fields_and_versions() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for change in ({"version": 0}, {"status": "invented"}, {"owner_id": ""}, {"secret": "x"}):
        with pytest.raises(ValidationError):
            Run.model_validate(data["run"] | change)
    with pytest.raises(ValidationError):
        ExecutionCommand.model_validate(data["command"] | {"operation": "resume"})


def test_canonical_hash() -> None:
    assert payload_hash({"b": [1, "á"], "a": True}) == payload_hash({"a": True, "b": [1, "á"]})
    assert payload_hash({"a": 1}) != payload_hash({"a": 2})
    assert canonical_json({"x": "1.00"}) == b'{"x":"1.00"}'
    for bad in ({"x": 1.0}, {1: "x"}, {"x": Decimal("1")}):
        with pytest.raises(ValueError):
            canonical_json(bad)


def test_approval_contracts_are_distinct() -> None:
    assert "pending_action_id" in ActionApproval.model_fields
    assert "purchase_request_id" in PurchaseDecision.model_fields
    assert "purchase_request_id" not in ActionApproval.model_fields
    assert "pending_action_id" not in PurchaseDecision.model_fields
    actor = {
        "tenant_id": "tenant",
        "subject_id": "service",
        "actor_type": "service",
        "client_id": "client",
        "scopes": [],
        "app_roles": [],
        "memberships": [],
    }
    with pytest.raises(ValidationError):
        PurchaseDecision.model_validate(
            {
                "purchase_request_id": "p",
                "expected_version": 1,
                "decision": "approve",
                "actor": actor,
                "comment": "",
            }
        )


def test_exported_tool_schemas_forbid_identity() -> None:
    schemas = json.loads((ROOT / "tool-inputs-v0.json").read_text(encoding="utf-8"))
    assert set(schemas) == set(TOOL_INPUTS)
    forbidden = {
        "actor",
        "actor_context",
        "tenant_id",
        "subject_id",
        "owner_id",
        "requester_id",
        "client_id",
        "credentials",
        "token",
    }
    assert "approve_purchase_request" not in schemas
    for name, cls in TOOL_INPUTS.items():
        assert schemas[name] == cls.model_json_schema()
        assert not forbidden.intersection(schemas[name]["properties"])
        assert schemas[name]["additionalProperties"] is False
        with pytest.raises(ValidationError):
            cls.model_validate({"tenant_id": "attacker"})
