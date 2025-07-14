import boto3

# AWS credentials should already be configured (via ~/.aws/credentials or env vars)
ec2 = boto3.resource('ec2', region_name='us-east-1')

# User data script to install Docker on Amazon Linux 2
user_data_script = '''#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
systemctl enable docker
usermod -a -G docker ec2-user
'''

# Launch EC2 instance
instances = ec2.create_instances(
    ImageId='ami-0c02fb55956c7d316',       # Amazon Linux 2 (us-east-1)
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-server',                   #  Ensure this key pair exists in us-east-1
    SecurityGroupIds=['sg-04e73bbda715725b5'],  #  Must allow SSH (port 22) and optional port 8080/80 if needed
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'jenkins-ec2-instance'}]
        }
    ]
)

# Wait for instance to be running (optional but helpful)
instances[0].wait_until_running()

# Refresh attributes to get public IP
instances[0].reload()

print(f"Launched EC2 Instance ID: {instances[0].id}")
print(f"Public IP: {instances[0].public_ip_address}")
