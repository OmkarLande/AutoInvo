"""Models for the Data Import Engine."""

from dataclasses import dataclass
from typing import Literal

ImportRow = dict[str, object]

@dataclass(slots=True)
class CsvImportOptions:
    """Options for configuring CSV imports."""
    delimiter: str = ","
    encoding: str = "utf-8"
    quotechar: str = '"'

@dataclass(slots=True)
class XlsxImportOptions:
    """Options for configuring Excel (XLSX) imports."""
    sheet_index: int = 0
    sheet_name: str | None = None

@dataclass(slots=True, frozen=True)
class ImportResult:
    """Represents the standardized output of a data import operation."""
    headers: list[str]
    rows: list[ImportRow]
    row_count: int
    source_type: Literal["csv", "xlsx"]
