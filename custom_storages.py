from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import traceback


class StaticStorage(S3Boto3Storage):
    # class attribute read at import time (safe)
    location = getattr(settings, 'STATICFILES_LOCATION', 'static')
    print(f">>> [DEBUG] StaticStorage defined with location = {location!r} (class-level)")

    def __init__(self, *args, **kwargs):
        """
        This runs when Django instantiates the storage. We log success/failure here.
        Note: __init__ should not normally raise for a simple config, but if boto3 tries
        to connect or credentials are missing, we will capture and log the exception.
        """
        print(">>> [DEBUG] StaticStorage.__init__ called")
        try:
            super().__init__(*args, **kwargs)
            print(">>> [DEBUG] StaticStorage.__init__ completed successfully")
        except Exception as e:
            print(">>> [DEBUG] StaticStorage.__init__ raised exception:", e)
            traceback.print_exc()
            # Re-raise so it shows clearly in build/release logs (comment out to avoid fatal failure)
            raise


class MediaStorage(S3Boto3Storage):
    location = getattr(settings, 'MEDIAFILES_LOCATION', 'media')
    print(f">>> [DEBUG] MediaStorage defined with location = {location!r} (class-level)")

    def __init__(self, *args, **kwargs):
        print(">>> [DEBUG] MediaStorage.__init__ called")
        try:
            super().__init__(*args, **kwargs)
            print(">>> [DEBUG] MediaStorage.__init__ completed successfully")
        except Exception as e:
            print(">>> [DEBUG] MediaStorage.__init__ raised exception:", e)
            traceback.print_exc()
            raise
