import s3fs
from bdaserviceutils import get_cmd_arg


def set_connection(access_key, secret_key, url):

    minio_access_key = access_key
    minio_secret_key = secret_key
    endpoint_url = url

    class S3FileSystemPatched(s3fs.S3FileSystem):
        def __init__(self, *k, **kw):
            super(S3FileSystemPatched, self).__init__( *k,
                                                    key = minio_access_key,
                                                    secret = minio_secret_key,
                                                    client_kwargs={'endpoint_url': endpoint_url},
                                                    **kw)
            print('S3FileSystem is patched')

    s3fs.S3FileSystem = S3FileSystemPatched


def get_path(name):
    set_connection(access_key=get_cmd_arg("minIO_ACCESS_KEY-" + name), secret_key=get_cmd_arg("minIO_SECRET_KEY-" + name), url=get_cmd_arg("minIO_URL-" + name))
    return "s3://" + get_cmd_arg("minio_bucket-" + name) + "/" + get_cmd_arg(name)

