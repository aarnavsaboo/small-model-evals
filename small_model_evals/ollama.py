from time import perf_counter
from urllib.request import Request, urlopen
import json


class OllamaRunner:
    def __init__(self, endpoint: str = "http://127.0.0.1:11434"):
        self.endpoint = endpoint.rstrip("/")

    def generate(self, model: str, prompt: str, max_tokens: int, temperature: float, seed: int | None):
        options = {"num_predict": max_tokens, "temperature": temperature}
        if seed is not None:
            options["seed"] = seed
        body = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }).encode()
        req = Request(
            self.endpoint + "/api/generate",
            data=body,
            headers={"Content-Type":"application/json"},
            method="POST",
        )
        started = perf_counter()
        with urlopen(req, timeout=600) as response:
            row = json.load(response)
        elapsed = perf_counter() - started
        eval_count = row.get("eval_count")
        eval_duration = row.get("eval_duration")
        decode_tps = None
        if eval_count and eval_duration:
            decode_tps = eval_count / (eval_duration / 1e9)
        return {
            "text": row.get("response", ""),
            "elapsed_seconds": elapsed,
            "prompt_tokens": row.get("prompt_eval_count"),
            "output_tokens": eval_count,
            "decode_tps": decode_tps,
            "load_seconds": None if row.get("load_duration") is None else row["load_duration"] / 1e9,
        }
