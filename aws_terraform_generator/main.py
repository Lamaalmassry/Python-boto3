import argparse
import boto3
from utils.vpc_functions import list_vpcs, generate_vpc_terraform
from utils.ec2_functions import list_ec2_instances, generate_ec2_terraform

def parse_arguments():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Generate Terraform from AWS resources")
    parser.add_argument("--region", required=True, help="AWS region (e.g., us-east-1)")
    parser.add_argument("--output", default="output.tf", help="Output Terraform file")
    return parser.parse_args()

def main():
    """Fetch AWS resources and generate Terraform code."""
    args = parse_arguments()
    session = boto3.Session(region_name=args.region)
    
    vpcs = list_vpcs(session)
    ec2_instances = list_ec2_instances(session)
    
    assert vpcs is not None, "No VPCs fetched"
    assert ec2_instances is not None, "No EC2 instances fetched"
    
    terraform_code = "# Auto-generated Terraform\n\n"
    terraform_code += generate_vpc_terraform(vpcs)
    terraform_code += generate_ec2_terraform(ec2_instances)
    
    with open(args.output, "w") as f:
        f.write(terraform_code)
    print(f"Terraform file saved to {args.output}")

if __name__ == "__main__":
    main()