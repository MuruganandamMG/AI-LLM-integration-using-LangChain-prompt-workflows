from app.schemas.habit_schedule import HabitSchedule, TimeOfDaySlot

def test_default_habit_schedule():
    sched = HabitSchedule()
    assert sched.time_slot == TimeOfDaySlot.ANYTIME
    assert sched.reminder_time == "09:00"

def test_custom_habit_schedule():
    sched = HabitSchedule(time_slot=TimeOfDaySlot.MORNING, reminder_time="07:30")
    assert sched.time_slot == "morning"
    assert sched.reminder_time == "07:30"
