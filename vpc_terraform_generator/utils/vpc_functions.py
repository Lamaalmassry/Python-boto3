from typing import List, Dict
import boto3

def list_vpcs(ec2_client: boto3.client) -> List[str]:
    """
    List all VPC IDs in the us-east-1 region.
    
    Args:
        ec2_client: Boto3 EC2 client instance
        
    Returns:
        List of VPC IDs
    """
    response = ec2_client.describe_vpcs()
    return [vpc['VpcId'] for vpc in response['Vpcs']]

def get_vpc_details(ec2_client: boto3.client, vpc_id: str) -> Dict:
    """
    Get detailed information for a specific VPC.
    
    Args:
        ec2_client: Boto3 EC2 client instance
        vpc_id: ID of the VPC to fetch details for
        
    Returns:
        Dictionary containing VPC details
    """
    response = ec2_client.describe_vpcs(VpcIds=[vpc_id])
    vpc = response['Vpcs'][0]
    
    return {
        'id': vpc['VpcId'],
        'cidr_block': vpc['CidrBlock'],
        'name': next((tag['Value'] for tag in vpc.get('Tags', []) if tag['Key'] == 'Name'), vpc['VpcId']),
        'is_default': vpc.get('IsDefault', False)
    }