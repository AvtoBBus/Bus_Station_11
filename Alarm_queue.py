from datetime import datetime


class Alarm_queue():
    alarm_queue = []

    def __init__(self, alarm_list: list[str]):
        index = 0
        for elem in alarm_list:
            self.alarm_queue.append([index, self.calc_time(elem)])
            index += 1
        self.alarm_queue.sort(key=lambda x: x[1])

    def calc_time(self, time: str) -> int:
        current_time = datetime.now().time()
        cur_minute = int(str(current_time).split(
            ":")[1]) + (int(str(current_time).split(":")[0]) * 60)
        alarm_minute = int(time.split(
            ":")[1]) + (int(time.split(":")[0]) * 60)
        dif = alarm_minute - cur_minute
        if dif > 0:
            return dif
        return 24 * 60 - cur_minute + alarm_minute

    def get_first_in_queue(self) -> list[int, int]:
        return self.alarm_queue[0]

    def clear_queue(self) -> None:
        self.alarm_queue.clear()

# aq = Alarm_queue(["10:00", "13:00", "15:00"])
