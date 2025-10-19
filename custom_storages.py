from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = getattr(settings, 'STATICFILES_LOCATION', 'static')


class MediaStorage(S3Boto3Storage):
    location = getattr(settings, 'MEDIAFILES_LOCATION', 'media')
