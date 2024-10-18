import boto3
from boto3 import s3
from decouple import config


class S3Service:
    def __init__(self):
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id= config("AWS_KEY"),
            aws_secret_access_key = config("ASW_SECRET"),
        )

    def upload_file(self, path_to_store_photo, photo_name, bucket_name =None, region=None):
        if bucket_name:
            bucket = config("BUCKET_NAME")

        if region:
            region = config("REGION")

        self.s3.meta.client.upload_file(path_to_store_photo, bucket_name, photo_name)
        bucket_url = f"https://{bucket_name}.s3.{config("BUCKET_REGION")}.amazonaws.com/{photo_name}"
        return bucket_url