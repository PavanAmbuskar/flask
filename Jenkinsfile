pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "pavanambuskar/flask-k8s"
        EC2_HOST = "ubuntu@13.221.232.109"
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
                script {
                    sshagent(['ec2-key']) {
                        bat """
                            echo Deploying to EC2...
                            ssh -o StrictHostKeyChecking=no %EC2_HOST% "docker pull %DOCKER_IMAGE% && docker stop flask-app || true && docker rm flask-app || true && docker run -d --name flask-app -p 80:5000 %DOCKER_IMAGE%"
                        """
                    }
                }
            }
        }
    }
}
