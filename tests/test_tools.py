import unittest
from utils.tools import get_time, get_system_stats

class TestJarvisTools(unittest.TestCase):
    def test_get_time(self):
        time_str = get_time()
        self.assertIsInstance(time_str, str)
        self.assertEqual(len(time_str), 5) # HH:MM

    def test_get_system_stats(self):
        stats = get_system_stats()
        self.assertIn("Sir", stats)

if __name__ == "__main__":
    unittest.main()
