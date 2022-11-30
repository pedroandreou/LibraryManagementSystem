pipeline{
    agent any
    stages {
        stage('version') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('testing') {
            steps {
                sh 'virtualenv venv && . venv/bin/activate && pip install -r requirements.txt && python src/menu.py'
            }
        }
    }
}
