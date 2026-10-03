from argparse import ArgumentParser
from pathlib import Path
import json

from .compare import paired
from .io import read_jobs, read_rows
from .ollama import OllamaRunner
from .planner import expand
from .report import model_summary, summarize
from .runner import execute, write_jsonl
from .tasks import load


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("config")
    plan.add_argument("--tasks", default="tasks/core.jsonl")

    run = sub.add_parser("run")
    run.add_argument("plan")
    run.add_argument("--tasks", required=True)
    run.add_argument("--out", required=True)
    run.add_argument("--endpoint", default="http://127.0.0.1:11434")

    report = sub.add_parser("report")
    report.add_argument("path")
    report.add_argument("--models", action="store_true")

    compare = sub.add_parser("compare")
    compare.add_argument("path")
    compare.add_argument("left")
    compare.add_argument("right")

    args = parser.parse_args()

    if args.cmd == "plan":
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        task_ids = [x.id for x in load(args.tasks)]
        for job in expand(config, task_ids):
            print(json.dumps(job.to_dict(), sort_keys=True))
    elif args.cmd == "run":
        rows = execute(read_jobs(args.plan), load(args.tasks), OllamaRunner(args.endpoint))
        write_jsonl(args.out, rows)
        print(json.dumps({"attempts": len(rows), "completed": sum(bool(x.get("ok")) for x in rows)}))
    elif args.cmd == "report":
        rows = read_rows(args.path)
        print(json.dumps(model_summary(rows) if args.models else summarize(rows), indent=2))
    else:
        print(json.dumps(paired(read_rows(args.path), args.left, args.right), indent=2))


if __name__ == "__main__":
    main()
