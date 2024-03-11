import unittest

list = [
    15,
    47,
    48,
    50,
    42,
    1,
    41,
    36,
    32,
    29,
    44,
    13,
    33,
    21,
    31,
    25,
    4,
    16,
    10,
    20,
    12,
    45,
    27,
    22,
    8,
    26,
    2,
    46,
    30,
    38,
    7,
    23,
    34,
    17,
    28,
    6,
    3,
    5,
    18,
    19,
    49,
    39,
    11,
    40,
    14,
    37,
    9,
    43,
    35,
    24,
]


def oracle(input):
    correct = 9
    if input is correct:
        return True
    else:
        return False


class TestClassicalImplementation(unittest.TestCase):
    def test_classical_search(self):
        for index, guess in enumerate(list):
            if oracle(guess) is True:
                print("Solution Found at index %i" % index)
                print("It took %i calls to the oracle" % (index + 1))
                break

                self.assertTrue(False)
