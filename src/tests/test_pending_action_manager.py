import tempfile
import unittest
from pathlib import Path

from src.conversation.pending_action_manager import (
    build_pending_action,
    build_pending_action_prompt,
    clear_pending_action,
    extract_pending_action_from_response,
    load_pending_action,
    resolve_pending_action_response,
    save_pending_action
)


class PendingActionManagerTests(unittest.TestCase):

    def test_save_load_and_clear_pending_action(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            data_dir = Path(temp_dir)

            action = build_pending_action(
                "Would you like me to explain the three types of neurons?",
                topic="Neuron"
            )

            save_pending_action(
                "TEST_STUDENT",
                action,
                data_dir=data_dir
            )

            loaded = load_pending_action(
                "TEST_STUDENT",
                data_dir=data_dir
            )

            self.assertEqual(
                loaded["action_id"],
                action["action_id"]
            )

            clear_pending_action(
                "TEST_STUDENT",
                data_dir=data_dir
            )

            self.assertIsNone(
                load_pending_action(
                    "TEST_STUDENT",
                    data_dir=data_dir
                )
            )

    def test_extract_pending_action_from_offer_response(self):

        action = extract_pending_action_from_response(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        self.assertIsNotNone(action)
        self.assertEqual(
            action["action_type"],
            "EXPLAIN_MORE"
        )
        self.assertEqual(
            action["topic"],
            "Neuron"
        )

    def test_accept_pending_action_from_text(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            "go ahead",
            action
        )

        self.assertEqual(
            decision["decision"],
            "ACCEPT_PENDING_ACTION"
        )

    def test_reject_pending_action_from_text(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            "not now",
            action
        )

        self.assertEqual(
            decision["decision"],
            "REJECT_PENDING_ACTION"
        )

    def test_structured_drona_accept_event(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            {
                "type": "PENDING_ACTION_RESPONSE",
                "action_id": action["action_id"],
                "response": "ACCEPT"
            },
            action
        )

        self.assertEqual(
            decision["decision"],
            "ACCEPT_PENDING_ACTION"
        )

    def test_simplify_pending_action(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            "I did not understand that part",
            action
        )

        self.assertEqual(
            decision["decision"],
            "SIMPLIFY_CONTEXT"
        )

    def test_refine_pending_action_for_specific_part(self):

        action = build_pending_action(
            "Would you like me to explain sensory, motor, and relay neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            "explain relay neuron",
            action
        )

        self.assertEqual(
            decision["decision"],
            "REFINE_PENDING_ACTION"
        )

    def test_quiz_request_replaces_pending_with_quiz_flow(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            "quiz me",
            action
        )

        self.assertEqual(
            decision["decision"],
            "START_QUIZ_FROM_CONTEXT"
        )

    def test_new_request_replaces_pending_action(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        decision = resolve_pending_action_response(
            "what is force",
            action
        )

        self.assertEqual(
            decision["decision"],
            "REPLACE_WITH_NEW_REQUEST"
        )

    def test_pending_action_prompt_contains_offer_and_decision(self):

        action = build_pending_action(
            "Would you like me to explain the three types of neurons?",
            topic="Neuron"
        )

        prompt = build_pending_action_prompt(
            "yes",
            action,
            "assistant: Would you like me to explain the three types of neurons?",
            "Batman rules",
            {
                "decision": "ACCEPT_PENDING_ACTION"
            }
        )

        self.assertIn(
            "ACCEPT_PENDING_ACTION",
            prompt
        )
        self.assertIn(
            "Would you like me to explain the three types of neurons?",
            prompt
        )


if __name__ == "__main__":

    unittest.main()
