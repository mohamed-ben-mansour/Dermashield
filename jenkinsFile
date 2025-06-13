pipeline:
  agent any

  environment:
    DOCKER_IMAGE_NAME: 'benmansourmohamed/django_app_health_devops'
    DEPLOY_DIR: '/mnt/c/Users/ASUS/Desktop/gl_version2.00'

  stages:
    - stage: Checkout Code
      steps:
        - echo 'Checking out code from GitHub...'
        - checkout scm

    - stage: Run Linters
      steps:
        - echo 'Running flake8, black, isort...'
        - sh 'flake8 .'
        - sh 'black --check .'
        - sh 'isort --check-only .'

    - stage: Run Tests with Coverage
      steps:
        - echo 'Running Django tests with pytest and coverage...'
        - sh 'coverage run -m pytest project_tests.py'
        - sh 'coverage report'

    - stage: Build Docker Image
      steps:
        - echo 'Building Docker image...'
        - sh 'docker build -t $DOCKER_IMAGE_NAME:latest .'

    - stage: Push to Docker Hub
      steps:
        - withCredentials([usernamePassword(credentialsId: 'Docker-Hub-credentials-for-Jenkins', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USERNAME')]) {
            sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin'
            sh 'docker push $DOCKER_IMAGE_NAME:latest'
          }

    - stage: Deploy to VPS
      steps:
        - echo 'Connecting to VPS and deploying...'
        - sshagent (credentials: ['WSLVPSSSHKey']) {
            sh 'ssh -o StrictHostKeyChecking=no mohamed@your.vps.ip.address "cd $DEPLOY_DIR && docker-compose pull && docker-compose up -d"'
          }
