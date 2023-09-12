import csv
import pandas as pd
from datetime import datetime

DB_PATH = "data_bases/reminders_data_base/reminders_data.csv"


def Add_to_data_base(Reminder_text: str, Creature_date: str, reminders_type: int, activated: int = 1) -> None:
    with open(DB_PATH, 'a', encoding="utf-8", newline="") as db_file:
        writerer = csv.writer(db_file, delimiter=';')
        writerer.writerow([Reminder_text, Creature_date,
                          activated, reminders_type])


def Read_full() -> list[list[str, str, int, str]]:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    result_list = []
    for i in range(int(db_file.shape[0])):
        result_list.append([str(db_file["Reminder_text"][i]),
                            str(db_file["Creature_date"][i]),
                            int(db_file["Activated"][i]),
                            str(db_file["Reminders_type"][i])]
                           )
    return result_list


def Read_full_date() -> list[str]:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return db_file['Creature_date'].to_list()


def Read_text_index(index: int) -> str:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return str(db_file["Reminder_text"][index])


def Read_date_index(index: int) -> list[str]:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return str(db_file["Creature_date"][index]).split(".")


def Read_type_index(index: int) -> str:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return str(db_file["Reminders_type"][index])


def Check_activated(index: int) -> bool:
    db_file = pd.read_csv(DB_PATH, delimiter=";",
                          encoding="utf-8", index_col=False)
    return bool(db_file["Activated"][index])


def Edit_reminder_index(index: int, new_text: str, new_date: str, new_type: str) -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    db_file.at[index, "Reminder_text"] = new_text
    db_file.at[index, "Creature_date"] = new_date
    db_file.at[index, "Reminders_type"] = new_type
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)


def Delete_index(index: int) -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    db_file.drop(labels=index, axis=0, inplace=True)
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)


def Activate_remind(index: int) -> None:
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
        writerer.writerow(["Reminder_text", "Creature_date",
                          "Activated", "Reminders_type"])


# if __name__ == "__main__":
#     Clear_data_base()
#     Add_to_data_base("a", "a", 0)
#     Add_to_data_base("b", "b")
#     Add_to_data_base("c", "c")
#     Add_to_data_base("d", "d")
#     print(Read_full())
#     print(Check_activated(0))
#     print(Check_activated(1))
#     Activate_remind(1)
#     print(Check_activated(1))
#     Edit_reminder_index(0, "aaaa", "aaaaaaa")
#     print(Read_full())
#     Clear_data_base()
