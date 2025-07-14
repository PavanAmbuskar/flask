pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        PYTHON_SCRIPT = 'launch_ec2.py'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/PavanAmbuskar/flask.git'
            }
        }

        stage('Install boto3') {
            steps {
bat '"C:\\Users\\<your-user>\\AppData\\Local\\Programs\\Python\\Python3x\\python.exe" -m pip install boto3'
bat '"C:\\Users\\<your-user>\\AppData\\Local\\Programs\\Python\\Python3x\\python.exe" %PYTHON_SCRIPT%'
            }
        }

        stage('Run EC2 Script') {
            steps {
                bat "python %PYTHON_SCRIPT%"
            }
        }
    }
}
