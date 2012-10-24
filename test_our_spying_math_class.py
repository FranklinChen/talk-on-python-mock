import unittest
import our_spying_math_class

class TestOurSpyingMathClass(unittest.TestCase):
    def setUp(self):
        self.our_module = our_spying_math_class.OurSpyingMathClass()
        
    def test_our_add(self):
        """Our addition function should work on 2 and 3."""

        # arrange
        x = 2
        y = 3
        expected_result = 5

        # act; assert
        self.assertEqual(self.our_module.add(x, y), expected_result)

    # Another test in same test case.
    def test_our_multiply(self):
        """Our multiply function should work on 3 and 4."""

        self.assertEqual(self.our_module.multiply(3, 4), 12)

    def test_our_double_with_multiply(self):
        """Our double function should not work by multiplying."""

        result = self.our_module.double(5)
        self.assertEqual(self.our_module.multiply_call_count, 0)
