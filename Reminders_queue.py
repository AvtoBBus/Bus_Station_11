from datetime import datetime
import Convert_date_time


class Reminders_queue():
    reminders_queue = []
    ed_queue = []
    ew_queue = []
    ey_queue = []
    once_queue = []

    def __init__(self, input_list: list[list[str, str]]):
        index = 0
        for elem in input_list:
            dif = 0
            if elem[0] == "Каждый день":
                dif = self.calc_every_day(elem[1])
            elif elem[0] == "День недели":
                dif = self.calc_every_week(elem[1])
            elif elem[0] == "Один день в год":
                dif = self.calc_every_year(elem[1])
            else:
                dif = self.calc_once(elem[1])
            self.reminders_queue.append([index, elem[0], dif])
            index += 1
        self.sort_reminders_queue()

    def calc_every_day(self, time: str) -> int:
        current_time = datetime.now().time()
        cur_minute = int(str(current_time).split(
            ":")[1]) + (int(str(current_time).split(":")[0]) * 60)
        reminder_minute = int(time.split(
            ":")[1]) + (int(time.split(":")[0]) * 60)
        dif = reminder_minute - cur_minute
        if dif >= 0:
            return dif
        return 24 * 60 - cur_minute + reminder_minute

    def calc_every_week(self, day_in_week: str) -> int:
        week = ["Понедельник", "Вторник", "Среда",
                "Четверг", "Пятница", "Суббота", "Воскресенье"]
        cur_day = datetime.now().isoweekday()
        reminder_day = 0
        for i in range(7):
            if week[i] == day_in_week:
                reminder_day = i + 1
                break
        return 7 - cur_day + reminder_day if reminder_day < cur_day else reminder_day - cur_day

    def calc_every_year(self, day_in_year: str) -> int:
        day = Convert_date_time.convert_date(day_in_year)
        cur_date = datetime.now().isoformat().split("T")[0]
        reminder_date = f"{cur_date.split('-')[0]}-{day.split()[1]}-{day.split()[0]}"

        help = cur_date.split('-')
        cur_date = ""
        for elem in help[::-1]:
            cur_date += elem + "."

        help = reminder_date.split('-')
        reminder_date = ""
        for elem in help[::-1]:
            reminder_date += elem + "."

        zero_date = datetime.strptime(
            f"01.01.{datetime.now().year}", "%d.%m.%Y")
        final_date = datetime.strptime(
            f"31.12.{datetime.now().year}", "%d.%m.%Y")

        cur_date_zero = datetime.strptime(cur_date[:-1], "%d.%m.%Y")
        rem_date_zero = datetime.strptime(reminder_date[:-1], "%d.%m.%Y")
        if (rem_date_zero - zero_date).days < (cur_date_zero - zero_date).days:
            return (final_date - cur_date_zero).days + rem_date_zero.day
        return (rem_date_zero - cur_date_zero).days

    def calc_once(self, day: str) -> int:
        cur_date = datetime.now().isoformat().split("T")[0]

        help = cur_date.split('-')
        cur_date = ""
        for elem in help[::-1]:
            cur_date += elem + "."

        cur_date_new = datetime.strptime(cur_date[:-1], "%d.%m.%Y")
        rem_date_new = datetime.strptime(day, "%d.%m.%Y")
        return (rem_date_new - cur_date_new).days

    def sort_reminders_queue(self) -> None:
        for elem in self.reminders_queue:
            if elem[1] == "Каждый день":
                self.ed_queue.append(elem)
            elif elem[1] == "День недели":
                self.ew_queue.append(elem)
            elif elem[1] == "Один день в год":
                self.ey_queue.append(elem)
            else:
                self.once_queue.append(elem)
        self.ed_queue.sort(key=lambda x: x[2])
        self.ew_queue.sort(key=lambda x: x[2])
        self.ey_queue.sort(key=lambda x: x[2])
        self.once_queue.sort(key=lambda x: x[2])

    def get_first_every_day(self) -> list[int, str, int]:
        return self.ed_queue[0] if len(self.ed_queue) != 0 else None

    def get_first_every_week(self) -> list[int, str, int]:
        return self.ew_queue[0] if len(self.ew_queue) != 0 else None

    def get_first_every_year(self) -> list[int, str, int]:
        return self.ey_queue[0] if len(self.ey_queue) != 0 else None

    def get_first_once(self) -> list[int, str, int]:
        return self.once_queue[0] if len(self.once_queue) != 0 else None

    def clear_queue(self) -> None:
        self.reminders_queue.clear()
        self.ed_queue.clear()
        self.ew_queue.clear()
        self.ey_queue.clear()
        self.once_queue.clear()


if __name__ == "__main__":
    r = Reminders_queue([["Один день в год", "14 Июль"]])
    print(r.get_first_every_year())
