# VPC Terraform Generator

## Overview
This Python CLI tool uses AWS Boto3 SDK to list VPCs in the us-east-1 region and generate Terraform configuration files for those VPCs. The tool follows Python PEP standards and is structured with modular functions.

## Requirements
- Python 3.8+
- AWS CLI configured with appropriate credentials
- Boto3 (`pip install boto3`)
- AWS account with permissions to list VPCs

## Project Structure
```
vpc_terraform_generator/
  - main.py
  - utils/
      - vpc_functions.py
      - terraform_generator.py
  - README.md
```

## Installation
1. Clone the repository:
```bash
git clone <repository_url>
cd vpc_terraform_generator
```
2. Install dependencies:
```bash
pip install boto3
```
3. Configure AWS credentials using AWS CLI:
```bash
aws configure
```

## Usage
Run the main script:
```bash
python main.py
```

This will:
1. List all VPCs in us-east-1 region
2. Fetch detailed information for each VPC
3. Generate a `vpcs.tf` Terraform file in the current directory

## Output
The tool creates a `vpcs.tf` file containing Terraform configurations for all discovered VPCs, including:
- VPC ID
- CIDR block
- Name tag (if present)
- AWS provider configuration for us-east-1

## Development Standards
- Follows PEP 8 style guidelines
- Includes type hints and docstrings
- Modular function design with single responsibility
- Organized utility functions in `utils/` directory
- Uses Black and Pylint for code formatting and linting

## Recommended VSCode Extensions
- Python
- Pylint
- Black Formatter
- AWS Toolkit

