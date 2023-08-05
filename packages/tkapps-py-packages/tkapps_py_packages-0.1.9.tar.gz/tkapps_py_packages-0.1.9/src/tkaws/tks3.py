import os
import boto3,math,json,codecs,traceback,shutil
from botocore.exceptions import ClientError

class Tks3:
    def __init__(self, region=None):
        """
        :param region: The region for AWS S3
        """
        self.service_name = 's3'
        if region is None:
            region = os.getenv("S3_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60
        self.env=os.getenv("ENV")

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

    def generate_presigned_get_url(self, s3_bucket, s3_key):
        """
        param: s3_bucket,s3_key:
        return:URL
        desc: Pre-signed URLs are time-limited URLs here 1hr that grant temporary access to the specified resource,
        allowing clients to perform operations without requiring their own AWS credentials.
        """
        self.get_client()
        url = self.client.generate_presigned_url('get_object', Params={'Bucket': s3_bucket, 'Key': s3_key},
                                                 ExpiresIn=3600)
        url = url.replace(f"s3.{self.region}.amazonaws.com/{s3_bucket}", f"{s3_bucket}.s3-{self.region}.amazonaws.com")
        return url

    def generate_presigned_post_url(self, s3_bucket, s3_key):
        """
        param: s3_bucket,s3_key
        return: URL
        desc: generate a pre-signed URL and form fields for performing a POST operation to upload an object
        to an Amazon S3 bucket. Instructions for clients to securely upload objects directly to S3.
        """
        self.get_client()
        url = self.client.generate_presigned_post(s3_bucket, s3_key, ExpiresIn=3600)
        return url

    def get_file_content(self, s3_bucket, s3_key):
        """
        param: s3_bucket, s3_key.
        return: content of file.
        """
        self.get_resource()
        obj = self.resource.Object(s3_bucket, s3_key)
        body = obj.get()['Body'].read().decode(encoding="utf-8", errors="ignore")
        return body

    def get_file_object(self, s3_bucket, s3_key):
        """
        param: s3_bucket, s3_key.
        return: object
        """
        self.get_resource()
        return self.resource.Object(s3_bucket, s3_key).get()

    def upload_local_file_to_s3(self, s3_bucket, s3_key, local_path):
        """
        param: s3_bucket, s3_key, local_path
        return: boolean value
        desc: upload file to path
        """
        try:
            self.get_client()
            self.client.upload_file(local_path, s3_bucket, s3_key)
            return True
        except Exception as e:
            print("Exception at upload_local_file_to_s3", str(e))
            return False

    def delete_s3_object(self,oldFilePath, oldFileName):
        """
        param: oldfilepath,oldfilename
        return:
        desc: delete s3 object
        """
        self.get_client()
        self.get_resource()
        s3_client=self.client
        response = s3_client.list_objects(Bucket=oldFilePath.split('/')[0],
                                          Prefix=oldFilePath.split('/', 1)[1])
        for obj in response['Contents']:
            fileName = obj['Key'].split('/')[-1]
            if (fileName != "" and fileName != "_SUCCESS" and
                    fileName is oldFileName):
                s3=self.resource
                obj = s3.Object(oldFilePath.split('/')[0],
                                oldFilePath.split('/', 1)[1] + fileName)
                obj.delete()
                # LogSupport.console_log("Deleted file : {}".format(str(fileName)))

    def rename_s3_object(self,oldFilePath, newFileName):
        """
        param: oldfilepath,NewFilename
        return:
        desc: access the obj though path provided and rename s3 object.
        """
        self.get_client()
        self.get_resource()
        s3_client = self.client
        response = s3_client.list_objects(Bucket=oldFilePath.split('/')[0],
                                          Prefix=oldFilePath.split('/', 1)[1])
        for obj in response['Contents']:
            file_name = obj['Key'].split('/')[-1]
            if (file_name != "" and file_name != "_SUCCESS" and
                    file_name != newFileName):

                s3 = self.resource
                s3.Object(oldFilePath.split('/')[0], oldFilePath.split('/', 1)[
                    1] + '/' + newFileName).copy_from(
                    CopySource=oldFilePath + '/' + file_name)
                s3.Object(oldFilePath.split('/')[0],
                          oldFilePath.split('/', 1)[1] + '/' + file_name).delete()

    def __convert_size(self,size_bytes):
        """
        param: size_bytes
        return: string containing size with suitable units of data.
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_file_size(self,bucket_name, s3_prefix):
        """
        param: bucket, s3_prefix
        return: returns object  size.
        """
        try:
            self.get_resource()
            s3=self.resource
            my_bucket = s3.Bucket(bucket_name)
            file_size = 0
            for srcFile in my_bucket.objects.filter(Prefix=s3_prefix):
                file_size = file_size + s3.Object(bucket_name, srcFile.key).content_length
            file_size = self.__convert_size(file_size)
            return file_size
        except Exception as err:
            print("Exception occurred at get_file_size for :-" + str(s3_prefix) + "Error:-" + str(err))
            return None

    def read_json_from_s3(self,bucket,s3key):
        """
        :param bucket,s3key
        return: obj content returned as json
        """
        try:
            self.get_client()
            s3Client = self.client
            response = s3Client.get_object(Bucket=bucket, Key=s3key)
            responseJson = json.loads(response['Body'].read().decode('utf-8'))
            return responseJson
        except Exception as err:
            print("Exception occurred while reading json from s3 read_json_from_s3:", str(err))

    def write_json_to_s3(self,data, bucket, s3_key):
        """
        param: bucket,s3key
        desc: write data as json to s3object
        """
        try:
            self.get_client()
            s3_client = self.client
            data = json.dumps(data).encode('UTF-8')
            s3_client.put_object(Body=data, Bucket=bucket, Key=s3_key)
        except Exception as err:
            print("Exception occurred while writing json from s3 :: {}".format(str(err)))

    def get_all_folders(self,bucket, s3Key):
        """
        param: bucket,s3Key:
        return: A list of objects with prefix s3key stored in s3bucket
        """
        try:
            self.get_client()
            s3client = self.client
            folders = list()
            paginator = s3client.get_paginator('list_objects_v2')
            result = paginator.paginate(Bucket=bucket, Prefix=s3Key)
            for prefix in result.search('Contents'):
                if prefix is not None:
                    tokens = prefix.get('Key').split('/')
                    if tokens[len(tokens) - 1] is not "":
                        folders.append(tokens[len(tokens) - 2])
            return folders
        except Exception as err:
            print("Exception occurred while getting tenant global configurations in s3 {}".format(str(err)))

    # def get_leaf_entries_local(self,bucket,s3Key):
    #     return os.listdir(EtlPathSupport.get_full_path(bucket, s3Key))
    def get_leaf_entries(self,bucket, s3Key):
        """
        Returns only the filenames in a folder
            - args
                - bucket<string>: aws bucket name
                - s3Key<string>: folder path prefix
                - s3Client<string>(optional): Aws s3 client object

            - Returns list of filenames
        """
        try:
            self.get_client()
            s3Client = self.client
            folders = list()
            paginator = s3Client.get_paginator('list_objects_v2')
            result = paginator.paginate(Bucket=bucket, Prefix=s3Key)
            for prefix in result.search('Contents'):
                if prefix is not None:
                    tokens = prefix.get('Key').split('/')
                    if tokens[len(tokens) - 1] is not "":
                        folders.append(tokens[len(tokens) - 1])
            return folders
        except Exception as err:
            print("Exception occurred while getting leaf entries in S3 {}".format(str(err)))

    def copy_s3_to_s3_local(self,bucket, sourceKey, destKey):

        copy_source = {
            'Bucket': bucket,
            'Key': sourceKey
        }
        shutil.copyfile(copy_source, destKey)

    def copy_s3_to_s3(self,bucket, sourceKey, destKey):
        """
        param: bucket,sourceKey,destKey
        desc: It is used to copy the contents of a source file to a destination file.
        """
        self.get_resource()
        s3Resource = self.resource

        copy_source = {
            'Bucket': bucket,
            'Key': sourceKey
        }
        s3Resource.meta.client.copy(copy_source, bucket, destKey)

    def delete_files_in_folder(self,bucket, folderKey):
        """
        param: bucket,folderKey
        desc: delete file of folder inside a bucket
        """
        self.get_resource()
        s3 = self.resource
        objects_to_delete = s3.meta.client.list_objects(Bucket=bucket,
                                                        Prefix=folderKey)
        delete_keys = dict()
        delete_keys['Objects'] = list()
        delete_keys['Objects'] = [{'Key': k} for k in [obj['Key'] for obj in
                                                       objects_to_delete.get(
                                                           'Contents', [])]]

        s3.meta.client.delete_objects(Bucket=bucket, Delete=delete_keys)

    def read_s3_stream(self,bucket, key, encoding='utf-8'):
        """
        Read s3 object as a s3 stream without loading it in memory
        bucket: name of bucket
        key : full/path/of/object.txt/.csv etc
        """
        try:
            self.get_resource()
            s3 = self.resource
            s3_object = s3.Object(bucket, key)
            line_stream = codecs.getreader(encoding)
            data = line_stream(s3_object.get()['Body'])
            return data
        except Exception as err:
            traceback.print_exc()
            print("Exception occurred while reading s3 stream ""in s3 {}".format(str(err)))

    def get_immediate_folders(self,bucketName, prefixName):
        self.get_client()
        result = self.client.list_objects(Bucket=bucketName, Prefix=prefixName, Delimiter='/')
        folders = list()
        for path in result.get('CommonPrefixes'):
            folders.append(path.get('Prefix'))
        return folders

    def get_leaf_folder(self,bucket, s3Key):
        try:
            self.get_client()
            s3Client = self.client
            folders = list()
            paginator = s3Client.get_paginator('list_objects_v2')
            result = paginator.paginate(Bucket=bucket, Prefix=s3Key)
            for prefix in result.search('Contents'):
                if prefix is not None:
                    tokens = prefix.get('Key').split('/')
                    if tokens[- 2] is not "":
                        folders.append(tokens[-2])
            return folders
        except Exception as err:
            print("Exception occurred while getting leaf folders in S3 {}".format(str(err)))

    def get_file_object(self,bucket, key, s3_resource=None):
        if s3_resource is None:
            s3_resource = self.get_resource().resource
        return s3_resource.Object(bucket, key).get()

    def put_object(self,bucket, key, body):
        s3_client = self.get_client().client
        return s3_client.put_object(Bucket=bucket, Body=body, Key=key)

    def get_files_from_s3(self,bucket, prefix):
        """
        accept bucket name and folder prefix and get files from s3 and append to list
        """
        try:
            li = []
            self.get_client()
            s3 = self.client()
            paginator = s3.get_paginator('list_objects')
            pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
            for page in pages:
                for obj in page['Contents']:
                    file = obj['Key']
                    li.append(file)
        except Exception as e:
            print('no files found %s', str(e))
        return li

    def empty_s3_folder(self,bucket, folder_prefix):
        """
        accept bucket name and folder prefix and delete the folder
        """
        self.get_client()
        client = self.client
        all_files = self.get_files_from_s3(bucket, folder_prefix)
        delete_us = dict(Objects=[])
        for file in all_files:
            delete_us['Objects'].append(dict(Key=file))
            # flush once aws limit reached
            if len(delete_us['Objects']) >= 1000:
                client.delete_objects(Bucket=bucket, Delete=delete_us)
                delete_us = dict(Objects=[])
        # flush rest
        if len(delete_us['Objects']):
            client.delete_objects(Bucket=bucket, Delete=delete_us)

    def get_list_of_objects(self,bucketName, prefixName):
        """
        Returns full path of the contents of a path prefix
            -args
                bucketName::string : S3 bucket name
                prefixName::string : folder path prefix
        """
        self.get_client()
        s3Client = self.client
        response = s3Client.list_objects(
            Bucket=bucketName,
            Prefix=prefixName
        )
        return response

    def get_list_of_objects_v2(self,bucket, prefix):
        keys = []
        kwargs = {'Bucket': bucket, 'Prefix': prefix}
        s3Client = self.get_client().client
        while True:
            resp = s3Client.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                keys.append(obj['Key'])

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break
        return keys

    def get_file_content(self,bucket: str, key: str, force=False, force_encoding_type=None) -> str:
        """
        Read files in bytes from S3
            - args
                - bucket<string>:: source bucket string
                - key<string>:: source key prefix path to the file
                - force <bool>:: force decode `default False`
                - force_encoding_type<string>:: used when force is True encoding types are 'utf-8','utf-16','windows-1252','cp437' `default False`

            - Returns a byte stream
        """
        try:
            self.get_resource()
            obj = self.resource.Object(bucket, key)
            body = obj.get()['Body'].read()
            encodings = ['utf-8', 'utf-16', 'windows-1252', 'cp437']
            len_encodings = len(encodings)
            if force:
                return body.decode(encoding=force_encoding_type, errors="ignore")
            for idx, encoding in enumerate(encodings):
                try:
                    body = body.decode(encoding=encoding)
                    break
                except Exception as err:
                    if (len_encodings - 1) > idx:
                        continue
                    else:
                        print("Exception@AwsS3Support.get_file_content:: Unable to correct encoding try force encoding")
            return body
        except Exception as err:
            print("Exception@AwsS3Support.get_file_content:: Unable to correct encoding try force encoding")

    def get_file_contents(self,s3Path, decode='utf-8'):
        try:
            s3Resource = self.get_resource().resource
            obj = s3Resource.Object(s3Path.split('/')[0], s3Path.split('/', 1)[1])
            try:
                body = obj.get()['Body'].read().decode(decode).splitlines()  # 'utf-8'
            except Exception as err:
                try:
                    body = obj.get()['Body'].read().decode('windows-1252').splitlines()  # 'windows-1252'
                except Exception as err:
                    body = obj.get()['Body'].read().decode('utf-16').splitlines()  # 'utf-16'
            return body
        except Exception as err:
            print("Exception @ get_file_contents.get_file_content :: {}".format(str(err)))



