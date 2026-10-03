from collections import defaultdict


def paired(rows: list[dict], left_model: str, right_model: str) -> dict:
    by_key = defaultdict(dict)
    for row in rows:
        if row.get("ok") and row["model"] in {left_model, right_model}:
            key = (row["task_id"], row["repeat"], row.get("temperature", 0.0))
            by_key[key][row["model"]] = row

    pairs = [
        values for values in by_key.values()
        if left_model in values and right_model in values
    ]
    if not pairs:
        return {"pairs": 0}

    score_delta = [
        x[right_model]["score"] - x[left_model]["score"]
        for x in pairs
    ]
    latency_delta = [
        x[right_model]["elapsed_seconds"] - x[left_model]["elapsed_seconds"]
        for x in pairs
    ]
    return {
        "pairs": len(pairs),
        "mean_score_delta_right_minus_left": sum(score_delta) / len(score_delta),
        "mean_latency_delta_s_right_minus_left": sum(latency_delta) / len(latency_delta),
        "right_score_wins": sum(x > 0 for x in score_delta),
        "score_ties": sum(x == 0 for x in score_delta),
        "right_score_losses": sum(x < 0 for x in score_delta),
    }
