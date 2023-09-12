def Format_note_name(input_text: str) -> str:
    return input_text[:20] + "..." if len(input_text) > 20 else input_text


def Format_reminder(input_text: str, date: str, reminders_type: str) -> str:
    text = ""
    if len(input_text) > 5:
        text = input_text[:5] + "..."
    else:
        text = input_text

    if reminders_type == "Каждый день":
        return f"{text.ljust(10)}{reminders_type} в {date}"
    elif reminders_type == "День недели":
        return f"{text.ljust(10)}Каждый(-ую) {date.lower()}"
    else:
        return f"{text.ljust(10)}{reminders_type} {date}"
