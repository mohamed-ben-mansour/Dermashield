pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'benmansourmohamed/django_app_health_devops'
        VPS_IP            = '172.21.3.34'
        DEPLOY_DIR        = '/home/mohamed/gl_version2.00' // Correct VPS Linux path
        SSH_USER = 'mohamed'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image (this installs requirements.txt)'
                bat "docker build -t %DOCKER_IMAGE_NAME%:%BUILD_NUMBER% ."
            }
        }


    

        stage('Run Unit Tests') {
            steps {
                echo 'Running tests inside Docker Compose environment'
                bat 'docker-compose run --rm web sh -c "coverage run -m pytest forum/tests/test_views.py feedback/tests/test_views.py && coverage report"'
            }
        }




        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Docker-Hub-credentials-for-Jenkins',
                    usernameVariable: 'DOCKER_HUB_USERNAME',
                    passwordVariable: 'DOCKER_HUB_PASSWORD'
                )]) {
                    bat 'echo %DOCKER_HUB_PASSWORD% | docker login -u %DOCKER_HUB_USERNAME% --password-stdin'
                    bat "docker push %DOCKER_IMAGE_NAME%:%BUILD_NUMBER%"
                }
            }
        }
        stage('Deploy to VPS') {
            steps {
                echo 'Deploying to VPS (via WSL SSH)'
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'WSLVPSSSHKey',
                    keyFileVariable: 'SSH_KEY_PATH',
                    usernameVariable: 'SSH_USER'
                )]) {
                    bat """
                    wsl ssh -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no ${SSH_USER}@${VPS_IP} "cd ${DEPLOY_DIR} && docker-compose pull && docker-compose up -d"
                    """
                }
            }
        }
    }
        post {
            always {
                echo 'Cleaning workspace'
                cleanWs()
            }
        }
}
