pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "pavanambuskar/flask-k8s"
        EC2_HOST = "ubuntu@44.210.122.166"
    }

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/PavanAmbuskar/flask.git'
            }
        }

        stage('Docker Build') {
            steps {
                bat "docker build -t %DOCKER_IMAGE% ."
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        echo Logging in to DockerHub...
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKER_IMAGE%
                    '''
                }
            }
        }

stage('Deploy to EC2') {
    steps {
        withCredentials([sshUserPrivateKey(credentialsId: 'ec2-key', keyFileVariable: 'KEY')]) {
            powershell """
                echo Fixing key permissions...
                icacls "$env:KEY" /inheritance:r
                icacls "$env:KEY" /grant:r "$env:USERNAME:F"
                echo Deploying to EC2...
                ssh -i "$env:KEY" -o StrictHostKeyChecking=no $env:EC2_HOST "docker pull $env:DOCKER_IMAGE && docker stop flask-app || true && docker rm flask-app || true && docker run -d --name flask-app -p 80:5000 $env:DOCKER_IMAGE"
            """
                    }
                }
            }
    }
}
