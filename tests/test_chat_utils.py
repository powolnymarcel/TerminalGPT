"""Tests for chat_utils.py."""

import unittest

from terminalgpt import chat_utils


class TestChatUtils(unittest.TestCase):
    """Tests for chat_utils.py."""

    def set_test(self):
        """Sets a test."""

        messages = [
            {"role": "system", "content": "Hello user"},
            {"role": "user", "content": "Hello system"},
            {"role": "assistant", "content": "Hello user"},
            {"role": "user", "content": "Hello assistant"},
        ]
        return messages

    def test_exceeding_token_limit(self):
        """Tests exceeding_token_limit function."""

        self.assertTrue(chat_utils.exceeding_token_limit(1025, 1024))
        self.assertFalse(chat_utils.exceeding_token_limit(1000, 1023))

    def test_validate_token_limit(self):
        """Tests validate_token_limit function."""

        self.assertEqual(chat_utils.validate_token_limit(None, None, 1024), 1024)
        self.assertEqual(chat_utils.validate_token_limit(None, None, 2048), 2048)
        self.assertEqual(chat_utils.validate_token_limit(None, None, 4096), 4096)

        with self.assertRaises(ValueError):
            chat_utils.validate_token_limit(None, None, 512)

        with self.assertRaises(ValueError):
            chat_utils.validate_token_limit(None, None, 8192)

        with self.assertRaises(ValueError):
            chat_utils.validate_token_limit(None, None, 1023)

    def test_count_all_tokens(self):
        """Tests count_all_tokens function."""

        messages = self.set_test()
        total_usage = chat_utils.count_all_tokens(messages)
        self.assertEqual(total_usage, 26)

    def test_reduce_tokens(self):
        """Tests reduce_tokens function."""

        token_limit = 24
        messages = self.set_test()
        total_usage = chat_utils.count_all_tokens(messages)

        messages, total_usage = chat_utils.reduce_tokens(
            messages, token_limit, total_usage
        )

        self.assertEqual(total_usage, token_limit)
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "Hello user")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "")

        token_limit = 21
        messages = self.set_test()
        total_usage = chat_utils.count_all_tokens(messages)

        messages, total_usage = chat_utils.reduce_tokens(
            messages, token_limit, total_usage
        )

        self.assertEqual(total_usage, token_limit)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "Hello user")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], " assistant")


if __name__ == "__main__":
    unittest.main()
