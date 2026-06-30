"""CSV Importer for the Data Import Engine."""

import csv
import io
from pathlib import Path
from typing import BinaryIO

from autoinvo.importers.contracts import DataImporter, ImportSource
from autoinvo.importers.models import ImportResult, CsvImportOptions
from autoinvo.importers.exceptions import ImportError

class CsvImporter(DataImporter):
    """Importer for CSV data."""

    def parse(self, source: ImportSource, options: CsvImportOptions | None = None) -> ImportResult:
        """Parses a CSV source into an ImportResult.
        
        Args:
            source: The CSV input data source.
            options: Configuration options for CSV import.
            
        Returns:
            An ImportResult containing headers and rows.
            
        Raises:
            ImportError: If parsing fails or input is invalid.
        """
        if options is None:
            options = CsvImportOptions()

        if source is None:
            raise ImportError("Source cannot be None")

        file_obj = None
        should_close = False
        text_io = None

        try:
            if isinstance(source, (str, Path)):
                path = Path(source)
                if str(path).strip() == "":
                    raise ImportError("Source path cannot be empty")
                if not path.is_file():
                    raise ImportError(f"File not found: {path}")
                file_obj = path.open('rb')
                should_close = True
            elif isinstance(source, bytes):
                if not source:
                    raise ImportError("Source bytes cannot be empty")
                file_obj = io.BytesIO(source)
                should_close = True
            elif hasattr(source, "read"):
                # BinaryIO
                file_obj = source
                should_close = False
            else:
                raise ImportError(f"Unsupported source type: {type(source)}")
            
            # Use utf-8-sig to automatically handle UTF-8 BOM if present
            encoding = "utf-8-sig" if options.encoding.lower() in ("utf-8", "utf8") else options.encoding
            
            text_io = io.TextIOWrapper(file_obj, encoding=encoding, newline='')
            
            reader = csv.reader(
                text_io,
                delimiter=options.delimiter,
                quotechar=options.quotechar
            )

            try:
                raw_headers = next(reader)
            except StopIteration:
                raise ImportError("CSV is empty")
            except Exception as e:
                raise ImportError(f"Failed to read CSV: {e}", original_exception=e)
                
            if not raw_headers:
                raise ImportError("CSV contains empty headers")
                
            # Normalize headers
            headers = []
            for h in raw_headers:
                h_stripped = h.strip() if h else ""
                if not h_stripped:
                    raise ImportError("CSV contains empty headers")
                headers.append(h_stripped)
            
            if len(headers) != len(set(headers)):
                raise ImportError("CSV contains duplicate headers")
                
            rows = []
            for row in reader:
                # Skip blank rows (empty list or list of all empty strings)
                if not row or all(not str(cell).strip() for cell in row):
                    continue
                
                # Zip headers and row, fill missing with empty string
                row_dict = {}
                for i, h in enumerate(headers):
                    val = str(row[i]).strip() if i < len(row) else ""
                    row_dict[h] = val
                rows.append(row_dict)
                
            return ImportResult(
                headers=headers,
                rows=rows,
                row_count=len(rows),
                source_type="csv"
            )
            
        except ImportError:
            raise
        except UnicodeDecodeError as e:
            raise ImportError(f"Failed to decode CSV with encoding {options.encoding}: {e}", original_exception=e)
        except Exception as e:
            raise ImportError(f"Error parsing CSV: {e}", original_exception=e)
        finally:
            if text_io:
                text_io.detach()
            if should_close and file_obj:
                file_obj.close()
