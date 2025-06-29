from typing import List, Dict
import boto3

def list_ec2_instances(session: boto3.Session) -> List[Dict]:
    """Fetch all EC2 instances in the region."""
    client = session.client("ec2")
    response = client.describe_instances()
    instances = []
    for reservation in response["Reservations"]:
        instances.extend(reservation["Instances"])
    return instances

def generate_ec2_terraform(instances: List[Dict]) -> str:
    """Generate Terraform code for EC2 instances."""
    tf_code = ""
    for instance in instances:
        name = next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"), instance["InstanceId"])
        tf_code += f"""
resource "aws_instance" "ec2_{instance['InstanceId']}" {{
  ami = "{instance['ImageId']}"
  instance_type = "{instance['InstanceType']}"
  subnet_id = "{instance.get('SubnetId', '')}"
  tags = {{
    Name = "{name}"
  }}
}}
"""
    return tf_code