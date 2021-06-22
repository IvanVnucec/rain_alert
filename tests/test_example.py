"""
This file serves as test template!
"""

import unittest


class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(3+2+1, 6, "Message if fail")

    def test_another(self):
        self.assertEqual("Bok kaj ima lima", "Bok kaj ima lima")
        self.assertEqual("Nema pojma", "Nema pojma")


if __name__ == '__main__':
    unittest.main()
