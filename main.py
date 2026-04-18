import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region='us-east-1'):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    # try:
    #     bucket_config = {}
    #     s3_client = boto3.client('s3', region_name=region)
    #     if region == 'us-east-1':
    #         bucket_config['CreateBucketConfiguration'] = {'LocationConstraint': region}
    #     # else:
    #     s3_client.create_bucket(Bucket=bucket_name, **bucket_config)
    #         # Add the following line instead:
    #         # s3_client.create_bucket(Bucket=bucket_name)
            
    # Fixed
    # If no region, use the session default (your us-east-1)
    if region is None:
        s3_client = boto3.client('s3')
    else:
        s3_client = boto3.client('s3', region_name=region)

    try:
        bucket_config = {}
        # ONLY add LocationConstraint if it is NOT us-east-1
        if region is not None and region != 'us-east-1':
            bucket_config['CreateBucketConfiguration'] = {'LocationConstraint': region}
        
        s3_client.create_bucket(Bucket=bucket_name, **bucket_config)
            
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Add this line to run the above function and hardcode a name of a bucket

x = create_bucket("second-sharih-116", "us-east-1")
print(x)

# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

# Debug region

print(boto3.Session().region_name)

print(boto3.client('s3').meta.region_name)