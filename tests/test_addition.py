import unittest

from utils.addition import addition


class TestAddition(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(addition(1, 2), 3)
        self.assertEqual(addition(2, 3), 5)


# if __name__ == "__main__":
#     unittest.main()
