from our_math_class import OurMathClass

class OurSpyingMathClass(OurMathClass):
    def __init__(self):
        self.multiply_call_count = 0

    # Override
    def multiply(self, x, y):
        """Return product of x and y while spying."""
        self.multiply_call_count += 1

        # Python 2.7 classes
        return super(OurSpyingMathClass, self).multiply(x, y)
