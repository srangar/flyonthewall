import json
import uuid
from fly_on_the_wall.customer import Customer


def create_customer(event, _):
    alexa_notif_bearer = event["alexa_bearer_token"]
    customer_id = str(uuid.uuid4())
    customer = Custamer(customer_id=customer_id, alexa_notif_bearer=alexa_notif_bearer)
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
