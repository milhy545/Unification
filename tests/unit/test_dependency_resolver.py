import unittest
from tools.dependency_resolver import DependencyResolver

class TestDependencyResolver(unittest.TestCase):
    def setUp(self):
        self.dr = DependencyResolver()

    def test_common_packages_exist(self):
        # Ensure core mappings exist
        for pkg in ["git", "python3", "pip", "curl", "wget"]:
            self.assertIn(pkg, self.dr.COMMON_PACKAGES)

    def test_package_manager_names_present(self):
        # Verify at least APT/APK/PACMAN names are present for key packages
        pkgs = self.dr.COMMON_PACKAGES
        self.assertEqual(pkgs["git"].apt_name, "git")
        self.assertIsNotNone(pkgs["git"].pacman_name)
        self.assertIsNotNone(pkgs["git"].apk_name)

        self.assertIsNotNone(pkgs["python3"].apt_name)
        self.assertIsNotNone(pkgs["python3"].pacman_name)
        self.assertIsNotNone(pkgs["python3"].apk_name)

        self.assertIsNotNone(pkgs["pip"].apt_name)
        self.assertIsNotNone(pkgs["pip"].pacman_name)
        self.assertIsNotNone(pkgs["pip"].apk_name)

if __name__ == '__main__':
    unittest.main()
