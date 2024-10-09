# Flask Application with AWS EC2 and S3 Integration

This is a Python Flask application that includes a script to create an AWS S3 bucket and an EC2 instance. Follow the instructions below to set up the virtual environment, install the necessary dependencies, and run the application.

## Prerequisites

- Python 3.x
- AWS account with access to create EC2 instances and S3 buckets
- AWS CLI configured on your local machine (for access keys)

## Setup Instructions

### 1. Set Up a Virtual Environment

To keep your environment clean and avoid conflicts between dependencies, set up a virtual environment:


# Create a virtual environment
python -m venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

### 2 .After activating the virtual environment, install the necessary dependencies from the requirements.txt file
pip install -r requirements.txt

### 3. Create a .env File. It should include following variables 
ImageId=<Your EC2 Image ID>
KeyName=<Your EC2 Key Pair Name>
SecurityGroup=<Your EC2 Security Group>
Region=<Your AWS Region>
BucketName=<Your S3 Bucket Name>
AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

### 4. Run create_instance.py Script
This script is used to create an AWS S3 bucket and an EC2 instance. Make sure the .env file is correctly configured, then run the script:

python create_instance.py

### 5. Run the Flask Application
After setting up the EC2 instance and S3 bucket, you can run the Flask application (app.py):

python app.py

