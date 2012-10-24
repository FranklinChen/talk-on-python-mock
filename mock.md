# Testing with isolation: concepts and examples using the [Python standard library `mock`](http://www.voidspace.org.uk/python/mock/) <br> <i>Franklin Chen</i> <br> <i>[http://franklinchen.com/](http://franklinchen.com/)</i> <br> [Pittsburgh Python](http://www.meetup.com/pghpython/) <br> October 23, 2012

---

# Why this talk?

# "The best way to learn something is to teach it."

- resistance
- confusion
- understanding

---

# Mocks: controversial

# [Gregory Moeck: "Why You Don't Get Mock Objects", RubyConf 2011](http://www.confreaks.com/videos/659-rubyconf2011-why-you-don-t-get-mock-objects)

- advocates correct use of mocks
- (examples in Ruby)

# [Martin Fowler: "Mocks Aren't Stubs"](http://martinfowler.com/articles/mocksArentStubs.html), 2007

- objective comparison
- himself chooses not to use mocks
- (examples in Java)

# [Brett Schuchert: "Modern Mocking Tools and Black Magic"](http://www.martinfowler.com/articles/modernMockingTools.html), September 2012

- the power of mocking tools, but dangers

---

# Outline of presentation

- basic concepts in testing
- what is a mock anyway?
- types of test doubles
- using mocks

---

# Types of tests

# Terminology

Gerard Meszaros's, "xUnit Test Patterns", 2007.

"System under test" (SUT)

# Different scopes

- acceptance test
- integration test
- unit test

---

# Focus on unit testing

Scope: class or module

- arrange
- act
- assert

[`unittest`](http://docs.python.org/library/unittest.html): test framework included in Python standard library

[Many others exist.](http://wiki.python.org/moin/PythonTestingToolsTaxonomy)

---

# `unittest` example

    !python
    import unittest
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

---

# Running the unit test

(Assume Python 2.7 or higher, for nice test discovery features.)

    !console
    $ python -m unittest discover

Oops, where is `our_module`?

    !console
    E
    ======================================================================
    ERROR: test_our_module (unittest.loader.ModuleImportFailure)
    ----------------------------------------------------------------------
    ImportError: Failed to import test module: test_our_module
    Traceback (most recent call last):
      File "/usr/local/Cellar/python/2.7.3/lib/python2.7/unittest/loader.py", line 252, in _find_tests
        module = self._get_module_from_name(name)
      File "/usr/local/Cellar/python/2.7.3/lib/python2.7/unittest/loader.py", line 230, in _get_module_from_name
        __import__(name)
      File "/Users/chen/Dropbox/pghpython/2012-10-24/talk-on-python-mock/test_our_module.py", line 2, in <module>
        import our_module
    ImportError: No module named our_module


    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (errors=1)

---

# [Test-driven development (TDD)](http://en.wikipedia.org/wiki/Test-driven_development)

Our test case `test_our_module` failed because we had not yet written `our_module.py` at all!

This is *on purpose*.

- write test first
- see test fail
- write code to make test succeed
- repeat

---

# Implementing our module

Creating `our_module.py`:

    !python
    # Note: this is deliberately buggy!
    def add(x, y):
        """Return sum of x and y using clever algorithm."""
        return x + y + 1

---

# Rerunning tests

    !console
    $ python -m unittest discover
    FE
    ======================================================================
    ERROR: test_our_multiply (test_our_module.TestOurModule)
    Our multiply function should work on 3 and 4.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/chen/Dropbox/pghpython/2012-10-24/talk-on-python-mock/test_our_module.py", line 20, in test_our_multiply
        self.assertEqual(our_module.multiply(3, 4), 12)
    AttributeError: 'module' object has no attribute 'multiply'

    ======================================================================
    FAIL: test_our_add (test_our_module.TestOurModule)
    Our addition function should work on 2 and 3.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/chen/Dropbox/pghpython/2012-10-24/talk-on-python-mock/test_our_module.py", line 14, in test_our_add
        self.assertEqual(our_module.add(x, y), expected_result)
    AssertionError: 6 != 5

    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    FAILED (failures=1, errors=1)

---

# Skipping tests

We want to focus *only* on `test_our_add` for now, so mark `test_our_multiply` as **skipped** for now:

    !python
        @unittest.skip("Not working on multiply till add works")
        def test_our_multiply(self):
            """Our multiply function should work on 3 and 4."""

            self.assertEqual(our_module.multiply(3, 4), 12)

Rerun:

    !console
    $ python -m unittest discover
    Fs
    ======================================================================
    FAIL: test_our_add (test_our_module.TestOurModule)
    Our addition function should work on 2 and 3.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/chen/Dropbox/pghpython/2012-10-24/talk-on-python-mock/test_our_module.py", line 14, in test_our_add
        self.assertEqual(our_module.add(x, y), expected_result)
    AssertionError: 6 != 5

    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    FAILED (failures=1, skipped=1)

---

# Fixing the bug

    !python
    def add(x, y):
        """Return sum of x and y using clever algorithm."""
        return x + y

Rerun:

    !console
    $ python -m unittest discover
    .s
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK (skipped=1)

---

# Repeat process: do `multiply`

- remove `@unittest.skip` decorator from `test_our_multiply`
- rerun test case to fail again
- implement `our_module.multiply`
- rerun test case for complete success

Success!

    !console
    $ python -m unittest discover
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK

---

# What are test doubles?

A *test double* is anything that stands in for a real thing: [terminology by Meszaros, used by Fowler](http://xunitpatterns.com/Test%20Double.html)

# dummy object

- passed around, never used

# test stub

- control indirect inputs of SUT: canned answers

# test spy

- control indirect inputs; *record* to verify indirect outputs of SUT

# mock object

- verify indirect outputs of SUT, by setting up *expectations* (of calls, etc.), then *verifying*

# fake object

- use same interface, but alternate implementation of an object

---

# Introduction to Python `mock`

# Installation

- Python 3.3: part of standard library as `unittest.mock`
- Python 2.7: install with `easy_install` or `pip`

# Terminology

Technically, the `mock` library provides a *test spy* rather than a *mock*!

[Michael Foord, creator of `mock`, on terminology](http://www.voidspace.org.uk/python/mock/#terminology):

> `mock.Mock()` is capable of being used in most of the different roles described by Fowler, except (annoyingly / frustratingly / ironically) a Mock itself!

---

# Basic ideas of `mock`

Create a mock; author says it makes sense to use `MagicMock` in place of original `Mock` since `MagicMock` is more capable:

    !python
    >>> from mock import MagicMock
    >>> m = MagicMock()

Use the mock; actions are recorded internally:

    !python
    >>> result = m(42, "everything")

Make an assertion that fails:

    !python
    >>> m.assert_called_once_with("something", "else")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/local/Cellar/python/2.7.3/lib/python2.7/site-packages/mock.py", line 835, in assert_called_once_with
        return self.assert_called_with(*args, **kwargs)
      File "/usr/local/Cellar/python/2.7.3/lib/python2.7/site-packages/mock.py", line 824, in assert_called_with
        raise AssertionError(msg)
    AssertionError: Expected call: mock('something', 'else')
    Actual call: mock(42, 'everything')

Make an assertion that succeeds (silently):

    >>> m.assert_called_once_with(42, "everything")

---

# More examples of spying

    !python
    >>> from mock import MagicMock
    >>> m = MagicMock()
    >>> # Not called yet
    ... m.called
    False
    >>> # Make three calls
    ... m(2, 3)
    <MagicMock name='mock()' id='4300782544'>
    >>> m(True)
    <MagicMock name='mock()' id='4300782544'>
    >>> m("hello", "world")
    <MagicMock name='mock()' id='4300782544'>
    >>> # Number of calls made
    ... m.call_count
    3
    >>> # Assert whether ever called with (2, 3)?
    ... m.assert_any_call(2, 3)
    >>> # the exact sequence of all calls
    ... m.mock_calls
    [call(2, 3), call(True), call('hello', 'world')]
    >>> # Set return value for the next call
    ... m.return_value = "yes"
    >>> m(52)
    'yes'

---

# Controlled patching

`mock` provides many ways to *patch* out a real object by a fake one.

Especially useful: *context managers* and *decorators*

- limit the scope of patching
- restore everything after exiting scope

---

# Testing behavior without patching

Assume: we have `double` in `our_module`:

    !python
    def double(x):
        """Return double x."""
        return multiply(2, x)

## New requirement from customer: no use of multiplication when doubling!

## How write a test to express this *behavioral* requirement?

Without a mocking framework, tricky.

---

# A terrible solution

- create a **global variable** `multiply_count`, initialized to `0`
- **modify** code for `our_module.multiply` to increment `multiply_count` on each call
- write test to call `double` and then assert on the *state* `multiply_count` being `0`
- uh, undo the source code change

Terrible: temporary change to source code in order to test

# Leave the instrumenting code in there permanently?

- bad performance in production
- global variable interferes with other tests, concurrency

---

# A very principled solution

Must do a lot of *refactoring* just to be able to test!

# Extract code in `our_module` into a class `OurMathClass`

(Note: this is Python 2.7 code)

    !python
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

---

# Must refactor test case accordingly

    !python
    import unittest
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

---

# Subclass `OurMathClass` to spy

Use overriding:

(Note: this is Python 2.7 code)

    !python
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

---

# Replace `OurMathClass` with spy class

    !python
        def setUp(self):
            self.our_module = our_spying_math_class.OurSpyingMathClass()

        def test_our_double_with_multiply(self):
            """Our double function should not work by multiplying."""

            result = self.our_module.double(5)
            self.assertEqual(self.our_module.multiply_call_count, 0)

Test finally runs!

    !console
    $ python -m unittest test_our_spying_math_class
    .F.
    ======================================================================
    FAIL: test_our_double_with_multiply (test_our_spying_math_class.TestOurSpyingMathClass)
    Our double function should not work by multiplying.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_our_spying_math_class.py", line 29, in test_our_double_with_multiply
        self.assertEqual(self.our_module.multiply_call_count, 0)
    AssertionError: 1 != 0

    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s

    FAILED (failures=1)

---

# Summary of principled approach

- much *refactoring* just to be able to test
- subclassing, overriding
- custom *fake object* operating as *test spy*
- very clean

I actually like this principled approach.

# Drawbacks of non-mock approach

- invasive: often requires global redesign
- we may not always be able to modify someone else's code we use

---

# Solution using patching

## We write new test designed to fail, *asserting on behavior*.

Use `patch` decorator: patch existing function in dynamic context.

    !python
    @mock.patch('our_module.multiply')
    def test_our_double_with_multiply(self, fake_multiply):
        """Our double function should not work by multiplying."""

        result = our_module.double(5)
        self.assertEqual(fake_multiply.call_count, 0)

It fails because `fake_multiply.call_count` is in fact `1`.

---

# A better doubling algorithm

The redesigned doubling algorithm:

    !python
    def double(x):
        """Return double x using clever algorithm."""
        return add(x, x)

This passes the test.

Lessons:

- *no need* to change any implementation code in order to test
- a test spy is a very powerful tool!

Drawbacks:

- `mock` does scary monkey patching behind the scenes; be warned, in complex and corner cases

---

# Example: don't want to send email

Want to add to `OurMathClass`: a function `divide` such that dividing `N` by `0` results in sending email to `zerowatcherN@foo.com`

## Start with new test in `test_our_math_class.py`

    !python
    def test_our_divide(self):
        """Dividing by zero should result in email being sent."""

        with mock.patch.object(our_math_class.OurMathClass, 'mail') as mail:
            result = self.our_module.divide(5, 0)
            mail.assert_called_once_with('zerowatcher5@foo.com')

- patch out the method `mail`: avoid sending real email!
- only care about the *behavior* that the mailer was called

---

# Isolation: divide without emailing

Note that our test passes without having yet implemented the mailer.

    !python
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

Used the mock for *isolation*.

---

# Other examples

Other functionality one might want to patch out:

- printing to a display
- outputting to GUI
- receiving input from the network
- accessing a database

---

# Conclusion

- test doubles are a powerful way to isolate tests
- Python `mock` provides flexible test spies
- other possible designs may reduce need for mocks

*Franklin Chen*

[`http://franklinchen.com/`](http://franklinchen.com/)

[`franklinchen@franklinchen.com`](mailto:franklinchen@franklinchen.com)

This slideshow: [`http://franklinchen.com/talk-on-python-mock`](http://franklinchen.com/talk-on-python-mock)