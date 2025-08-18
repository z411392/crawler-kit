from typing import Any
from firebase_admin import storage, initialize_app
from crawler_kit.utils.google_cloud.credentials_from_env import credentials_from_env
from os import environ

STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET')
try:
    from firebase_admin import get_app
    get_app()
except ValueError:
    credentials = credentials_from_env()
    initialize_app(credentials, {'storageBucket': STORAGE_BUCKET})


def set_object(key: str, obj: Any):
    bucket = storage.bucket()
    blob = bucket.blob(key)
    
    if isinstance(obj, str):
        blob.upload_from_filename(obj)
    elif isinstance(obj, bytes):
        blob.upload_from_string(obj, content_type='image/png')
    else:
        raise TypeError(f"Unsupported data type: {type(obj)}")

def save_screenshot(key: str, image_data: bytes) -> None:

    bucket = storage.bucket()
    blob = bucket.blob(key)
    blob.upload_from_string(image_data, content_type='image/png')
    
def get_object(key: str) -> bytes:

    bucket = storage.bucket()
    blob = bucket.blob(key)
    return blob.download_as_bytes()

def get_download_url(key: str) -> str:

    from datetime import datetime, timedelta
    
    bucket = storage.bucket()
    blob = bucket.blob(key)
    
    expiration = datetime.now(datetime.timezone.utc) + timedelta(hours=1)
    return blob.generate_signed_url(expiration=expiration, method='GET')

def delete_object(key: str) -> None:
    bucket = storage.bucket()
    blob = bucket.blob(key)
    blob.delete()

def object_exists(key: str) -> bool:
    bucket = storage.bucket()
    blob = bucket.blob(key)
    return blob.exists()