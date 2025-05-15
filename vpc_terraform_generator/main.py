import boto3
from typing import List, Dict
from utils.vpc_functions import list_vpcs, get_vpc_details
from utils.terraform_generator import generate_terraform_vpc

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
