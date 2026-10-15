import unittest
from features.hello import hello

class HelloTests(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello World")
