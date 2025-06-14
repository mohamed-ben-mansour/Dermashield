pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'benmansourmohamed/django_app_health_devops'
        VPS_IP            = '172.21.3.34'
        DEPLOY_DIR        = '/mnt/c/Users/ASUS/Desktop/gl_version2.00'
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
                bat "wsl docker build -t ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ."
            }
        }

          stage('Run Linters & Tests') {
              steps {
                  echo 'Running linters and tests inside container'
                  bat """
                  wsl docker run --rm \
                    -v \$(wslpath -a '%WORKSPACE%'):/app \
                    -w /app \
                    ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} \
                    sh -c "flake8 . && black --check . && isort --check-only . && coverage run -m pytest tests/ && coverage report"
                  """
              }
          }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Docker-Hub-credentials-for-Jenkins',
                    usernameVariable: 'DOCKER_HUB_USERNAME',
                    passwordVariable: 'DOCKER_HUB_PASSWORD'
                )]) {
                    bat 'wsl echo %DOCKER_HUB_PASSWORD% | docker login -u %DOCKER_HUB_USERNAME% --password-stdin'
                    bat "wsl docker push ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy to VPS') {
            steps {
                echo 'Deploying to VPS'
                sshagent(credentials: ['WSLVPSSSHKey']) {
                    bat """
                    wsl ssh -o StrictHostKeyChecking=no \
                      mohamed@${VPS_IP} \
                      \"cd ${DEPLOY_DIR} && docker-compose pull && docker-compose up -d\"
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
