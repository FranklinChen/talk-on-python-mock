class OurMathClass(object):
    def add(self, x, y):
        """Return sum of x and y using clever algorithm."""
        return x + y

    def multiply(self, x, y):
        """Return product of x and y using clever algorithm."""
        return x * y

    def double(self, x):
        """Return double x."""
        return self.multiply(2, x)

    def divide(self, x, y):
        """Return division of x and y, sending email if y is 0."""
        if y == 0:
            self.mail('zerowatcher' + str(x) + '@foo.com')
        else:
            return x / y

    # TODO implement
    def mail(self):
        """Email a message."""
        pass
