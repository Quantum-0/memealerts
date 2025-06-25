class MAError(Exception):
    """Memealerts error"""
    pass

class MATokenExpired(MAError):
    """Token is already expired."""
    pass