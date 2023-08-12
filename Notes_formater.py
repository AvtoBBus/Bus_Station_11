def Format_note_text(input_text: str) -> str:
    return input_text[:20] + "..." if len(input_text) > 20 else input_text