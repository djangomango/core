from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.azure_storage import AzureStorage
from storages.backends.s3boto3 import S3Boto3Storage


class S3BotoPublicMediaStorage(S3Boto3Storage):
    default_acl = "public-read"

    if settings.AWS_MEDIA_STORAGE:
        location = settings.AWS_S3_MEDIA_ROOT


class S3BotoPrivateMediaStorage(S3Boto3Storage):
    default_acl = "private"

    if settings.AWS_MEDIA_STORAGE:
        location = settings.AWS_S3_MEDIA_ROOT


class AzurePublicMediaStorage(AzureStorage):
    if settings.AZURE_MEDIA_STORAGE:
        account_name = settings.AZURE_BLOB_ACCOUNT_NAME
        account_key = settings.AZURE_BLOB_ACCOUNT_KEY
        azure_container = settings.AZURE_BLOB_CONTAINER_NAME
        expiration_secs = None


class AzurePrivateMediaStorage(AzureStorage):
    if settings.AZURE_MEDIA_STORAGE:
        account_name = settings.AZURE_BLOB_ACCOUNT_NAME
        account_key = settings.AZURE_BLOB_ACCOUNT_KEY
        azure_container = settings.AZURE_BLOB_CONTAINER_NAME
        expiration_secs = 60


class AzurePrivateProductStorage(AzureStorage):
    if settings.AZURE_MEDIA_STORAGE:
        account_name = settings.AZURE_BLOB_ACCOUNT_NAME
        account_key = settings.AZURE_BLOB_ACCOUNT_KEY
        azure_container = "product"
        expiration_secs = 60


private_storage_class = get_storage_class(settings.STORAGES['private']['BACKEND'])
private_storage = private_storage_class()
