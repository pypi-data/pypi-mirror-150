import s3fs
from bdaserviceutils import get_cmd_arg
from minio import Minio


def set_connection(access_key, secret_key, url):

    minio_access_key = access_key
    minio_secret_key = secret_key
    endpoint_url = url

    class S3FileSystemPatched(s3fs.S3FileSystem):
        def __init__(self, *k, **kw):
            
            # Fix for calling set connection as many times as needed. Another fix is to remove kw from init method.
            if "key" in kw:
                kw.pop("key")
                kw.pop("secret")
                kw.pop("client_kwargs")
            
            super(S3FileSystemPatched, self).__init__( *k,
                                                    key = minio_access_key,
                                                    secret = minio_secret_key,
                                                    client_kwargs={'endpoint_url': endpoint_url},
                                                    **kw)
            print('S3FileSystem is patched with url:  ' + endpoint_url)

    s3fs.S3FileSystem = S3FileSystemPatched


def minio_ls(address, access_key, secret_key, bucket_name, folder, extention):

    if folder[-1] != "/":
        folder = folder + "/"

    client = Minio(
        address,
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )
    objects = client.list_objects(bucket_name=bucket_name, prefix=folder)

    return [x._object_name for x in objects if extention in x._object_name[-len(extention):]]



# def get_path(name):
#     set_connection(access_key=get_cmd_arg("minIO_ACCESS_KEY-" + name), secret_key=get_cmd_arg("minIO_SECRET_KEY-" + name), url=get_cmd_arg("minIO_URL-" + name))
#     return "s3://" + get_cmd_arg("minio_bucket-" + name) + "/" + get_cmd_arg(name)


def get_path(name):
    # Get credentials
    minio_url = get_cmd_arg("minIO_URL-" + name)
    access_key = get_cmd_arg("minIO_ACCESS_KEY-" + name)
    secret_key = get_cmd_arg("minIO_SECRET_KEY-" + name)
    bucket_name = get_cmd_arg("minio_bucket-" + name)
    
    # Set connection for pandas reading
    set_connection(access_key=access_key, secret_key=secret_key, url=minio_url)

    # TODO Needs a better way to find out if dataset is an input or output one
    if "input" in name:
        # List all files in dataset folder
        files_list = minio_ls(address=minio_url.replace("http://", ""), access_key=access_key, secret_key=secret_key, bucket_name=bucket_name, 
                                folder=get_cmd_arg(name),
                                extention=".csv")
        if len(files_list) > 1:
            return ["s3://" + bucket_name + "/" + x for x in files_list]
        elif len(files_list) == 1:
            return "s3://" + bucket_name + "/" + files_list[0]
        else:
            raise Exception("Dataset is empty!")

    elif "output" in name:
        return "s3://" + bucket_name + "/" + get_cmd_arg(name) + "/dataset.csv"
    else:
        raise Exception("Error: currently only input-dataset and output-dataset dataset names are supported!")