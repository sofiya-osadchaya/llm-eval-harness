import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("harness",Path(__file__).parents[1]/"eval.py")
harness=importlib.util.module_from_spec(spec);spec.loader.exec_module(harness)
def test_corrupted_candidates_are_detected():
    r=harness.run(Path(__file__).parents[1]/"data/synthetic.jsonl")
    assert r["total_fields"]==40 and r["correct_fields"]==36
    assert r["unsupported_claims"]==4 and r["checked_claims"]==40

import unittest
class EvaluationTests(unittest.TestCase):
    def test_corrupted_candidates(self):test_corrupted_candidates_are_detected()
