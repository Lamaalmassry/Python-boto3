import boto3
import json
from botocore.exceptions import ClientError
from datetime import datetime

def get_vpc_details(ec2_client):
    """Fetch all VPC details in the specified region."""
    try:
        response = ec2_client.describe_vpcs()
        vpcs = response['Vpcs']
        vpc_details = []
        for vpc in vpcs:
            vpc_info = {
                'VPCId': vpc.get('VpcId', ''),
                'CidrBlock': vpc.get('CidrBlock', ''),
                'State': vpc.get('State', ''),
                'IsDefault': vpc.get('IsDefault', False),
                'Tags': {tag['Key']: tag['Value'] for tag in vpc.get('Tags', [])},
            }
            vpc_details.append(vpc_info)
        return vpc_details
    except ClientError as e:
        print(f"Error fetching VPC details: {e}")
        return []




def get_ec2_details(ec2_client):
    """Fetch all EC2 instance details in the specified region."""
    try:
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_info = {
                    'InstanceId': instance.get('InstanceId', ''),
                    'InstanceType': instance.get('InstanceType', ''),
                    'State': instance.get('State', {}).get('Name', ''),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', ''),
                    'PublicIpAddress': instance.get('PublicIpAddress', ''),
                    'LaunchTime': instance.get('LaunchTime', '').isoformat() if instance.get('LaunchTime') else '',
                    'VPCId': instance.get('VpcId', ''),
                    'SubnetId': instance.get('SubnetId', ''),
                    'Tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                    'ImageId': instance.get('ImageId', ''),
                    'KeyName': instance.get('KeyName', '')
                }
                instances.append(instance_info)
        return instances
    except ClientError as e:
        print(f"Error fetching EC2 details: {e}")
        return []

def save_to_json(data, filename):
    """Save data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def main():
    # Initialize Boto3 EC2 client for us-east-1 region
    try:
        ec2_client = boto3.client('ec2', region_name='us-east-1')
    except Exception as e:
        print(f"Error initializing Boto3 client: {e}")
        return

    # Fetch VPC details
    vpc_details = get_vpc_details(ec2_client)
    vpc_output = {
        'Timestamp': datetime.utcnow().isoformat(),
        'Region': 'us-east-1',
        'VPCs': vpc_details
    }
    save_to_json(vpc_output, 'vpc_details_us-east-1.json')

    # Fetch EC2 details
    ec2_details = get_ec2_details(ec2_client)
    ec2_output = {
        'Timestamp': datetime.utcnow().isoformat(),
        'Region': 'us-east-1',
        'EC2Instances': ec2_details
    }
    save_to_json(ec2_output, 'ec2_details_us-east-1.json')

if __name__ == "__main__":
    main()