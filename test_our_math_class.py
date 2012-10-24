import unittest
import mock
import our_math_class

class TestOurMathClass(unittest.TestCase):
    def setUp(self):
        self.our_module = our_math_class.OurMathClass()
        
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

    def test_our_divide(self):
        """Dividing by zero should result in email being sent."""

        with mock.patch.object(our_math_class.OurMathClass, 'mail') as mail:
            result = self.our_module.divide(5, 0)
            mail.assert_called_once_with('zerowatcher5@foo.com')
