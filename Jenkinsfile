pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'benmansourmohamed/django_app_health_devops'
        DEPLOY_DIR        = '/mnt/c/Users/ASUS/Desktop/gl_version2.00'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Run Linters') {
            steps {
                echo 'Running linters...'
                bat 'wsl flake8 .'
                bat 'wsl black --check .'
                bat 'wsl isort --check-only .'
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                echo 'Running Django tests with pytest and coverage...'
                bat 'wsl coverage run -m pytest tests/'
                bat 'wsl coverage report'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat "wsl docker build -t ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Docker-Hub-credentials-for-Jenkins',
                    usernameVariable: 'DOCKER_HUB_USERNAME',
                    passwordVariable: 'DOCKER_HUB_PASSWORD'
                )]) {
                    bat 'wsl echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin'
                    bat "wsl docker push ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy to VPS') {
            steps {
                echo 'Deploying to WSL2 VPS...'
                sshagent(credentials: ['WSLVPSSSHKey']) {
                    bat """wsl ssh -o StrictHostKeyChecking=no mohamed@your.vps.ip.address \
"cd ${DEPLOY_DIR} && docker-compose pull && docker-compose up -d"
"""
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}
