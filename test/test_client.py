import unittest
import os
import platform
import shutil
import sys
from io import StringIO
from onepassword import OnePassword


def set_up_one_password():
    """Set up a mock OnePassword Vault"""
    domain = "test"
    email = "user@test.com"
    secret = "test_secret"
    password = "test_password"
    os.mkdir("test_utilities")
    with open('test_utilities/.bash_profile', 'w') as f:
        f.write("")
    f.close()
    return OnePassword(domain=domain, email=email, secret=secret, password=password)


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('--- Set up TestClient ---')
        cls.test_path = 'test_utilities'
        if str(platform.system()) == 'Linux':
            cls.user_home = "/usr/local/bin"
        else:
            cls.user_home = os.environ["HOME"]
        cls.op = set_up_one_password()

    @classmethod
    def tearDownClass(cls):
        print('--- Tear down TestUtilities ---')
        path = 'test_utilities'
        shutil.rmtree(path)

    def setUp(self):
        """Record print statements per test"""
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        """Clear print statements after each test"""
        sys.stdout = self.held
        os.environ["HOME"] = self.user_home

    @unittest.skip("Travis not installing op - test in docker?")
    def test_install(self):
        self.assertTrue(os.path.exists(os.path.join(self.user_home, "op")))

    def test_first_use(self):
        """
        Tested by signin_wrapper hence signin by proxy.
        """
        pass

    def test_signin_wrapper(self):
        """
        Tested by signin.
        """
        pass

    @unittest.skip("Jenkins bash profile cannot be read.")
    def test_signin(self):
        p, s, d, b = self.op.signin(self.op.signin_domain, self.op.email_address, self.op.secret_key, "test_password")
        self.assertEqual(p, b"test_password")
        self.assertIn(b"(ERROR)  invalid account key length\n", s)
        self.assertEqual(d, "test")
        self.assertGreater(len(b.profile_lines), 0)

    def test_get_uuid(self):
        """
        Without user interaction will not be signed in and be unable to get anything
        """
        pass

    def test_get_document(self):
        """
        Without user interaction will not be signed in and be unable to get anything
        """
        pass

    def test_put_document(self):
        """
        Tested in signin and read_bash_return.
        """
        pass

    def test_update_document(self):
        """
        Tested in delete_document, put_document and os.
        """
        pass

    def test_delete_document(self):
        """
        Tested in signing, get_uuid and read_bash_return.
        """
        pass

    def test_signout(self):
        """
        Tested in read_bash_return.
        """
        pass

    def test_list_vaults(self):
        """
        Tested in read_bash_return.
        """
        pass

    def test_get_items(self):
        """
        Without user interaction will not be signed in and be unable to list anything
        """
        pass


if __name__ == '__main__':
    unittest.main()
