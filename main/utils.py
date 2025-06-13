from datetime import  timedelta




def generate_time_slots(start_time, end_time, slot_duration=25, break_duration=5):
    """
    Generate time slots between start_time and end_time with a specified duration
    and optional breaks between slots.
    """
    slots = []
    current_time = start_time
    while current_time + timedelta(minutes=slot_duration) <= end_time:
        slot_start = current_time
        slot_end = current_time + timedelta(minutes=slot_duration)
        slots.append((slot_start, slot_end))
        current_time = slot_end + timedelta(minutes=break_duration)  # Add break duration
    return slots