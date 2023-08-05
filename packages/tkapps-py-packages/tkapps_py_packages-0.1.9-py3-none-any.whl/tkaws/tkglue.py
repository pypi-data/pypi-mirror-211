import os, time
import boto3
from boto3.dynamodb.conditions import Key


class Tkglue:
    def __init__(self, region=None):
        """
        :param region: The region for AWS Glue
        """
        self.service_name = 'glue'
        if region is None:
            region = os.getenv("GLUE_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60
        self.env = os.getenv("ENV")
        self.db = 'dynamodb'
        self.db_resource = boto3.resource(self.db, region_name=self.region)

    def get_client(self):
        """
        To be used internally for the purpose of creating the boto3 client of Glue.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_resource(self):
        """
        To be used internally for the purpose of creating the boto3 resource of Glue.
        This method creates the boto3 resource for AWS, The resource can later be accessed using 'self.resource'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def start_job(self):
        return True

    # def get_table(self,table_name):
    #     if str(self.env).lower() in ['prod', 'prod1']:
    #         return str(table_name).lower()
    #     else:
    #         return self.env + "_" + str(table_name).lower()
    #
    # def get_this_job(self,job_month, job_id):
    #     try:
    #         STATUS_TABLE = self.get_table("tdp_etl_job_status")
    #         table = self.db_resource.Table(STATUS_TABLE)
    #         response = table.query(
    #             KeyConditionExpression=Key('job_month').eq(job_month) & Key('job_id').eq(job_id)
    #         )
    #         return response['Items']
    #     except Exception as err:
    #         print("Exception @ GetStatusSupport.get_this_job_logs :: {}".format(str(err)))
    #         return False
    #
    # def update_stop_job(self,item):
    #     try:
    #         item['job_status'] = "STOPPED"
    #         item['job_phase_status'] = "STOPPED"
    #         item['end_timestamp'] = int(time.time() * 1000)
    #         STATUS_TABLE = self.get_table("tdp_etl_job_status")
    #         table = self.db_resource.Table(STATUS_TABLE)
    #         table.put_item(
    #             Item=item
    #         )
    #         return True
    #     except Exception as err:
    #         print("Exception @ get_jobs_support.stop_job :: {}".format(str(err)))
    #         return False

    def stop_job_run(self, glue_job_name, glue_job_id):
        try:
            glueClient = self.get_resource().resource
            response = glueClient.batch_stop_job_run(
                JobName=glue_job_name,
                JobRunIds=[
                    glue_job_id,
                ]
            )
            return response
        except Exception as err:
            print("Exception @ GetJobs.stop_jobs :: {}".format(str(err)))
            return 'code: ERROR, {message: Internal Server Error}'
