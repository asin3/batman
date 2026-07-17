import unittest

from src.understanding.clarification_engine import needs_clarification
from src.understanding.engine import understand


class ContinuationFlowTests(unittest.TestCase):

    def test_yes_please_is_continuation(self):

        result = understand(
            "yes please",
            student_id="TEST_STUDENT"
        )

        self.assertEqual(
            result["intent"]["name"],
            "CONTINUATION"
        )
        self.assertTrue(
            result["confidence"]["complete"]
        )
        self.assertIsNone(
            result["clarification"]
        )

    def test_did_not_understand_is_continuation(self):

        result = understand(
            "I didn't understand the difference between relay and ascending neurons",
            student_id="TEST_STUDENT"
        )

        self.assertEqual(
            result["intent"]["name"],
            "CONTINUATION"
        )
        self.assertIsNone(
            result["clarification"]
        )

    def test_empty_missing_clarification_does_not_crash(self):

        clarification = needs_clarification(
            intent=None,
            entities={},
            confidence={
                "complete": False,
                "missing": []
            }
        )

        self.assertEqual(
            clarification,
            {
                "field": "intent",
                "question": "Can you say a little more?"
            }
        )

if __name__ == "__main__":

    unittest.main()
