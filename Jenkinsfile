pipeline {
    agent any
    environment {
        DJANGO_SETTINGS_MODULE = 'superlists.settings.test'
        SECRET_KEY = 'UToroo1cu3jaemi9eewo6shoohohchah4Esa7Ietin1Faishi9'
    }
    stages {
        stage('Create virtualenv and installing dependencies') {
            steps {
                sh '''#!/bin/bash
                echo 'Creating Virtualenv..'
                /usr/local/bin/python3.8 -m venv venv
                source venv/bin/activate
                cd superlists && pip install -r requirements_test.txt
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