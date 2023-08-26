import csv
import pandas as pd
from datetime import datetime

DB_PATH = "data_bases/alarm_data_base/alarm_data.csv"


def Add_to_data_base(time: str, music: str, activated: int = 1) -> None:
    with open(DB_PATH, 'a', encoding="utf-8", newline="") as db_file:
        writerer = csv.writer(db_file, delimiter=';')
        writerer.writerow([time,
                           music,
                           activated]
                          )
    sort_data_base()


def sort_data_base() -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    db_file.sort_values("Alarm_time", inplace=True)
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)


def Read_full() -> list[list[str, str, int]]:
    sort_data_base()
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    result_list = []
    for i in range(int(db_file.shape[0])):
        result_list.append([str(db_file["Alarm_time"][i]),
                            str(db_file["Music"][i]),
                            int(db_file["Activated"][i])]
                           )
    return result_list


def Read_time_index(index: int) -> str:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return str(db_file["Alarm_time"][index])


def Read_music_index(index: int) -> str:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return str(db_file["Music"][index])


def Check_activated(index: int) -> bool:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return bool(db_file["Activated"][index])


def Edit_alarm_index(index: int, new_time: str, new_music: str) -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    db_file.at[index, "Alarm_time"] = new_time
    db_file.at[index, "Music"] = new_music
    db_file.at[index, "Activated"] = db_file["Activated"][index]
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)


def Delete_index(index: int) -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    db_file.drop(labels=index, axis=0, inplace=True)
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)


def Activate_alarm(index: int) -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    if db_file["Activated"][index] == 0:
        db_file.at[index, "Activated"] = 1
    else:
        db_file.at[index, "Activated"] = 0
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)


def Clear_data_base() -> None:
    with open(DB_PATH, "w", encoding="utf-8", newline="") as file:
        writerer = csv.writer(file, delimiter=";")
        writerer.writerow(["Alarm_time", "Music", "Activated"])


def Read_full_time() -> list[str]:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return db_file['Alarm_time'].to_list()


# if __name__ == "__main__":
#     Clear_data_base()
#     Add_to_data_base("a", "a", 0)
#     Add_to_data_base("b", "b")
#     Add_to_data_base("c", "c")
#     Add_to_data_base("d", "d")
#     print(Read_full())
#     print(Check_activated(0))
#     print(Check_activated(1))
#     Activate_alarm(1)
#     print(Check_activated(1))
#     Clear_data_base()
