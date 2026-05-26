pipeline {

    agent any

    stages {

        stage('Verify Environment') {
            steps {

                sh 'pwd'
                sh 'ls -la'

                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh 'docker compose down || true'
            }
        }

        stage('Build Containers') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh 'docker ps'
            }
        }

    }

    post {

        success {
            echo 'deployment successful'
        }

        failure {
            echo 'deployment failed'
        }

    }
}