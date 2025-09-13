pipeline {
  agent any

  environment {
    DB_DOCKER_IMAGE = "marcoz/trab-devops-db:${env.BUILD_NUMBER}"
    WEB_DOCKER_IMAGE = "marcoz/trab-devops-web:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Construcao') {
      steps {
        dir('web') {
          sh 'python3 -m venv venv' 
          sh 'source venv/bin/activate && pip install -r requirements.txt'
          sh 'source venv/bin/activate && pytest'
          sh "/usr/local/bin/docker buildx build -f Dockerfile.web -t ${WEB_DOCKER_IMAGE} ."
        }
      }
    }

    stage('Entrega') {
      steps {
        echo 'Fazendo delivery'
      }
    }

    stage('Cleanup') {
      steps {
        echo 'Fazendo cleanup'
      }
    }
  }
}