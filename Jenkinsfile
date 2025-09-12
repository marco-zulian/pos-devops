pipeline {
  agent any {
    stages {
      stage('Checkout') {
        steps {
          echo 'Pulling code from remote repo'
          checkout scm
          echo 'Code checkout complete!'
        }
      }
    }
  }
}