
# Auto-generated Terraform configuration for AWS VPCs
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "vpc-01af746b63d64f798" {
  cidr_block = "172.31.0.0/16"
  tags = {
    Name = "vpc-01af746b63d64f798"
  }
}
