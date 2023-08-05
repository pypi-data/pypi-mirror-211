import os
import boto3
from botocore.exceptions import ClientError

class Tksns:
    def __init__(self, region=None):
        """
        :param region: The region for AWS SES
        """
        self.service_name = 'sns'
        if region is None:
            region = os.getenv("SNS_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        self.http_timeout = 60

    def send_notification(self, email, save_copy=False):
        try:
            response = self.client.send_raw_email(
                Source=email.from_email,
                Destinations=to_emails + cc_emails,
                RawMessage={
                    'Data': email.as_string(),
                }
            )
            return True
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False




