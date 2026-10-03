from pathlib import Path
import json

from .planner import Job


def read_jobs(path: str) -> list[Job]:
    return [Job(**json.loads(line)) for line in Path(path).read_text().splitlines() if line.strip()]


def read_rows(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
