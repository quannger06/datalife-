"""Exercise the real CLI in isolated projects without modifying team files."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELLO = 'def hello():\n    return "Hello World"\n'
XINCHAO = 'def xinchao():\n    return "Xin chào World"\n'


class RunnerTests(unittest.TestCase):
    def run_project(self, modules, strict=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copyfile(ROOT / "main.py", root / "main.py")
            (root / "features").mkdir()
            (root / "features" / "__init__.py").write_text("", encoding="utf-8")
            for name, code in modules.items():
                (root / "features" / f"{name}.py").write_text(code, encoding="utf-8")
            command = [sys.executable, "-X", "utf8", "main.py"]
            if strict:
                command.append("--require-all")
            return subprocess.run(command, cwd=root, capture_output=True,
                                  text=True, encoding="utf-8", timeout=15)

    def test_empty_scaffold_reports_pending_features(self):
        result = self.run_project({})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(),
                         ["Waiting for feature: hello", "Waiting for feature: xinchao"])

    def test_hello_can_arrive_first(self):
        result = self.run_project({"hello": HELLO})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(),
                         ["Hello World", "Waiting for feature: xinchao"])

    def test_xinchao_can_arrive_first(self):
        result = self.run_project({"xinchao": XINCHAO})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(),
                         ["Xin chào World", "Waiting for feature: hello"])

    def test_both_features_produce_exact_output(self):
        result = self.run_project({"hello": HELLO, "xinchao": XINCHAO}, strict=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["Hello World", "Xin chào World"])

    def test_strict_mode_rejects_missing_feature(self):
        result = self.run_project({"hello": HELLO}, strict=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required features: xinchao", result.stderr)

    def test_wrong_result_fails(self):
        result = self.run_project({"hello": 'def hello(): return "Wrong"'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError", result.stderr)

    def test_missing_function_fails(self):
        result = self.run_project({"hello": "value = 1"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AttributeError", result.stderr)

    def test_internal_missing_dependency_is_not_skipped(self):
        result = self.run_project({"hello": "import missing_dependency_for_test"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ModuleNotFoundError", result.stderr)

    def test_runtime_error_is_not_skipped(self):
        result = self.run_project({"hello": 'def hello(): raise RuntimeError("broken")'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RuntimeError: broken", result.stderr)
