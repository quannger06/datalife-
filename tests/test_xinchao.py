import unittest
from features.xinchao import xinchao

class XinChaoTests(unittest.TestCase):
    def test_xinchao(self):
        self.assertEqual(xinchao(), "Xin chào World")
