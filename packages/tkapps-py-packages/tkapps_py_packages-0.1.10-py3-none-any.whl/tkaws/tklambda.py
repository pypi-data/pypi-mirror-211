import os
import boto3
import json
from decimal import Decimal

class Tklambda:
    def __init__(self, region=None):
        """
        :param region: The region for AWS Lambda
        """
        self.service_name = 'lambda'
        if region is None:
            region = os.getenv("LAMBDA_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60

    def get_client(self):
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def invoke_lambda(self, lambda_arn, payload):
        """
        param: lambda_arn, payload
        return: response from the lambda function
        desc: invoking lambda fn byproviding lambda amazon resource number (arn), invocation type as asynchronous
            and the input data.
        """
        try:
            def default(obj):
                if isinstance(obj, Decimal):
                    return str(obj)
            self.get_client()
            response = self.client.invoke(
                FunctionName=lambda_arn,
                InvocationType='Event',
                Payload=json.dumps(payload, default=default)
            )
            return response
        except Exception as e:
            return False


