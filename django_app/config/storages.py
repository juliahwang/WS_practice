from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    # 같은 이름의 미디어파일이 덮어써지지 않도록 False로 설정.기본값은 True이다.
    file_overwrite = False
