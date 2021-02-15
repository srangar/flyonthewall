import json

from fly_on_the_wall.alexa_client import AlexaClient
from fly_on_the_wall.customer import Customer
from fly_on_the_wall import exceptions


def send_alexa_notifs(event, _):
    print(f"Event Received: {event}")
    try:
        record = event["Records"][0]
        message = json.loads(record["body"])["message"]
        customer_id = message["customer_id"]
        notification = message["notification"]

        customer = Customer.load(customer_id=customer_id)
        alexa_client = AlexaClient(alexa_notif_bearer=customer.alexa_notif_bearer)
        alexa_client.send_notification(message=notification)

        return True
    except KeyError as err:
        print(f"KeyError: {err}")
        raise exceptions.MissingParametersError(
            "customer_id and message are required in event"
        )
