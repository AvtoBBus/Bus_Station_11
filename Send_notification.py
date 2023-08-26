import win10toast
import schedule


def send_alarm(time: str):
    toast = win10toast.ToastNotifier()
    toast.show_toast(
        title="БУДИЛЬНИК", msg=time, duration=5)
