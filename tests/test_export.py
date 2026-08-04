from app.services.export_service import ExportService

def test_empty_export():
    csv_data = ExportService.export_habits_csv([])
    assert "Title,Category,Frequency,Total Logs" in csv_data
