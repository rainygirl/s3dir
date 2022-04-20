import boto3


class S3:
    def __init__(self, bucket):

        self.s3 = boto3.resource("s3")
        self.bucket = bucket
        self.bucket_object = self.s3.Bucket(bucket)

    def load_data(self, prefix):
        paginator = self.bucket_object.meta.client.get_paginator("list_objects")
        iterator = paginator.paginate(
            Bucket=self.bucket,
            Prefix=prefix,
            Delimiter="/",
            PaginationConfig={"MaxItems": 1000},
        )

        l = len(prefix)
        for result in iterator:
            dirs = [d["Prefix"][l:] for d in result.get("CommonPrefixes", [])]
            files = [
                {
                    "key": f["Key"][l:],
                    "size": f["Size"],
                }
                for f in result.get("Contents", [])
                if f["Key"][l:] != ""
            ]

            if prefix == "":
                return dirs + files

            return [".."] + dirs + files

    def download(self, key, destination):
        self.bucket_object.download_file(key, destination)

    def upload(self, source, key):
        self.bucket_object.upload_file(source, key)

    @staticmethod
    def parent_dir(path):
        if len(path.split("/")) == 2:
            return ""
        return path[: path[:-1].rfind("/")] + "/"
