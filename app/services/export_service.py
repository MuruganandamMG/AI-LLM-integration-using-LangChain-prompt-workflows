import csv
import io
from app.models.habit import Habit

class ExportService:
    @staticmethod
    def export_habits_csv(habits: list[Habit]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Title", "Category", "Frequency", "Total Logs"])
        for h in habits:
            writer.writerow([h.id, h.title, h.category, h.frequency, len(h.logs)])
        return output.getvalue()
