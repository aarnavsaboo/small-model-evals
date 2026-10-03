from collections import defaultdict
from statistics import median


def summarize(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        if row.get("ok"):
            groups[(row["model"], row["task_type"])].append(row)

    output = []
    for (model, task_type), group in sorted(groups.items()):
        scores = [float(x["score"]) for x in group]
        latency = [float(x["elapsed_seconds"]) for x in group]
        decode = [float(x["decode_tps"]) for x in group if x.get("decode_tps") is not None]
        output.append({
            "model": model,
            "task_type": task_type,
            "runs": len(group),
            "mean_score": sum(scores) / len(scores),
            "median_latency_s": median(latency),
            "median_decode_tps": None if not decode else median(decode),
        })
    return output


def model_summary(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        if row.get("ok"):
            groups[row["model"]].append(row)
    out = []
    for model, group in sorted(groups.items()):
        out.append({
            "model": model,
            "attempts": len(group),
            "mean_score": sum(x["score"] for x in group) / len(group),
            "median_latency_s": median(x["elapsed_seconds"] for x in group),
            "total_output_tokens": sum(x.get("output_tokens") or 0 for x in group),
        })
    return out
