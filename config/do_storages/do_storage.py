from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False


class AutoServisMediaStorage(S3Boto3Storage):
    location = "slike-servisa"
    default_acl = "public-read"
    file_overwrite = False
