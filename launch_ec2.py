import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

user_data_script = """#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
yum install -y git
service docker start
systemctl enable docker
usermod -aG docker ec2-user

cd /home/ec2-user
git clone https://github.com/PavanAmbuskar/flask.git
cd flask

docker build -t flask-app-3 .
docker run -d -p 5000:5000 --name my-flask-container flask-app-3
"""

instances = ec2.create_instances(
    ImageId='ami-020cba7c55df1f615',  # ✅ Amazon Linux 2 AMI
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-server',
    SecurityGroupIds=['sg-04e73bbda715725b5'],
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'jenkins-ec2-instance'}]
        }
    ]
)

instances[0].wait_until_running()
instances[0].reload()

print(f"Launched EC2 Instance ID: {instances[0].id}")
print(f"Public IP: {instances[0].public_ip_address}")
