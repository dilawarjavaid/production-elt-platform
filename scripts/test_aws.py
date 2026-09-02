import os

import boto3
from dotenv import load_dotenv


load_dotenv()

bucket_name = os.getenv("S3_BUCKET_NAME")
region = os.getenv("AWS_REGION")

if not bucket_name:
    raise ValueError("S3_BUCKET_NAME is not configured")

s3 = boto3.client(
    "s3",
    region_name=region
)

response = s3.list_objects_v2(
    Bucket=bucket_name
)

print("AWS connection successful!")
print(f"Bucket: {bucket_name}")
print(f"Region: {region}")
print(f"Objects found: {response.get('KeyCount', 0)}")