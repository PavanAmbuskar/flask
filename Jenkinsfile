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
                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2-key', keyFileVariable: 'KEY')]) {
                        bat """
                            echo Deploying to EC2...
                            ssh -i %KEY% -o StrictHostKeyChecking=no ubuntu@44.210.122.166 "docker pull pavanambuskar/flask-k8s && docker stop flask-app || true && docker rm flask-app || true && docker run -d --name flask-app -p 80:5000 pavanambuskar/flask-k8s"
                        """
                      }
                }
            }
        }

       stage('Deploy to EC2') {
            steps {
                bat """
                        echo Deploying to EC2...
                        ssh -o StrictHostKeyChecking=no %EC2_HOST% ^
                        "docker pull %DOCKER_IMAGE% && ^
                        docker stop flask-app || true && ^
                        docker rm flask-app || true && ^
                        docker run -d --name flask-app -p 80:5000 %DOCKER_IMAGE%"
                    """
                }
            }

    }
}
