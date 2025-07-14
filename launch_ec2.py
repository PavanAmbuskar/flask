import boto3

# AWS credentials should already be configured (via IAM role or ~/.aws/credentials)
ec2 = boto3.resource('ec2', region_name='us-east-1')

# User data script to install Docker
user_data_script = '''#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
'''

# Launch EC2 instance
instance = ec2.create_instances(
    ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2 / Ubuntu AMI ID (depends on region)
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-server.pem',     # Replace with your actual key pair
    SecurityGroupIds=['sg-04e73bbda715725b5'], # Replace with your security group ID
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'jenkins-ec2-instance'}]
        }
    ]
)

print(f"Launched EC2 Instance ID: {instance[0].id}")
