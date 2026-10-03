# Methodology

Small-model evaluation is most useful when task score and systems cost are kept side by side.

A model can be attractive because it loads quickly and generates rapidly but still miss a minimum quality floor. Conversely, a larger model can improve a task score by a few points while doubling latency and memory.

For repeated experiments:

1. freeze task prompts before comparing models;
2. keep generation settings constant;
3. repeat deterministic or low-temperature runs;
4. keep raw generated text;
5. report per-task-family scores;
6. compare models on paired tasks;
7. avoid collapsing everything into one weighted leaderboard.

The sample task pack is intentionally tiny. It exists to exercise the harness, not to establish a general ranking of models.
