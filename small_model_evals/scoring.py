import re

from .tasks import Task


def normalize(text: str) -> str:
    return " ".join(re.findall(r"\w+", text.casefold(), flags=re.UNICODE))


def exact(output: str, answer: str) -> float:
    return float(normalize(output) == normalize(answer))


def contains(output: str, answer: str) -> float:
    return float(normalize(answer) in normalize(output))


def choice(output: str, answer: str, choices: tuple[str, ...]) -> float:
    cleaned = output.strip().upper()
    expected = answer.strip().upper()
    if cleaned == expected:
        return 1.0
    first = re.match(r"^([A-Z])(?:\b|[.): -])", cleaned)
    if first and first.group(1) == expected:
        return 1.0
    if expected in choices and normalize(expected) == normalize(output):
        return 1.0
    return 0.0


def keywords(output: str, required: tuple[str, ...]) -> float:
    if not required:
        return 0.0
    haystack = normalize(output)
    return sum(normalize(term) in haystack for term in required) / len(required)


def score(task: Task, output: str) -> float:
    if task.type == "exact":
        return exact(output, task.answer or "")
    if task.type == "contains":
        return contains(output, task.answer or "")
    if task.type == "choice":
        return choice(output, task.answer or "", task.choices)
    if task.type == "keywords":
        return keywords(output, task.required)
    raise ValueError(f"unknown task type: {task.type}")
