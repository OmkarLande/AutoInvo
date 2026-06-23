"""Custom exceptions for the autoinvo PDF module."""

class PdfGenerationError(Exception):
    """Custom exception raised when PDF generation fails.

    This exception allows wrapping an underlying original exception for debugging purposes,
    while hiding the implementation details of specific engines (e.g. WeasyPrint, wkhtmltopdf)
    from package consumers.
    """

    def __init__(self, message: str, original_exception: Exception | None = None) -> None:
        """Initializes the exception with a message and an optional original exception.

        Args:
            message: Descriptive error message explaining the failure.
            original_exception: The underlying exception that caused this error, if any.
        """
        super().__init__(message)
        self.original_exception = original_exception
