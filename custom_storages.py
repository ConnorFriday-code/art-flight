from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print(">>> [DEBUG] custom_storages.py loaded")

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    def __init__(self, *args, **kwargs):
        print(f">>> [DEBUG] StaticStorage initialised with location = {self.location}")
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def __init__(self, *args, **kwargs):
        print(f">>> [DEBUG] MediaStorage initialised with location = {self.location}")
        super().__init__(*args, **kwargs)
