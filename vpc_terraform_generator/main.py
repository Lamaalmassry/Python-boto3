"""VPC Terraform Generator CLI tool for managing AWS VPCs.

This script provides a command-line interface to list VPCs in the us-east-1 region,
generate Terraform configuration files for those VPCs, and delete specified VPCs.
It uses the Boto3 SDK (third-party) to interact with AWS EC2 APIs.

Example:
    python main.py list
    python main.py generate
"""
from typing import List, Dict
from utils.vpc_functions import list_vpcs, get_vpc_details
from utils.terraform_generator import generate_terraform_vpc
import boto3


def main() -> None:
    """Main function to orchestrate VPC listing and Terraform generation."""
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    
    # List VPCs
    vpc_ids = list_vpcs(ec2_client)
    print(f"Found VPCs: {vpc_ids}")
    
    # Get detailed VPC information
    vpcs_details = []
    for vpc_id in vpc_ids:
        details = get_vpc_details(ec2_client, vpc_id)
        vpcs_details.append(details)
    
    # Generate Terraform file
    generate_terraform_vpc(vpcs_details)
    
    print("Terraform file 'vpcs.tf' has been generated successfully.")

if __name__ == "__main__":
    main()
