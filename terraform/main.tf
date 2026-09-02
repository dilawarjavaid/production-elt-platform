terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "raw_bucket" {
  bucket = "production-elt-platform-dilawarjavaid-2026"
}

output "raw_bucket_name" {
  value = aws_s3_bucket.raw_bucket.bucket
}

output "raw_bucket_region" {
  value = aws_s3_bucket.raw_bucket.region
}

resource "aws_s3_bucket_versioning" "raw_bucket_versioning" {
  bucket = aws_s3_bucket.raw_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "raw_bucket_public_access" {
  bucket = aws_s3_bucket.raw_bucket.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}