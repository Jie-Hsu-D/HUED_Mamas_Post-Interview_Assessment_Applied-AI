import copy
import json
import pathlib
import unittest

from src.explainer import ExplanationError, render_explanation


ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES = [json.loads(path.read_text()) for path in sorted((ROOT / "cases").glob("*.json"))]
FORBIDDEN = {
    "you should",
    "we recommend",
    "consult",
    "seek care",
    "treatment",
    "diagnosis",
    "will become pregnant",
    "caused by",
}


class ExplanationContractTests(unittest.TestCase):
    def test_same_input_same_output(self):
        for case in CASES:
            first = render_explanation(copy.deepcopy(case), "patient")
            second = render_explanation(copy.deepcopy(case), "patient")
            self.assertEqual(first, second)

    def test_both_audiences_preserve_facts(self):
        for case in CASES:
            patient = render_explanation(copy.deepcopy(case), "patient")
            provider = render_explanation(copy.deepcopy(case), "provider")
            self.assertEqual(patient["facts"], provider["facts"])

    def test_forbidden_language_is_absent(self):
        for case in CASES:
            for audience in ("patient", "provider"):
                output = json.dumps(render_explanation(copy.deepcopy(case), audience)).lower()
                for phrase in FORBIDDEN:
                    self.assertNotIn(phrase, output)

    def test_unknown_fields_are_rejected(self):
        case = copy.deepcopy(CASES[0])
        case["raw_lab_value"] = "unexpected"
        with self.assertRaises(ExplanationError):
            render_explanation(case, "patient")

    def test_unknown_version_is_rejected(self):
        case = copy.deepcopy(CASES[0])
        case["score_version"] = "UNKNOWN"
        with self.assertRaises(ExplanationError):
            render_explanation(case, "patient")

    def test_audit_event_contains_no_bounded_payload(self):
        output = render_explanation(copy.deepcopy(CASES[0]), "patient")
        audit = output["audit_event"]
        serialized = json.dumps(audit)
        self.assertNotIn("contributors", serialized)
        self.assertNotIn("missing_domains", serialized)
        self.assertNotIn("score\"", serialized)


if __name__ == "__main__":
    unittest.main()

