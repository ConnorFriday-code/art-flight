from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print(">>> [DEBUG] custom_storages.py loaded")


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    print(">>> [DEBUG] StaticStorage initialised with location =", self.location)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    print(">>> [DEBUG] MediaStorage initialised with location =", self.location)
