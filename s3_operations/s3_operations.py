import boto3
import botocore
import uuid
import os
from botocore.exceptions import ClientError
from datetime import datetime

# Initialize S3 resource and client
s3_resource = boto3.resource('s3', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

def list_buckets():
    """List all S3 buckets in us-east-1 using resource call."""
    try:
        print("Listing all buckets in us-east-1:")
        buckets = s3_resource.buckets.all()
        bucket_list = [bucket.name for bucket in buckets]
        if not bucket_list:
            print("No buckets found.")
            return None
        for bucket in bucket_list:
            print(f" - {bucket}")
        return bucket_list
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return None

def create_dummy_file(file_path):
    """Create a dummy text file with timestamp."""
    try:
        with open(file_path, 'w') as f:
            f.write(f"Dummy file created at {datetime.now().isoformat()}")
        print(f"Created dummy file: {file_path}")
        return True
    except IOError as e:
        print(f"Error creating dummy file: {e}")
        return False

def read_local_file(file_path):
    """Read and print the contents of a local file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"\nContents of {file_path}:")
        print(content)
        return content
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def upload_file(bucket_name, file_path, object_key):
    """Upload a file to an S3 bucket using resource call."""
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.upload_file(Filename=file_path, Key=object_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{object_key}")
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False

def download_file(bucket_name, object_key, download_path):
    """Download a file from an S3 bucket using resource call."""
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.download_file(Key=object_key, Filename=download_path)
        print(f"Downloaded s3://{bucket_name}/{object_key} to {download_path}")
        return True
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False

def wait_for_object(bucket_name, object_key):
    """Use waiter to check if object exists with 10s delay and 10 attempts."""
    try:
        waiter = s3_client.get_waiter('object_exists')
        waiter.wait(
            Bucket=bucket_name,
            Key=object_key,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 10
            }
        )
        print(f"Object s3://{bucket_name}/{object_key} exists.")
        return True
    except botocore.exceptions.WaiterError as e:
        print(f"Waiter error: {e}")
        return False

def list_objects_paginator(bucket_name):
    """List objects in a bucket using ListObjectsV2 paginator."""
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        print(f"Objects in s3://{bucket_name}:")
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    print(f" - {obj['Key']} (Size: {obj['Size']} bytes)")
            else:
                print("No objects found in bucket.")
    except ClientError as e:
        print(f"Error listing objects: {e}")

def main():
    """Main function to orchestrate S3 operations."""
    # List buckets
    bucket_list = list_buckets()
    if not bucket_list:
        print("No buckets available. Exiting.")
        return

    # Select a random bucket (first one for simplicity)
    target_bucket = bucket_list[0]
    print(f"Selected bucket: {target_bucket}")

    # Create and manage dummy file
    dummy_file = f"dummy_{uuid.uuid4().hex}.txt"
    object_key = f"test/{dummy_file}"
    download_path = f"downloaded_{dummy_file}"

    if not create_dummy_file(dummy_file):
        print("Failed to create dummy file. Exiting.")
        return

    # Read the dummy file contents
    read_local_file(dummy_file)

    try:
        # Upload file
        if not upload_file(target_bucket, dummy_file, object_key):
            print("Upload failed. Exiting.")
            return

        # Download file
        if not download_file(target_bucket, object_key, download_path):
            print("Download failed. Exiting.")
            return

        # Read the downloaded file contents
        read_local_file(download_path)

        # Wait for object existence
        if not wait_for_object(target_bucket, object_key):
            print("Object verification failed. Exiting.")
            return

        # List objects using paginator
        list_objects_paginator(target_bucket)

        # Pause for manual inspection
        input("\nPress Enter to clean up local files and exit...")

    finally:
        # Clean up local files
        for file in [dummy_file, download_path]:
            if os.path.exists(file):
                os.remove(file)
                print(f"Cleaned up local file: {file}")

if __name__ == "__main__":
    main()