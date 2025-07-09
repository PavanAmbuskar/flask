pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "talhahamidsyed/flask"
        EC2_HOST = "ubuntu@16.171.136.221"
    }

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/syedtalhahamid/flask.git'
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
                        echo Logging into DockerHub...
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKER_IMAGE%
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['my-new-key-1']) {
                    bat '''
                        ssh -o StrictHostKeyChecking=no %EC2_HOST% ^
                        "docker pull %DOCKER_IMAGE% && ^
                        docker stop flask-app || true && ^
                        docker rm flask-app || true && ^
                        docker run -d --name flask-app -p 80:5000 %DOCKER_IMAGE%"
                    '''
                }
            }
        }
    }
}
