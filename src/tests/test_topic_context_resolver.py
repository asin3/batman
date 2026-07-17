import unittest

from src.understanding.conversation_state import reset_state
from src.understanding.engine import understand
from src.understanding.topic_context_resolver import resolve_topic_context


class TopicContextResolverTests(unittest.TestCase):

    def test_quick_quiz_uses_current_learning_topic(self):

        reset_state()

        understanding = understand(
            "quick quiz 2 easy",
            student_id="TEST_STUDENT"
        )

        decision = resolve_topic_context(
            understanding,
            learning_state={
                "topic": "Neuron",
                "chapter": "Nervous System"
            },
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        self.assertEqual(
            decision,
            {
                "explicit_topic": None,
                "resolved_topic": "Neuron",
                "source": "learning_state",
                "confidence": 0.75,
                "needs_clarification": False
            }
        )

    def test_missing_topic_requires_clarification(self):

        decision = resolve_topic_context(
            {
                "entities": {
                    "topic": None
                }
            },
            learning_state={},
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        self.assertIsNone(
            decision["resolved_topic"]
        )
        self.assertTrue(
            decision["needs_clarification"]
        )

    def test_explicit_new_topic_wins_over_learning_state(self):

        decision = resolve_topic_context(
            {
                "entities": {
                    "topic": "Quick On Force"
                }
            },
            learning_state={
                "topic": "Neuron"
            },
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        self.assertEqual(
            decision,
            {
                "explicit_topic": "Force",
                "resolved_topic": "Force",
                "source": "explicit",
                "confidence": 1.0,
                "needs_clarification": False
            }
        )

    def test_ambiguous_topic_reference_requires_context(self):

        decision = resolve_topic_context(
            {
                "entities": {
                    "topic": "Same Topic"
                }
            },
            learning_state={},
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        self.assertIsNone(
            decision["explicit_topic"]
        )
        self.assertIsNone(
            decision["resolved_topic"]
        )
        self.assertTrue(
            decision["needs_clarification"]
        )

    def test_tutor_question_cleans_topic_phrase(self):

        decision = resolve_topic_context(
            {
                "entities": {
                    "topic": "What Is Neuron?"
                }
            },
            learning_state={},
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        self.assertEqual(
            decision["resolved_topic"],
            "Neuron"
        )
        self.assertEqual(
            decision["source"],
            "explicit"
        )

    def test_explain_request_cleans_leading_article(self):

        decision = resolve_topic_context(
            {
                "entities": {
                    "topic": "Explain The Neuron"
                }
            },
            learning_state={},
            conversation_state={
                "entities": {
                    "topic": None
                }
            }
        )

        self.assertEqual(
            decision["resolved_topic"],
            "Neuron"
        )
        self.assertFalse(
            decision["needs_clarification"]
        )


if __name__ == "__main__":

    unittest.main()
