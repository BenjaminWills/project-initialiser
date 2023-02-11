import boto3
from botocore.exceptions import ClientError
from make_logger import make_logger

logger = make_logger(
    logging_path="./s3_log.log", save_logs=True, logger_name="s3_logger"
)


class S3:
    """
    A helper class for boto3 s3 operations.
    """

    def __init__(
        self,
        ACCESS_KEY_ID: str = None,
        SECRET_ACCESS_KEY: str = None,
        region_name: str = None,
    ) -> None:
        logger.info("Initialsing client")
        self.client = boto3.client(
            "s3",
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name=region_name,
        )
        logger.info("Initialsing resource")
        self.resource = boto3.resource(
            "s3",
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name=region_name,
        )

    def create_bucket(self, bucket_name: str, region: str = None) -> bool:
        try:
            logger.info("Begining bucket creation")
            if region is None:
                s3_client = self.client
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                logger.info(f"Creating bucket in region: {region}")
                s3_client = boto3.client("s3", region_name=region)
                location = {"LocationConstraint": region}
                s3_client.create_bucket(
                    Bucket=bucket_name, CreateBucketConfiguration=location
                )
            logger.info("Bucket successfully created")
            return True
        except ClientError as e:
            logger.exception(e)
            return False

    def delete_bucket(self, bucket_name: str) -> bool:
        try:
            s3_client = self.client
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            file_count = objects["KeyCount"]
            if file_count == 0:
                s3_client.delete_bucket(Bucket=bucket_name)
            else:
                return False
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def add_item_to_bucket(
        self, file_path: str, bucket_name: str, file_name: str
    ) -> bool:
        try:
            s3_client = self.client
            s3_client.upload_file(file_path, bucket_name, file_name)
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def list_bucket_contents(self, bucket_name: str) -> list:
        try:
            s3_resource = self.resource
            bucket = s3_resource.Bucket(bucket_name)
            contents = [file.key for file in bucket.objects.all()]
        except ClientError as e:
            logger.error(e)
            return False
        return contents

    def delete_bucket_item(self, bucket_name: str, file_name: str) -> bool:
        try:
            s3_resource = self.resource
            target = s3_resource.Object(bucket_name, file_name)
            target.delete()
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def list_s3_buckets(self, verbose: bool = True) -> list:
        try:
            s3 = self.client
            buckets = s3.list_buckets()["Buckets"]
            if verbose:
                logger.info("-" * 60)
                logger.info("Bucket names:")
                for index, bucket in enumerate(buckets):
                    logger.info(f"{index+1} : {bucket['Name']}")
                logger.info("-" * 60)
            return buckets
        except ClientError as e:
            logger.error(e)
            return False

    def download_object(self, bucket_name: str, object_name: str, output_path: str):
        try:
            logger.info(
                f"Downloading {object_name} from {bucket_name} and saving it to {output_path}."
            )
            self.client.download_file(bucket_name, object_name, output_path)
            logger.info("Download completed succesfully.")
        except ClientError as e:
            logger.error(e)
