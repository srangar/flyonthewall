import os
import json
import uuid
from fly_on_the_wall.customer import Customer
from fly_on_the_wall.message_broker import MessageBroker
from fly_on_the_wall.equity_client import EquityClient


def create_customer(event, _):
    alexa_notif_bearer = event["alexa_bearer_token"]
    customer_id = str(uuid.uuid4())
    customer = Customer(customer_id=customer_id, alexa_notif_bearer=alexa_notif_bearer)
    customer.save(create=True)

    return {"statusCode": 201}


def get_customer(event, _):
    try:
        customer_id = event["customer_id"]
        customer = Customer.load(customer_id=customer_id)

        return {"statusCode": 200, "body": json.dumps(customer.to_json())}
    except exceptions.UserLoadError as err:
        print(f"Unable to Load Customer: {customer_id}")
        return {"statusCode": 404}


def process_customer(event, _):
    print(f"Event Received: {event}")

    record = event["Records"][0]
    message = json.loads(record["body"])["message"]
    customer_id = message["customer_id"]
    portfolio = message.get("portfolio")
    alerts = []

    for stock in portfolio:
        equity_client = EquityClient(ticker=stock)
        delta = equity_client.get_delta()
        print(f"Stock: {stock}, delta: {delta}")

        # If there is 1% change or more in the equity...
        if delta > 0:
            alerts.append(stock)

    print(f"Customer ID: {customer_id}, Alerts: {alerts}")

    if alerts:
        notification = "Please Check Following Stocks: " + ", ".join(alerts)
        message = {"customer_id": customer_id, "notification": notification}
        message_broker = MessageBroker(queue_name=os.environ["ALERTING_QUEUE"])
        message_broker.enqueue(message=message)


def update_customer(event, _):
    try:
        new_portfolio = event["portfolio"]
        customer_id = event["customer_id"]
        customer = Custamer.load(customer_id=customer_id)
        customer.portfolio = new_portfolio
        customer.save()

        return {"statusCode": 200}
    except KeyError as err:
        print(f"KeryError: {err}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "new_portfolio required in event"}),
        }
