class MAError(Exception):
    """Memealerts error"""


class MATokenExpiredError(MAError):
    """Token is already expired."""
