# Python-boto3

A collection of Python-based tools for AWS cloud automation and resource management.

## Introduction

 This repository for Python scripts designed to streamline AWS cloud operation, this project aims to provide modular, reusable tools for tasks like resource inventory, automation, and monitoring. Our first tool fetches VPC and EC2 details in AWS `us-east-1`, saving them as JSON files. More tools will be added to tackle various cloud challenges.

Whether you're a cloud engineer, DevOps professional, or enthusiast, this repo offers practical solutions for AWS management.

## Current Tools

### Python-boto3 repo
- **Description**: A Python script using Boto3 to fetch aws services details in our AWS account.
- **Features**:
  - Retrieves aws services like ec2 , vpc ... and thier details
  - Saves output to separate JSON files for example :`vpc_details_us-east-1.json` and `ec2_details_us-east-1.json`.
  - Includes robust error handling and modular design.
- **Use Case**: Ideal for cloud inventory, auditing, or monitoring AWS resources.

## Prerequisites

- Python 3.6 or higher
- AWS CLI and credentials configured (for AWS tools)
- Python libraries (e.g., Boto3: `pip install boto3`)
- Appropriate IAM permissions (specific to each tool’s AWS services)

## Installation

1. Clone the repository:
   ```bash   
   https://github.com/Lamaalmassry/Python-boto3.git