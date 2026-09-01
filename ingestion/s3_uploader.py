import os

import boto3
from dotenv import load_dotenv


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if not S3_BUCKET_NAME:
    raise ValueError("S3_BUCKET_NAME is not configured")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


def upload_file_to_s3(local_path, dataset_name, ingestion_date, filename):
    s3_key = (
        f"raw/{dataset_name}/"
        f"ingestion_date={ingestion_date}/"
        f"{filename}"
    )

    s3.upload_file(
        str(local_path),
        S3_BUCKET_NAME,
        s3_key
    )

    print(
        f"Uploaded to S3 -> "
        f"s3://{S3_BUCKET_NAME}/{s3_key}"
    )

    return s3_key