import unittest
import os
from utils.productivity import ProductivityTools

class TestProductivity(unittest.TestCase):
    def test_pptx_creation(self):
        topic = "Test Topic"
        content = "This is a test content"
        result = ProductivityTools.create_powerpoint(topic, content)
        self.assertIn("Presentation created successfully", result)
        filename = f"assets/{topic.replace(' ', '_')}.pptx"
        self.assertTrue(os.path.exists(filename))
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
