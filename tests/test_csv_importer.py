"""Tests for the CsvImporter."""

import io
import pytest
from pathlib import Path

from autoinvo.importers.csv_importer import CsvImporter
from autoinvo.importers.models import CsvImportOptions
from autoinvo.importers.exceptions import ImportError

@pytest.fixture
def importer() -> CsvImporter:
    return CsvImporter()

def test_valid_csv(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("Name,Age\nAlice,30\nBob,25\n", encoding="utf-8")
    
    result = importer.parse(csv_file)
    assert result.headers == ["Name", "Age"]
    assert result.row_count == 2
    assert result.rows[0] == {"Name": "Alice", "Age": "30"}
    
def test_utf8_bom(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "bom.csv"
    csv_file.write_bytes(b"\xef\xbb\xbfName,Age\nAlice,30\n")
    
    result = importer.parse(csv_file)
    assert result.headers == ["Name", "Age"]
    assert result.row_count == 1
    
def test_crlf(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "crlf.csv"
    csv_file.write_bytes(b"Name,Age\r\nAlice,30\r\n")
    
    result = importer.parse(csv_file)
    assert result.headers == ["Name", "Age"]
    assert result.row_count == 1

def test_unicode_content(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "unicode.csv"
    csv_file.write_text("Name,Greeting\nこんにちは, नमस्ते 🎉\n", encoding="utf-8")
    
    result = importer.parse(csv_file)
    assert result.headers == ["Name", "Greeting"]
    assert result.rows[0] == {"Name": "こんにちは", "Greeting": "नमस्ते 🎉"}
    
def test_quoted_values_and_commas(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "quotes.csv"
    csv_file.write_text('Name,"Location, City"\nAlice,"Paris, France"\n', encoding="utf-8")
    
    result = importer.parse(csv_file)
    assert result.headers == ["Name", "Location, City"]
    assert result.rows[0]["Location, City"] == "Paris, France"

def test_custom_delimiter(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "custom.csv"
    csv_file.write_text("Name|Age\nAlice|30\n", encoding="utf-8")
    
    options = CsvImportOptions(delimiter="|")
    result = importer.parse(csv_file, options)
    assert result.headers == ["Name", "Age"]
    
def test_duplicate_headers(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "dup.csv"
    csv_file.write_text("Name,Name\nAlice,Bob\n", encoding="utf-8")
    
    with pytest.raises(ImportError, match="duplicate"):
        importer.parse(csv_file)
        
def test_empty_headers(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "empty_head.csv"
    csv_file.write_text(",Age\nAlice,30\n", encoding="utf-8")
    
    with pytest.raises(ImportError, match="empty headers"):
        importer.parse(csv_file)
        
def test_blank_rows(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "blank.csv"
    csv_file.write_text("Name,Age\n\nAlice,30\n   \n\nBob,25\n", encoding="utf-8")
    
    result = importer.parse(csv_file)
    assert result.row_count == 2
    assert result.rows[0]["Name"] == "Alice"
    assert result.rows[1]["Name"] == "Bob"

def test_missing_file(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "missing.csv"
    with pytest.raises(ImportError, match="File not found"):
        importer.parse(csv_file)

def test_empty_file(importer: CsvImporter, tmp_path: Path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    with pytest.raises(ImportError, match="empty"):
        importer.parse(csv_file)
        
def test_invalid_path(importer: CsvImporter):
    with pytest.raises(ImportError):
        importer.parse("")

def test_bytes_input(importer: CsvImporter):
    data = b"Name,Age\nAlice,30\n"
    result = importer.parse(data)
    assert result.row_count == 1
    
def test_binary_io_input(importer: CsvImporter):
    data = io.BytesIO(b"Name,Age\nAlice,30\n")
    result = importer.parse(data)
    assert result.row_count == 1
    
def test_performance():
    importer = CsvImporter()
    data = ["Name,Age"]
    for i in range(10000):
        data.append(f"Person {i},{i}")
    
    csv_text = "\n".join(data) + "\n"
    csv_bytes = csv_text.encode("utf-8")
    
    result = importer.parse(csv_bytes)
    assert result.row_count == 10000
