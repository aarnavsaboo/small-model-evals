from dataclasses import asdict, dataclass
from hashlib import sha1
from itertools import product
import json


@dataclass(frozen=True)
class Job:
    id: str
    model: str
    task_id: str
    repeat: int
    temperature: float
    seed: int | None

    def to_dict(self):
        return asdict(self)


def expand(config: dict, task_ids: list[str]) -> list[Job]:
    rows = []
    for model, task_id, repeat, temperature in product(
        config["models"],
        task_ids,
        range(int(config.get("repeats", 1))),
        config.get("temperature", [0.0]),
    ):
        seed = None if config.get("seed") is None else int(config["seed"]) + repeat
        payload = {
            "model": str(model),
            "task_id": str(task_id),
            "repeat": repeat,
            "temperature": float(temperature),
            "seed": seed,
        }
        ident = sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
        rows.append(Job(id=ident, **payload))
    return rows
