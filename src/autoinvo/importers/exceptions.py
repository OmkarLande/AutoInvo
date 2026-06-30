"""Exceptions for the Data Import Engine."""

class ImportError(Exception):
    """Exception raised for errors during the data import process."""
    
    def __init__(self, message: str, original_exception: Exception | None = None) -> None:
        """Initializes the ImportError.
        
        Args:
            message: Meaningful error message explaining the failure.
            original_exception: The underlying exception that caused this error, if any.
        """
        super().__init__(message)
        self.original_exception = original_exception
