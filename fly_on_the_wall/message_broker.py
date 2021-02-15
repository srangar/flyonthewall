import boto3


class MessageBroker:
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def enqueue(self, message: dict):
        sqs = boto3.resource("sqs", region_name=self.aws_region, config=config)
        queue = sqs.get_queue_by_name(QueueName=self.queue_name)
        response = queue.send_message(MessageBody=json.dumps({"message": message}))

        print(f"MessageID={response.get('MessageId')}")
        print(f"MD5OfMessageBody={response.get('MD5OfMessageBody')}")
