# small-model-evals

A local evaluation harness for comparing small language models on repeatable application-shaped workloads.

The repository is aimed at the practical question behind local deployment: how much useful task performance is retained when moving from a larger model to a smaller one that loads faster, uses less memory and produces tokens faster?

Instead of a single aggregate benchmark, task packs keep several workload types separate and record systems measurements beside task scores.

## Workload families

- short factual question answering
- retrieval-assisted question answering
- multiple-choice reasoning
- concise summarization
- constrained rewriting
- information extraction
- short code explanation
- instruction following with output-length limits

## Run model matrices

```bash
python -m small_model_evals plan configs/local-matrix.json > runs/plan.jsonl

python -m small_model_evals run \
  runs/plan.jsonl \
  --tasks tasks/core.jsonl \
  --out runs/raw.jsonl

python -m small_model_evals report runs/raw.jsonl
```

## Measurements

Each attempt can store:

- exact model and runtime
- task family
- prompt size
- requested output budget
- generated text
- task score
- wall-clock latency
- prompt token count
- output token count
- decode throughput when exposed by the runtime
- repeated-run index
- generation settings

The reporting layer keeps quality and systems measurements separate. A small model can be faster but fail a task floor; a larger model can improve quality while reducing throughput enough to be impractical for a repeated local workflow.

## Task packs

Task packs are JSONL so custom workloads can be added without changing Python code.

```json
{"id":"mc-1","type":"choice","prompt":"...","choices":["A","B","C"],"answer":"B"}
{"id":"qa-1","type":"exact","prompt":"...","answer":"reciprocal-rank fusion"}
{"id":"sum-1","type":"keywords","prompt":"...","required":["retrieval","reranking"]}
```

The included tasks are deliberately tiny examples, not claims of a broad benchmark.

## Architecture

```text
task pack + model matrix
          |
          v
       planner
          |
          v
   local-model runner
          |
          +--> response text
          +--> timings
          +--> token counts
          |
          v
        scorer
          |
          v
       raw JSONL
          |
       +--+--+
       |     |
       v     v
    report  pairwise deltas
```

## Repository layout

- `tasks.py` — task records and JSONL loader
- `planner.py` — model/task/repeat matrix expansion
- `ollama.py` — local runtime adapter
- `scoring.py` — deterministic task scorers
- `runner.py` — execution and raw records
- `report.py` — per-model and per-task summaries
- `compare.py` — paired quality/latency deltas
- `configs/` — example model matrices
- `tasks/` — small fixture task packs
- `tests/` — deterministic tests

Maintained by **Aarnav Saboo**.
