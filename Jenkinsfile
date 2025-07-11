// pipeline {
//     agent any

//     environment {
//         DOCKER_IMAGE = "pavanambuskar/flask-k8s"
//         EC2_HOST = "ubuntu@13.221.232.109"
//     }

//     stages {
//         stage('Clone Code') {
//             steps {
//                 git 'https://github.com/PavanAmbuskar/flask.git'
//             }
//         }

//         stage('Docker Build') {
//             steps {
//                 bat "docker build -t %DOCKER_IMAGE% ."
//             }
//         }

//         stage('Docker Push') {
//             steps {
//                 withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
//                     bat '''
//                         echo Logging in to DockerHub...
//                         docker login -u %DOCKER_USER% -p %DOCKER_PASS%
//                         docker push %DOCKER_IMAGE%
//                     '''
//                 }
//             }
//         }

// stage('Deploy to EC2') {
// stages {
// stage('Deploy') {
// steps {
// bat '''
// ssh -i C:\\Users\\Dell\\.ssh\\my-server.pem -o StrictHostKeyChecking=no ubuntu@13.221.232.109 ^
// "docker pull pavanambuskar/flask-k8s && docker stop flask-app || true && docker rm flask-app || true && docker run -d --name flask-app -p 80:5000 pavanambuskar/flask-k8s"
// '''
//                     }
//                 }
//             }   
//         }
//     }
// }

// Make sure you have defined these variables, perhaps in an environment block
environment {
    EC2_HOST = 'ubuntu@13.221.232.109'
    DOCKER_IMAGE = 'pavanambuskar/flask-k8s'
}stage('Deploy to EC2') {
    steps {
        // 'ec2-key' is the ID of your "SSH Username with private key" credential in Jenkins
        sshagent(credentials: ['ec2-key']) {
            // Because this is a Windows agent, we use 'bat'
            bat '''
                echo "Connecting to EC2 host..."               
                REM No need to specify the key with -i. The SSH Agent handles it automatically.
                ssh -o StrictHostKeyChecking=no ubuntu@13.221.232.109 "hostname && uptime"
            
                echo "Pulling new Docker image and restarting container..."
                ssh -o StrictHostKeyChecking=no ubuntu@13.221.232.109 "docker pull pavanambuskar/flask-k8s && docker stop flask-app || true && docker rm flask-app || true && docker run -d --name flask-app -p 80:5000 pavanambuskar/flask-k8s"
            '''
        }
    }
}