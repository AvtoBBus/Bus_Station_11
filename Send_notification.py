import win10toast
import schedule
import time


def every_day_send(notification_text: str) -> None:
    print("here")
    # time.sleep(59)
    toast = win10toast.ToastNotifier()
    toast.show_toast(
        title="НАПОМИНАНИЕ", msg=notification_text, duration=60)
