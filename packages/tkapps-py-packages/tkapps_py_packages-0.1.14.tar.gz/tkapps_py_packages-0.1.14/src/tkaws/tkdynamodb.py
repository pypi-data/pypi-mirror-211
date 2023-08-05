import os
import boto3
from boto3.dynamodb.conditions import Key

class Tkdynamodb:
    def __init__(self, region=None):
        """
        :param region: The region for AWS S3
        """
        self.service_name = 'dynamodb'
        if region is None:
            region = os.getenv("DYNAMODB_REGION")
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

    def get_resource(self):
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def scan_all(self, table_name):
        """
        param: table_name
        return: all the data of table
        desc: LastEvaluatedKey is returned by dynamodb when the result is large so parameter returned as
        part of pagination.
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.scan()
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            data.extend(result['Items'])
        return data

    def insert_item(self, table_name, item):
        """
        param: table_name,item
        return: boolean value
        desc:Adds an object to a bucket.
        """
        try:
            self.get_resource()
            table = self.resource.Table(table_name)
            table.put_item(
                Item=item
            )
            return True
        except Exception as err:
            return False

    def delete_item(self, table_name, item):
        """
        param: table_name,item
        return: boolean value
        desc:deletes an object from a bucket.
        """
        try:
            self.get_resource()
            table = self.resource.Table(table_name)
            table.delete_item(
                Key=item
            )
            return True
        except Exception as err:
            return False

    def scan_item_with_filter(self, table_name, key, value):
        """
        param: table_name,key,value
        return: all the data of table
        desc: LastEvaluatedKey is returned by dynamodb when the result is large so parameter returned as
        part of pagination. result extracted on the basis of condition of key:value.
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.scan(
            FilterExpression=Key(key).eq(value),
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(FilterExpression=Key(key).eq(value),
                                ConsistentRead=True,
                                ExclusiveStartKey=result['LastEvaluatedKey']
                                )
            data.extend(result['Items'])
        return data

    def scan_item_with_begin_str(self, table_name, pk, pk_val, sk, sk_beginstr):
        """
        param: table_name,pk,pk_val,sk,sk_beginstr.
        return: the data of table.
        desc: Result extracted on the basis of condition of pk:pk_value and sk:sk_beginstr*
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.query(
            KeyConditionExpression=Key(pk).eq(pk_val) & Key(sk).begins_with(sk_beginstr),
            ConsistentRead=True
        )
        return result["Items"]

    def get_item_by_key(self, table_name, key):
        """
        param: table_name,key (primary key)
        return: a set of attributes for the item for a given primary key
        desc:
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.get_item(Key=key)
        return result["Item"]

    def scan_items_by_expression(self, table_name, expr):
        """
        param: table_name,expr
        return: data of table matching expr
        desc: LastEvaluatedKey is returned by dynamodb when the result is large so parameter returned as
        part of pagination. result extracted on the basis of condition of expr
        """
        try:
            self.get_resource()
            table = self.resource.Table(table_name)
            result = table.scan(
                FilterExpression=expr,
                ConsistentRead=True
            )
            data = result["Items"]
            while 'LastEvaluatedKey' in result:
                result = table.scan(FilterExpression=expr,
                ConsistentRead=True, ExclusiveStartKey=result['LastEvaluatedKey'])
                data.extend(result['Items'])
            return data
        except Exception as err:
            return []

    def query_item_with_pk(self, table_name, pk, pkVal):
        """
        param: table_name,pk,pk_val
        return: data of table matching condition
        desc: LastEvaluatedKey is returned by dynamodb when the result is large so parameter returned as
        part of pagination. result extracted on the basis of pk:pkVal
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.query(
            KeyConditionExpression=Key(pk).eq(pkVal),
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pkVal),
                ExclusiveStartKey=result['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data

