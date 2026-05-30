import unittest
from utils.scripting import ScriptingTools
import os

class TestScripting(unittest.TestCase):
    def test_python_execution(self):
        code = "print('Hello Jarvis')"
        result = ScriptingTools.execute_python_code(code)
        self.assertIn("Hello Jarvis", result)
        self.assertIn("Execution complete", result)

if __name__ == "__main__":
    unittest.main()
