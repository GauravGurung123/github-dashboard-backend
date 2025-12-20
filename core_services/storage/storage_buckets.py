import boto3
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import  settings

class LocalStorage(FileSystemStorage):
    """Local filesystem storage backend."""
    def __init__(self):
        super().__init__(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL,
        )

class MinioStorage(S3Boto3Storage):
    """MinIO (S3-compatible) storage backend."""
    def __init__(self):
        super().__init__(
            bucket_name=settings.MINIO["BUCKET"],
            region_name=settings.MINIO["REGION"],
            endpoint_url=settings.MINIO["ENDPOINT_URL"],
            access_key=settings.MINIO["ACCESS_KEY"],
            secret_key=settings.MINIO["SECRET_KEY"]
        )
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.MINIO["ENDPOINT_URL"],
            aws_access_key_id=settings.MINIO["ACCESS_KEY"],
            aws_secret_access_key=settings.MINIO["SECRET_KEY"],
            region_name=settings.MINIO["REGION"],
            use_ssl=settings.MINIO["SSL"],
        )

    def get_url(self, name, expire_seconds=3600):
        return self.client.generate_presigned_url("get_object",
            Params={"Bucket": settings.MINIO["BUCKET"], "Key": name},
            ExpiresIn=expire_seconds,
        )
        # return f"{self.endpoint_url}/{self.bucket_name}/{name}"