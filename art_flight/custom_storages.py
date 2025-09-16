from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print(">>> [DEBUG] custom_storages.py has been imported")


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        print(">>> [DEBUG] StaticStorage is being initialized")
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def __init__(self, *args, **kwargs):
        print(">>> [DEBUG] MediaStorage is being initialized")
        super().__init__(*args, **kwargs)
