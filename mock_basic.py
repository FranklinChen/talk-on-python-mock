from mock import MagicMock
m = MagicMock()
result = m(42, "everything")
# Fails
m.assert_called_once_with("something", "else")
m.assert_called_once_with(42, "everything")
