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
        withCredentials([sshUserPrivateKey(credentialsId: 'ec2-key', keyFileVariable: 'KEY')]) {
            bat """
                echo Fixing key permissions on Windows...
                
                REM Step 1: Remove all inherited permissions from the key file.
                icacls "%KEY%" /inheritance:r

                REM Step 2: Remove permissions for the "BUILTIN\\Users" group, as requested by the error log.
                icacls "%KEY%" /remove "BUILTIN\\Users"

                echo Deploying to EC2...
                ssh -i "%KEY%" -o StrictHostKeyChecking=no %EC2_HOST% "docker pull %DOCKER_IMAGE% && docker stop flask-app || true && docker rm flask-app || true && docker run -d --name flask-app -p 80:5000 %DOCKER_IMAGE%"
            """
        }
    }
} 
   }
}
