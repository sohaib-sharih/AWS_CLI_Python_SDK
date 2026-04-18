## Installation AWS Python SDK

1. Run the following cmd on Win Powershell
```
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

2. **Ref link to AWS docs**: [AWS Cli Installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. To login, run the following on Win Powershell

```
aws login
NOTE
If this does not log you in, or open up a browser to authenticate with your login credentials, then use a name of a profile that exists or create a new one

----
To create a new profile for your account:

aws login --profile <create a new name>

Then authenticate by entering you login credentials.
```

## Using Python SDK

1. Run the installation command for downloading Python AWS Cli SDK kit.

```
$ python -m venv .venv
...
$ . .venv/bin/activate

...

$ python -m pip install boto3
```

2. [Python SDK installation guide](https://github.com/boto/boto3)
3. [Python Libraries and list of SDKs](https://builder.aws.com/content/2zYQkMbmrsxHPtT89s3teyKJh79/aws-tools-and-resources-python)
4. [Python SDK doc](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html)
5. Example Code

```
main.py

import logging
import boto3
from botocore.exceptions import ClientError

# def create_bucket(bucket_name, region='us-east-1'):
#     """Create an S3 bucket in a specified region
#     If a region is not specified, the bucket is created in the S3 default
#     region (us-east-1).
#     :param bucket_name: Bucket to create
#     :param region: String region to create bucket in, e.g., 'us-west-2'
#     :return: True if bucket created, else False
#     """

#     # Create bucket
#     try:
#         bucket_config = {}
#         s3_client = boto3.client('s3', region_name=region)
#         if region != 'us-east-1':
#             bucket_config['CreateBucketConfiguration'] = {'LocationConstraint': region}
#         s3_client.create_bucket(Bucket=bucket_name, **bucket_config)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

# Retrieve the list of existing buckets

s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')

for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

```

6. Run the python main.py inside the virtual environment

```
python main.py

OUTPUT:

(.venv) PS D:\AWS_Cloud> python main.py
Existing buckets:
  s3-soby-test
  

```

7. **NOTE (LocationConstraint):** If you set the default location or your region is set to ***us-east-1***, you will have to ensure to use the ***LocationConstraint***. Any other location besides ***us-east-1*** will not require the locationConstraint code snippet.

***Fun Fact:***  S3 was AWS’s first service, created when there was only one region (**us-east-1**). Every other region added later was treated as a "constraint" on that original global system. **us-east-1** (N. Virginia) is the original, global default for S3.

#### Rules of using the LocationConstraint:

1. **The Role of the Endpoint**: When you write `s3_client = boto3.client('s3', region_name='us-east-2')`, you are telling the SDK to send the "create bucket" request specifically to the **Ohio (us-east-2)** endpoint.
2. **Endpoint Definition**: An endpoint is the specific web address (URL) where your request is sent. For S3, every region has its own endpoint (e.g., `s3.us-east-2.amazonaws.com`).
3. **ERRORS:** if the code returns an ***EMPTY ARG*** as the second parameter, technically, its not wrong, but it doesn't fulfill the requirement of completing an endpoint, *only in the case where your location or the region where you want to create an s3 bucket is any location besides us-east-1*.

```
s3_client.create_bucket(Bucket=bucket_name, **bucket_config)

NOTES
1. The **bucket_config unpacks the dictionary so it can use that value of region for s3_client to complete its endpoint definition.
2. It then provides it to AWS, if its in the right format, then it will approve of the request.
3. REMEMBER: The locationContraint code snippet is only used if you want to create a resource in any region BESIDES us-east-1.
```

#### The FIX for creating a bucket in us-east-1 Region

```
main.py

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

x = create_bucket("first-sharih-116", "us-east-1")

print(x)


# Retrieve the list of existing buckets

s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

  
# Debug region

print(boto3.Session().region_name)
print(boto3.client('s3').meta.region_name)

```

#### STEP BY STEP INFERENCING THE CODE

1. **`import logging` / `import boto3`**: Brings in tools for error reporting and the AWS SDK.
2. **`from botocore.exceptions import ClientError`**: Specifically imports the error type AWS throws when something goes wrong (like a name conflict).
3. **`def create_bucket(bucket_name, region='us-east-1'):`**: Defines your function. `region` defaults to 'us-east-1' if you don't provide it.
4. **`bucket_config = {}`**: Initializes an empty dictionary to hold settings for the bucket.
5. **`s3_client = boto3.client('s3', region_name=region)`**: Creates the "phone" that calls AWS. You tell it which region's "office" to talk to.
6. **`if region == 'us-east-1':`**: Your code currently checks if the region is the default.
7. **`bucket_config[...] = ...`**: Adds the location requirement to your dictionary.
8. **`s3_client.create_bucket(Bucket=bucket_name, **bucket_config)`**: Sends the command to AWS with your settings.
9. **`except ClientError as e:`**: If AWS says "No," this catches the reason why and logs it.

#### Misconception about AWS CLI Region Setting

1. You don't have to set your AWS Default region while running this SDK because you have several options:
	a. You can explicitly define the region you want to create your bucket. `s3_client = boto3.client('s3', region_name='us-east-2`
	b. Define a default Parameter Value in the def function statement. `def create_bucket(bucket_name, region='us-east-1'):`
	c. Provide a 2nd argument in the **function call** `create_bucket("first-sharih-116", "us-east-2")`
2. You need to define it in the code.
#### Configuring your AWS CLI

1. If you have the [AWS CLI](http://aws.amazon.com/cli/) installed, then you can use the **aws configure** command to configure your credentials file:
```
aws configure
```

2. Alternatively, you can create the credentials file yourself. By default, its location is `~/.aws/credentials`. At a minimum, the credentials file should specify the access key and secret access key. In this example, the key and secret key for the account are specified in the `default` profile:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

3. 
#### Useful links

1. [AWS Developer Tools](https://builder.aws.com/build/tools)
2. [AWS Documentation](https://docs.aws.amazon.com/)


#### Useful commands

1. To list profiles
```
aws configure list-profiles
```

2. Check environment variables

```
echo $env:AWS_REGION
echo $env:AWS_DEFAULT_REGION
echo $env:AWS_S3_ENDPOINT

NOTE: Old cached environment variable, if the code block returns an error for invalid location, then you can check if these have a different location value.

To change their values(Powershell)

TEMPORARY
$env:AWS_REGION="us-east-1"
$env:AWS_DEFAULT_REGION="us-east-1"

PERMANENT change

setx AWS_REGION "us-east-1"
setx AWS_DEFAULT_REGION "us-east-1"
```
3. List Buckets

```
aws s3 ls
```

4. Check your current AWS CLI region

```
aws configure list

aws configure get region

```

5. Setting your AWS CLI region

```
aws configure set region us-east-2


To revert back to **us-east-1**, simply run:

aws configure set region us-east-1

```