import unittest
from blackjack import api

class TestValidateUsername(unittest.TestCase):

    def test_invalid_characters(self):
        self.assertFalse(api.validateUsername("test_string;"))

    def test_too_short_string(self):
        self.assertFalse(api.validateUsername(""))
        self.assertFalse(api.validateUsername("a"))
        self.assertFalse(api.validateUsername("6"))

    def test_too_long_string(self):
        self.assertFalse(api.validateUsername("""Lorem ipsum dolor sit amet,
        consectetur adipiscing elit. Maecenas rhoncus venenatis ante.
        Curabitur in suscipit justo. Cras at tellus sit amet mauris pretium
        maximus nec a risus. Quisque ut hendrerit felis, finibus sodales
        est. Proin rutrum,"""))

    def test_numerical_characters(self):
        self.assertTrue(api.validateUsername("000143"))
        self.assertTrue(api.validateUsername("tstring1"))


if __name__ == '__main__':
    unittest.main()