from app.services.ics_export_service import ICSExportService

def test_generate_ics():
    ics = ICSExportService.generate_ics("Meditation", "Mindfulness", "08:00")
    assert "BEGIN:VCALENDAR" in ics
    assert "SUMMARY:Meditation" in ics
    assert "END:VCALENDAR" in ics
