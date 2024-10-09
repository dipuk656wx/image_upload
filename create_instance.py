import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Get environment variables
ImageId = os.getenv('ImageId')
KeyName = os.getenv('KeyName')
SecurityGroup = os.getenv('SecurityGroup')
Region = os.getenv('Region')
BucketName = os.getenv('BucketName')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def create_session():
    """Create a session using the AWS credentials from environment variables."""
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=Region  # Specify the region here
    )
    return session

def create_s3_bucket(session, bucket_name, region=None):
    """Create an S3 bucket."""
    s3_client = session.client('s3')
    location = {'LocationConstraint': region} if region else None
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    print(f"S3 bucket '{bucket_name}' created successfully.")

def create_ec2_instance(session):
    """Create an EC2 instance."""
    ec2 = session.resource('ec2')
    instance = ec2.create_instances(
        ImageId=ImageId,  # Replace with your AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName=KeyName,
        SecurityGroups=[SecurityGroup]
    )
    print(f"EC2 instance '{instance[0].id}' created successfully.")

def main():
    # Create a session
    session = create_session()
    
    # Create S3 bucket
    # create_s3_bucket(session, BucketName, Region)  # Replace with your bucket name and region
    
    # Create EC2 instance
    create_ec2_instance(session)

if __name__ == '__main__':
    main()
