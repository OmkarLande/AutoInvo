"""Service layer for the Data Import Engine."""

from autoinvo.importers.contracts import DataImporter, ImportSource
from autoinvo.importers.csv_importer import CsvImporter
from autoinvo.importers.xlsx_importer import XlsxImporter
from autoinvo.importers.models import ImportResult, CsvImportOptions, XlsxImportOptions

class ImportService:
    """Service layer for handling data imports.
    
    Validates inputs, normalizes source types, and delegates to the appropriate DataImporter.
    """
    
    def __init__(
        self,
        csv_importer: DataImporter | None = None,
        xlsx_importer: DataImporter | None = None
    ) -> None:
        """Initializes the ImportService.
        
        Args:
            csv_importer: Optional custom DataImporter for CSV files. Defaults to CsvImporter.
            xlsx_importer: Optional custom DataImporter for XLSX files. Defaults to XlsxImporter.
        """
        self._csv_importer = csv_importer or CsvImporter()
        self._xlsx_importer = xlsx_importer or XlsxImporter()

    def import_csv(self, source: ImportSource, options: CsvImportOptions | None = None) -> ImportResult:
        """Imports data from a CSV source.
        
        Args:
            source: The input data source.
            options: Configuration options for CSV import.
            
        Returns:
            An ImportResult containing the parsed headers and rows.
            
        Raises:
            ImportError: If parsing fails or input is invalid.
        """
        return self._csv_importer.parse(source, options)

    def import_xlsx(self, source: ImportSource, options: XlsxImportOptions | None = None) -> ImportResult:
        """Imports data from an XLSX source.
        
        Args:
            source: The input data source.
            options: Configuration options for XLSX import.
            
        Returns:
            An ImportResult containing the parsed headers and rows.
            
        Raises:
            ImportError: If parsing fails or input is invalid.
        """
        return self._xlsx_importer.parse(source, options)
