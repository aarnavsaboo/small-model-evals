from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class Task:
    id: str
    type: str
    prompt: str
    answer: str | None = None
    choices: tuple[str, ...] = ()
    required: tuple[str, ...] = ()
    max_output_tokens: int = 128
    metadata: dict[str, Any] | None = None


def load(path: str) -> list[Task]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append(Task(
            id=str(row["id"]),
            type=str(row["type"]),
            prompt=str(row["prompt"]),
            answer=None if row.get("answer") is None else str(row["answer"]),
            choices=tuple(str(x) for x in row.get("choices", [])),
            required=tuple(str(x) for x in row.get("required", [])),
            max_output_tokens=int(row.get("max_output_tokens", 128)),
            metadata=dict(row.get("metadata", {})),
        ))
    return rows
