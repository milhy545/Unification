import unittest
from tools import preconditions as pc

class TestPreconditions(unittest.TestCase):
    def test_has_command_positive(self):
        # python3 should exist in this environment
        self.assertTrue(pc.has_command('python3') or pc.has_command('python'))

    def test_has_command_negative(self):
        self.assertFalse(pc.has_command('definitely-not-a-real-cmd-xyz'))

    def test_is_root_or_sudo_flag(self):
        # We don't know the environment, but function must return bool
        self.assertIsInstance(pc.is_root_or_sudo(), bool)

    def test_has_network_returns_bool(self):
        self.assertIsInstance(pc.has_network(timeout=0.5), bool)

if __name__ == '__main__':
    unittest.main()
