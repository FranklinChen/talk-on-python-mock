import unittest
import mock
import our_module

class TestOurModule(unittest.TestCase):
    def test_our_add(self):
        """Our addition function should work on 2 and 3."""

        # arrange
        x = 2
        y = 3
        expected_result = 5

        # act; assert
        self.assertEqual(our_module.add(x, y), expected_result)

    # Another test in same test case.
    def test_our_multiply(self):
        """Our multiply function should work on 3 and 4."""

        self.assertEqual(our_module.multiply(3, 4), 12)

    @mock.patch('our_module.multiply')
    def test_our_double_with_multiply(self, fake_multiply):
        """Our double function should not work by multiplying."""

        result = our_module.double(5)
        self.assertEqual(fake_multiply.call_count, 0)

    @mock.patch('our_module.add')
    def test_our_double_with_add(self, fake_add):
        """Our double function should work by adding."""

        result = our_module.double(5)
        self.assertEqual(fake_add.call_count, 1)
