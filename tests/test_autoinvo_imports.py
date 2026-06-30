"""Integration tests for AutoInvo importer facade methods."""

import pytest
from autoinvo.core.autoinvo import AutoInvo
import openpyxl

def test_autoinvo_import_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Name\nAlice\n", encoding="utf-8")
    
    autoinvo = AutoInvo()
    result = autoinvo.import_csv(csv_file)
    
    assert result.headers == ["Name"]
    assert result.rows[0]["Name"] == "Alice"
    assert result.source_type == "csv"

def test_autoinvo_import_xlsx(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Name"])
    ws.append(["Bob"])
    path = tmp_path / "test.xlsx"
    wb.save(path)
    
    autoinvo = AutoInvo()
    result = autoinvo.import_xlsx(path)
    
    assert result.headers == ["Name"]
    assert result.rows[0]["Name"] == "Bob"
    assert result.source_type == "xlsx"
