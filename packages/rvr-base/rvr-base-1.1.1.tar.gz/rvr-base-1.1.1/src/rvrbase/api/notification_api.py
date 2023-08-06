from notify_run import Notify


class New_notification_api:
    def __init__(self):
        super().__init__()
        self.notify = Notify()

    def send_browser_notification(self, message):
        self.notify.send(message)
