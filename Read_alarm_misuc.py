import os


def read_alarm_music(file_paht: str) -> list[str]:
    result = []
    for elem in os.listdir(file_paht):
        result.append(elem.split(".")[0])
    return result
