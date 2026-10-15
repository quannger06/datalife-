"""Test actual team modules once both feature PRs have been merged."""
import importlib.util
import unittest
from main import collect_messages


class IntegrationTests(unittest.TestCase):
    def test_combined_features(self):
        missing = [name for name in ("hello", "xinchao")
                   if importlib.util.find_spec(f"features.{name}") is None]
        if missing:
            self.skipTest("Scaffold phase; waiting for: " + ", ".join(missing))
        messages, pending = collect_messages(require_all=True)
        self.assertEqual(messages, ["Hello World", "Xin chào World"])
        self.assertEqual(pending, [])
