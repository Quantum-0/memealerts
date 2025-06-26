class MAError(Exception):
    """Memealerts error"""

class MATokenExpired(MAError):
    """Token is already expired."""
