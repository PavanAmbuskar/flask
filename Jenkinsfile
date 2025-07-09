pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "yourdockerhubusername/flask-app"
        EC2_HOST = "ec2-user@YOUR.EC2.IP.ADDRESS"
    }

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/yourgithubusername/flask-app.git'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Docker Push') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-creds', url: '']) {
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_HOST '
                        docker pull $DOCKER_IMAGE &&
                        docker stop flask-app || true &&
                        docker rm flask-app || true &&
                        docker run -d --name flask-app -p 80:5000 $DOCKER_IMAGE
                    '
                    """
                }
            }
        }
    }
}
