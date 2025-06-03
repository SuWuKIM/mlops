class S3:
    def __init__(self, endpoint, access_key_id, secret_key, dataset_dir):
        import boto3

        self.dataset_dir = dataset_dir
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
        )

    def down(self, bucket, key):
        import os

        name = os.path.basename(key)
        dest_path = os.path.join(self.dataset_dir, name)
        self.client.download_file(bucket, key, dest_path)
        print(f"success download at: {dest_path}")
