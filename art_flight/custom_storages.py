from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        print(">>> [DEBUG] StaticStorage is being used for collectstatic")
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
