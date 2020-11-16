pipeline {
    agent any

    stages {
        stage('Create virtualenv and installing dependencies') {
            steps {
                sh '''#!/bin/bash
                echo 'Creating Virtualenv..'
                /usr/local/bin/python3.8 -m venv venv
                source venv/bin/activate
                cd superlists && pip install -r requirements.txt
                '''
            }
        }
        stage('Unit tests') {
            steps {
                sh '''#!/bin/bash
                echo 'Running unit Tests..'
                source venv/bin/activate  && cd superlists && python manage.py test lists accounts
                '''
            }
        }
        stage('Functional tests') {
            steps {
                sh '''#!/bin/bash
                echo 'Running functional tests'
                source venv/bin/activate && cd superlists && python manage.py test functional_tests
                '''
            }
        }
    }
}