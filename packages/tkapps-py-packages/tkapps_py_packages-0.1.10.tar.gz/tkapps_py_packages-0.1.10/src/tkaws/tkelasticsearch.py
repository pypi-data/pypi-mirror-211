import os
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk, scan
from requests_aws4auth import AWS4Auth



class Tkelasticsearch:
    def __init__(self, region=None):
        """
        :param region: The region for AWS ElasticSearch
        """
        self.service_name = 'es'
        if region is None:
            region = os.getenv("ES_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.env = os.getenv("ENV", "local")
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60

    def get_host_and_port(self):
        host = os.getenv("ES_HOST")
        port = 443
        if self.env == "local":
            host = os.getenv("ES_ENDPOINT")
        return host, port


    def get_es_client(self):
        cred_type = os.getenv("CRED_TYPE")
        access_key = os.getenv("ACCESS_KEY")
        secret_key = os.getenv("SECRET_KEY")
        region = os.getenv("ES_REGION", "us-west-1")
        host, port = self.get_host_and_port()
        print(f"{host}, {port}, {self.env}")
        if self.env == "local":
            es = Elasticsearch(host)
            return es

        if cred_type == "ROLE":
            credentials = boto3.Session(region_name=region).get_credentials()
        else:
            credentials = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)\
                .get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, self.service_name,
                           session_token=credentials.token)
        es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=awsauth, use_ssl=True, verify_certs=True,
                           connection_class=RequestsHttpConnection)
        return es


    def insert_record_with_id(self, index, id, record, es_client=None):
        """
        :param index:
        :param id:
        :param record:
        :param es_client:
        :return:
        """
        if es_client is None:
            es_client = self.get_es_client()
        es_client.index(index=index, id=id, body=record)
        return True



    def update_record_with_id(self, index, id, record, es_client=None):
        """
        param: index,id,record,es_client
        return: boolean
        """
        if es_client is None:
            es_client = self.get_es_client()
        es_client.update(index=index, id=id, body=record)
        return True

    def generate_bulk_index_data(self, index, records, id_key=None):
        """

        :param index,records, id_key:
        :return: yield helps in creating indices
        """
        for record in records:
            item = dict()
            item["_index"] = index
            item["_source"] = record
            if id_key is not None:
                item['_id'] = record[id_key]
            yield item


    def bulk_insert_record_with_id(self, index, id_field, records, es_client=None):
        """
        param: index,id_field,records,es_client:
        return: boolean
        desc:
        """
        if es_client is None:
            es_client = self.get_es_client()
        bulk(es_client, self.generate_bulk_index_data(index, records, id_field))
        return True

    def search_records(self, index, query, es_client=None):
        if es_client is None:
            es_client = self.get_es_client()
        return es_client.search(index=index, body=query)


    def search_records_with_scroll(self, index, query, es_client=None):
        """
        param index,query, es_client:
        return: The Scroll API allows you to retrieve a large result set in manageable portions and scroll parameter
        specifies the duration of the scroll window.
        The response contains the scroll ID and the initial set of search results depending on provided query.
        """
        if es_client is None:
            es_client = self.get_es_client()
        return es_client.search(index=index, body=query, scroll='1m')

    def scroll_records(self, scroll_id, es_client=None):
        """

        :param scroll_id:
        :param es_client:
        :return: The scroll method return subsequent scroll requests pertaining to specific scroll id
        The scroll ID remains valid for the duration specified in the initial search request.
        """
        if es_client is None:
            es_client = self.get_es_client()
        return es_client.scroll(scroll_id=scroll_id, scroll='1m')


    def get_records_count(self, index, query, es_client=None):
        if es_client is None:
            es_client = self.get_es_client()
        return es_client.count(index=index, body=query)

    def delete_records(self, index, query, es_client=None):
        if es_client is None:
            es_client = self.get_es_client()
        es_client.delete_by_query(index=index, body=query)
        return True


    def delete_record_by_id(self, index, id, es_client=None):
        if es_client is None:
            es_client = self.get_es_client()
        es_client.delete(index=index, id=id)
        return True


    def get_record_by_id(self, index, id, es_client=None):
        """

        :param index:
        :param id:
        :param es_client:
        :return: returnds record having param id
        """
        if es_client is None:
            es_client = self.get_es_client()
        return es_client.get(index=index, id=id)

    def scan_all_records(self, index, query, es_client=None):
        if es_client is None:
            es_client = self.get_es_client()
        return scan(es_client, index=index, query=query)


    def fetch_index_stats(self, index_name, es_client=None):
        """

        :param index_name:
        :param es_client:
        :return:retireve statistics for mentioned index_name
        """
        if es_client is None:
            es_client = self.get_es_client()
        return es_client.indices.stats(index=index_name)