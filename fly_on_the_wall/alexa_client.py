import json
import requests


NOTIFY_URL = "https://api.notifymyecho.com/v1/NotifyMe"


class AlexaClient:
    def __init__(self, alexa_notif_bearer):
        self.alexa_notif_bearer = alexa_notif_bearer

    def send_notification(self, message):
        body = json.dumps(
            {"notification": message, "accessCode": self.alexa_notif_bearer}
        )

        requests.post(url=NOTIFY_URL, data=body)
