pipeline {
  agent any

  stages {
    stage('Construcao') {
      steps {
        sh 'pip intall -r requirements.txt'
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