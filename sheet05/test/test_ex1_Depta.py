import unittest
import ex1_Depta as Ex


class TestValue(unittest.TestCase):
    def test_str(self):
        int_val = Ex.IntValue(1)
        self.assertEqual(str(int_val), "IntValue(1)")


if __name__ == '__main__':
    unittest.main()
