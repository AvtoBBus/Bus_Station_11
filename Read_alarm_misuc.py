import os


def read_alarm_music(file_paht: str) -> list[str]:
    return os.listdir(file_paht)
