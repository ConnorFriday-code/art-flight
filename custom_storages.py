from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        print(">>> Initializing StaticStorage (S3)...")
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        print(">>> Initializing MediaStorage (S3)...")
        super().__init__(*args, **kwargs)
