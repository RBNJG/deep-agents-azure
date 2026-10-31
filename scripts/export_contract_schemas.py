"""Export versioned contract and LLM input JSON schemas."""

import json
from pathlib import Path

from packages.contracts import models
from packages.contracts.tool_inputs import TOOL_INPUTS

ROOT = Path(__file__).resolve().parents[1] / "packages" / "contracts" / "schemas"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    contracts = {
        name: value.model_json_schema()
        for name, value in vars(models).items()
        if isinstance(value, type)
        and issubclass(value, models.Contract)
        and value is not models.Contract
    }
    for name, data in {
        "contracts-v0.json": contracts,
        "tool-inputs-v0.json": {name: cls.model_json_schema() for name, cls in TOOL_INPUTS.items()},
    }.items():
        (ROOT / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
