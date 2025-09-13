pipeline {
  agent any

  environment {
    DB_DOCKER_IMAGE = "marcoz/trab-devops-db:${env.BUILD_NUMBER}"
    WEB_DOCKER_IMAGE = "marcoz/trab-devops-web:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Construcao Web') {
      steps {
        dir('web') {
          sh 'python3 -m venv venv' 
          sh 'source venv/bin/activate && pip install -r requirements.txt'
          sh 'source venv/bin/activate && pytest'
          sh "/usr/local/bin/docker buildx build -f Dockerfile.web -t ${WEB_DOCKER_IMAGE} ."
        }
      }
    }

    stage('Construcao DB') {
      steps {
        dir('db') {
          sh "/usr/local/bin/docker buildx build -f Dockerfile.mysql -t ${DB_DOCKER_IMAGE} ."
        }
      }
    }

    stage('Entrega') {
      steps {
        dir('web') {
          script {
              withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                  sh "echo \"$DOCKER_PASSWORD\" | /usr/local/bin/docker login -u \"$DOCKER_USERNAME\" --password-stdin && /usr/local/bin/docker push ${WEB_DOCKER_IMAGE}"
              }
          }
        }
      }
    }

    stage('Cleanup') {
      steps {
        echo 'Fazendo cleanup'
      }
    }
  }
}