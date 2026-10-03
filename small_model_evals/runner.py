from __future__ import annotations

from pathlib import Path
import json

from .ollama import OllamaRunner
from .planner import Job
from .scoring import score
from .tasks import Task


def execute(jobs: list[Job], tasks: list[Task], backend: OllamaRunner) -> list[dict]:
    task_by_id = {x.id: x for x in tasks}
    rows = []
    for job in jobs:
        task = task_by_id[job.task_id]
        try:
            result = backend.generate(
                job.model,
                task.prompt,
                task.max_output_tokens,
                job.temperature,
                job.seed,
            )
            rows.append({
                "job_id": job.id,
                "model": job.model,
                "task_id": task.id,
                "task_type": task.type,
                "repeat": job.repeat,
                "temperature": job.temperature,
                "seed": job.seed,
                "prompt_chars": len(task.prompt),
                "score": score(task, result["text"]),
                "ok": True,
                **result,
            })
        except Exception as exc:
            rows.append({
                "job_id": job.id,
                "model": job.model,
                "task_id": task.id,
                "task_type": task.type,
                "repeat": job.repeat,
                "ok": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
    return rows


def write_jsonl(path: str, rows: list[dict]):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows),
        encoding="utf-8",
    )
