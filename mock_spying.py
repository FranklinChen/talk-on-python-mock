from mock import MagicMock
m = MagicMock()
# Not called yet
m.called
# Make three calls
m(2, 3)
m(True)
m("hello", "world")
# Number of calls made
m.call_count
# Assert whether ever called with (2, 3)?
m.assert_any_call(2, 3)
# the exact sequence of all calls
m.mock_calls
# Set return value for the next call
m.return_value = "yes"
m(52)
