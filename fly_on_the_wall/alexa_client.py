import json
import requests


class AlexaClient:
    def __init__(self, alexa_notif_bearer):
        self.alexa_notif_bearer = alexa_notif_bearer

    def send_notification(self, message):
        body = json.dumps(
            {"notification": message, "accessCode": self.alexa_notif_bearer}
        )

        requests.post(url="https://api.notifymyecho.com/v1/NotifyMe", data=body)
