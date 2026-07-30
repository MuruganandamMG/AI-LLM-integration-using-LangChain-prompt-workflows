class ICSExportService:
    @staticmethod
    def generate_ics(habit_title: str, category: str, reminder_time: str = "09:00") -> str:
        time_clean = reminder_time.replace(":", "") + "00"
        return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AI Self-Improvement Platform//EN
BEGIN:VEVENT
SUMMARY:{habit_title}
DESCRIPTION:Habit category: {category}
RRULE:FREQ=DAILY
DTSTART;TZID=UTC:20260101T{time_clean}
END:VEVENT
END:VCALENDAR"""
