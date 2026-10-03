import unittest

from small_model_evals.scoring import exact, keywords, score
from small_model_evals.tasks import Task
from small_model_evals.planner import expand


class Tests(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(exact("Reciprocal-rank fusion", "reciprocal rank fusion"), 1)

    def test_keywords(self):
        self.assertEqual(keywords("lower memory and lower latency", ("memory","latency")), 1)

    def test_task_score(self):
        task = Task("x","keywords","p",required=("memory","latency"))
        self.assertEqual(score(task, "memory and latency"), 1)

    def test_plan(self):
        rows = expand({"models":["a","b"],"repeats":2,"temperature":[0]}, ["t1","t2"])
        self.assertEqual(len(rows), 8)


if __name__ == "__main__":
    unittest.main()
