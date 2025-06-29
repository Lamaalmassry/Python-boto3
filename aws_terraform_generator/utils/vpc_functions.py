from typing import List, Dict
import boto3

def list_vpcs(session: boto3.Session) -> List[Dict]:
    """Fetch all VPCs in the region."""
    client = session.client("ec2")
    response = client.describe_vpcs()
    return response["Vpcs"]

def generate_vpc_terraform(vpcs: List[Dict]) -> str:
    """Generate Terraform code for VPCs."""
    tf_code = ""
    for vpc in vpcs:
        name = next((tag["Value"] for tag in vpc.get("Tags", []) if tag["Key"] == "Name"), vpc["VpcId"])
        tf_code += f"""
resource "aws_vpc" "vpc_{vpc['VpcId']}" {{
  cidr_block = "{vpc['CidrBlock']}"
  enable_dns_hostnames = {str(vpc.get('EnableDnsHostnames', False)).lower()}
  enable_dns_support = {str(vpc.get('EnableDnsSupport', True)).lower()}
  tags = {{
    Name = "{name}"
  }}
}}
"""
    return tf_code