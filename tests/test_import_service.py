"""Tests for the ImportService."""

import pytest
from unittest.mock import Mock
from autoinvo.importers.service import ImportService
from autoinvo.importers.contracts import DataImporter
from autoinvo.importers.models import ImportResult, CsvImportOptions, XlsxImportOptions

def test_import_service_delegates_csv():
    mock_csv = Mock(spec=DataImporter)
    mock_xlsx = Mock(spec=DataImporter)
    
    expected_result = ImportResult(headers=["A"], rows=[{"A": "1"}], row_count=1, source_type="csv")
    mock_csv.parse.return_value = expected_result
    
    service = ImportService(csv_importer=mock_csv, xlsx_importer=mock_xlsx)
    options = CsvImportOptions()
    
    result = service.import_csv("dummy.csv", options)
    
    mock_csv.parse.assert_called_once_with("dummy.csv", options)
    mock_xlsx.parse.assert_not_called()
    assert result == expected_result

def test_import_service_delegates_xlsx():
    mock_csv = Mock(spec=DataImporter)
    mock_xlsx = Mock(spec=DataImporter)
    
    expected_result = ImportResult(headers=["B"], rows=[{"B": "2"}], row_count=1, source_type="xlsx")
    mock_xlsx.parse.return_value = expected_result
    
    service = ImportService(csv_importer=mock_csv, xlsx_importer=mock_xlsx)
    options = XlsxImportOptions()
    
    result = service.import_xlsx("dummy.xlsx", options)
    
    mock_xlsx.parse.assert_called_once_with("dummy.xlsx", options)
    mock_csv.parse.assert_not_called()
    assert result == expected_result
