def convert_date(input_date: str) -> str:
    months = [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]
    index = 0
    for index in range(len(months)):
        if months[index] == input_date.split()[1]:
            return f"{input_date.split()[0]} {index + 1}"
