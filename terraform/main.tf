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