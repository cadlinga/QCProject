import unittest

from utils.addition import addition


class TestAddition(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(addition(1, 3), 4)


# if __name__ == "__main__":
#     unittest.main()
