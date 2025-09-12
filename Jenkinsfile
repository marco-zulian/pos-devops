pipeline {
  agent any

  stages {
    stage('Construcao') {
      steps {
        dir('web') {
          sh 'python3 -m venv venv' 
          sh 'source venv/bin/activate && pip install -r requirements.txt'
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