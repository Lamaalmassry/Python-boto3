# utils/terraform_generator.py
from typing import List, Dict

def generate_terraform_vpc(vpcs: List[Dict]) -> None:
    """
    Generate Terraform configuration file for VPCs.

    Args:
        vpcs: List of dictionaries containing VPC details.

    Raises:
        IOError: If writing to the file fails.
    """
    terraform_content = """
# Auto-generated Terraform configuration for AWS VPCs
provider "aws" {
  region = "us-east-1"
}
"""
    
    for vpc in vpcs:
        vpc_resource = f"""
resource "aws_vpc" "{vpc['id']}" {{
  cidr_block = "{vpc['cidr_block']}"
  tags = {{
    Name = "{vpc['name']}"
  }}
}}
"""
        terraform_content += vpc_resource
    
    try:
        with open('vpcs.tf', 'w') as f:
            f.write(terraform_content)
    except IOError as e:
        raise Exception(f"Failed to write Terraform file: {str(e)}")