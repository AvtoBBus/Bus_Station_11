import csv
import pandas as pd
from datetime import datetime

DB_PATH = "data_bases/notes_data_base/notes_data.csv"

def Add_to_data_base(notes_text: str) -> None:
    current_datetime = datetime.now()
    with open(DB_PATH, 'a', encoding="utf-8", newline="") as db_file:
        writerer = csv.writer(db_file, delimiter=';')
        writerer.writerow([notes_text,
                           current_datetime.date(),
                           current_datetime.time()]
                           )

def Read_full() -> list[str]:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8", index_col=False)
    result_list = []
    for i in range(int(db_file.shape[0])):
        result_list.append(str(db_file["Notes_text"][i]))
    return result_list

def Read_text_index(index: int) -> str:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8", index_col=False)
    return str(db_file["Notes_text"][index])

def Edit_text_index(index: int, new_text: str) -> None:
    current_datetime = datetime.now()
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    db_file.at[index, "Notes_text"] = new_text
    db_file.at[index, "Create_date"] = current_datetime.date()
    db_file.at[index, "Create_time"] = current_datetime.time()
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)

def Delete_index(index: int) -> None:
    db_file = pd.read_csv(DB_PATH, delimiter=";", encoding="utf-8")
    db_file.drop(labels=index, axis=0,inplace=True)
    Clear_data_base()
    db_file.to_csv(DB_PATH, sep=';', index=False)

def Clear_data_base() -> None:
    with open(DB_PATH, "w", encoding="utf-8",newline="") as file:
        writerer = csv.writer(file, delimiter=";")
        writerer.writerow(["Notes_text","Create_date","Create_time"])

# if __name__ == "__main__":
#     Add_to_data_base("a")
#     Add_to_data_base("b")
#     Add_to_data_base("c")
#     Add_to_data_base("d")
#     Add_to_data_base("e")
    # print(Read_full())
    # print(Read_text_index(2))
    # Edit_text_index(2, "haha")
    # print(Read_text_index(2))
    # print(Read_full())
    # Delete_index(3)
    # print(Read_full())
    # Clear_data_base()