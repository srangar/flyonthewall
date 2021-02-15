import os
import uuid
import boto3
import botocore.exceptions

from fly_on_the_wall import exceptions


class Customer:
    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        customer_id: str,
        alexa_notif_bearer: str,
    ):
        self.customer_id = customer_id
        self.alexa_notif_bearer = alexa_notif_bearer

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
            )
        except KeyError as err:
            raise exceptions.UserLoadError(f"customer id: {customer_id}") from err

    def save(self, create=False):
        try:
            item = {
                "customer_id": self.customer_id,
                "alexa_notif_bearer": self.alexa_notif_bearer,
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
        }
