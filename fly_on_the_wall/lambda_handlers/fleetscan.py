from fly_on_the_wall.customer import all_customers
from fly_on_the_wall.equity_client import EquityClient


def scan(event, _):
    for item in all_customers():
        customer_id = item["customer_id"]
        alexa_notif_bearer = item["alexa_notif_bearer"]
        portfolio = item.get("portfolio")

        if not portfolio:
            continue

        print(f"Processing Customer: {customer_id}")

        for stock in portfolio:
            equity_client = EquityClient(ticker=stock)
            delta = equity_client.get_delta()
            print(f"Stock: {stock}, delta: {delta}")


def _push_to_alerting_queue():
    pass
