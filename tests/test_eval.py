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

from pydantic import ValidationError
import json,tempfile
class InputAndMetricTests(unittest.TestCase):
    def row(self,gold=None,candidate=None):
        return {"id":"one","source_text":"Synthetic asset has 20 sqm.","gold":gold or {"area_sqm":20},"candidate":candidate if candidate is not None else {"area_sqm":20}}
    def test_extra_claim_counted(self):
        result=harness.baseline(self.row(candidate={"area_sqm":20,"buyer":"invented"}))
        self.assertEqual((result.checked_claims,result.unsupported_claims),(2,1))
    def test_missing_is_not_hallucination(self):
        result=harness.baseline(self.row(candidate={}))
        self.assertEqual(result.checked_claims,0)
        self.assertEqual(result.unsupported_claims,0)
        self.assertEqual(result.completeness,0)
    def test_missing_null_is_not_match(self):
        result=harness.baseline(self.row(gold={"buyer":None},candidate={}))
        self.assertEqual(result.completeness,0)
    def test_boolean_is_not_numeric_fact(self):
        self.assertFalse(harness.exact(True,1))
    def test_bad_dataset_rows(self):
        for patch in ({"id":" "},{"source_text":""},{"gold":{}},{"candidate":[]}):
            with self.subTest(patch=patch),self.assertRaises(ValidationError):
                harness.DatasetRow.model_validate({**self.row(),**patch})
    def test_empty_evidence_rejected(self):
        row=harness.baseline(self.row()).model_dump();row["evidence_quote"]=""
        with self.assertRaises(ValidationError):harness.JudgeResult(**row)
    def test_duplicate_ids_and_zero_claim_denominator(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"data.jsonl";row=self.row(candidate={})
            p.write_text(json.dumps(row)+"\n")
            result=harness.run(p)
            self.assertEqual(result["exact_field_accuracy"],0)
            self.assertIsNone(result["unsupported_claim_rate"])
            p.write_text((json.dumps(row)+"\n")*2)
            with self.assertRaises(ValueError):harness.run(p)
