import os
import uuid
import boto3
from typing import Iterable
import botocore.exceptions

from fly_on_the_wall import exceptions


def all_customers() -> Iterable[dict]:
    table = Customer.table()
    last_evaluated_key = None
    kwargs = {}

    while True:
        if last_evaluated_key:
            kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.scan()

        for item in response.get("Items", []):
            yield item

        last_evaluated_key = response.get("LastEvaluatedKey")

        if not last_evaluated_key:
            break


class Customer:
    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        customer_id: str,
        alexa_notif_bearer: str,
        portfolio: list,
        risk_tolerance: str,
    ):
        self.customer_id = customer_id
        self.alexa_notif_bearer = alexa_notif_bearer
        self.portfolio = portfolio
        self.risk_tolerance = risk_tolerance

    @staticmethod
    def table():
        dynamodb = boto3.resource("dynamodb")
        return dynamodb.Table(os.environ["USER_TABLE"])

    @classmethod
    def load(cls, customer_id: str):
        try:
            response = cls.table().get_item(Key={"customer_id": customer_id})

            item = response["Item"]

            return cls(
                customer_id=item["customer_id"],
                alexa_notif_bearer=item["alexa_notif_bearer"],
                portfolio=item["portfolio"],
                risk_tolerance=item["risk_tolerance"],
            )
        except KeyError as err:
            raise exceptions.UserLoadError(f"customer id: {customer_id}") from err

    def save(self, create=False):
        try:
            item = {
                "customer_id": self.customer_id,
                "alexa_notif_bearer": self.alexa_notif_bearer,
                "portfolio": self.portfolio,
                "risk_tolerance": self.risk_tolerance,
            }

            if create:
                self.table().put_item(
                    Item=item,
                    ConditionExpression="attribute_not_exists(customer_id)",
                )
            else:
                self.table().put_item(Item=item)
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise

            raise exceptions.UserCreationError(f"customer id: {customer_id}") from err

    def delete(self):
        self.table().delete_item(
            Key={
                "customer_id": self.customer_id,
            }
        )

    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "alexa_notif_bearer": self.alexa_notif_bearer,
            "portfolio": self.portfolio,
            "risk_tolerance": self.risk_tolerance,
        }
