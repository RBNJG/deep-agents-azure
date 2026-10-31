"""Canonical JSON for idempotency, version 1."""

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> bytes:
    """Encode JSON values; reject floats and non-string keys to avoid ambiguity."""

    def validate(item: Any) -> None:
        if item is None or type(item) in (str, bool, int):
            return
        if isinstance(item, list):
            for child in item:
                validate(child)
            return
        if isinstance(item, dict) and all(type(key) is str for key in item):
            for child in item.values():
                validate(child)
            return
        raise ValueError("canonical arguments must contain only JSON values without floats")

    validate(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )


def payload_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()
