import boto3, uuid

class CloudStorage:
    def __init__(self, id, password, bucket):
        self.id        = id
        self.password  = password
        self.bucket    = bucket
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id     = self.id,
            aws_secret_access_key = self.password
        )

    def upload_file(self, image):
        upload_key = str(uuid.uuid4()).replace("-","") + image.name
        
        self.s3_client.upload_fileobj(
            image,
            self.bucket,
            upload_key,
            ExtraArgs = {
                "ContentType": image.content_type
            }
        )
        return upload_key
