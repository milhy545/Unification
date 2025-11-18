import unittest
from tools.system_detector import SystemDetector

class TestSystemDetector(unittest.TestCase):
    def setUp(self):
        self.sd = SystemDetector()

    def test_detect_basic_info_keys(self):
        info = self.sd.detect_basic_info()
        # Ensure required keys exist
        for key in ["hostname", "os", "os_version", "arch", "python"]:
            self.assertIn(key, info)
            self.assertIsInstance(info[key], str)
            self.assertTrue(len(info[key]) >= 0)

if __name__ == '__main__':
    unittest.main()
