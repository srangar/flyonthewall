from fly_on_the_wall.customer import all_customers
from fly_on_the_wall.equity_client import EquityClient
from fly_on_the_wall.message_broker import MessageBroker


def scan(event, _):
    try:
        for customer in all_customers():
            print(f"Customer scanned: {customer}")

            customer_id = customer["customer_id"]
            portfolio = customer.get("portfolio")

            if not portfolio:
                continue

            message = {"customer_id": customer_id, "portfolio": portfolio}
            message_broker = MessageBroker(queue_name=os.environ["PROCESSING_QUEUE"])
            message_broker.enqueue(message=message)
    except Exception as err:
        print(f"Encountered Excption: {err}, skipping")
        continue
