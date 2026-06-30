"""Contracts for the Data Import Engine."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

from autoinvo.importers.models import ImportResult

# Type alias for supported source types
ImportSource = Path | str | bytes | BinaryIO

class DataImporter(ABC):
    """Abstract base class defining the contract for all data importers."""

    @abstractmethod
    def parse(self, source: ImportSource, options: any = None) -> ImportResult:
        """Parses the given source into an ImportResult.

        Args:
            source: The input data source. Can be a Path object, file path string,
                bytes, or a file-like BinaryIO object.
            options: Configuration options specific to the importer implementation.

        Returns:
            An ImportResult containing the standardized parsed data.
            
        Raises:
            ImportError: If parsing fails, validation fails, or input is invalid.
        """
        ...
