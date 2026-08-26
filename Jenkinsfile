pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building application'
                sh 'python3 app.py'
            }
        }

        stage('Test') {
            steps {
                echo 'Running application tests'
                sh 'python3 -m pytest'
            }
        }

        stage('Validation') {
            steps {
                echo 'Validating Python syntax'
                sh 'python3 -m py_compile app.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed. Check Console Output'
        }
    }
}
