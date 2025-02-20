pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/flask-app"
        AWS_REGION = 'us-west-2'
        KUBECTL_CONFIG = credentials('kubectl-config')
        SNYK_TOKEN = credentials('snyk-token')
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Security Scan - Code') {
            parallel {
                stage('SAST - SonarQube') {
                    steps {
                        sh '''
                            sonar-scanner \
                              -Dsonar.projectKey=flask-app \
                              -Dsonar.sources=. \
                              -Dsonar.host.url=http://sonarqube:9000 \
                              -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
                
                stage('Dependencies - Snyk') {
                    steps {
                        sh '''
                            cd app
                            snyk test --all-projects
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('app') {
                    sh 'pip install -r requirements.txt'
                    sh 'python -m pytest test_app.py'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Security Scan - Container') {
            steps {
                sh "trivy image ${DOCKER_IMAGE}:${BUILD_NUMBER}"
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${DOCKER_IMAGE}
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Security Scan - Infrastructure') {
            steps {
                sh '''
                    cd terraform
                    tfsec .
                    checkov -d .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        kubectl apply -f kubernetes/
                        kubectl set image deployment/flask-app flask-app=${DOCKER_IMAGE}:${BUILD_NUMBER}
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            // Send security scan reports to monitoring system
            sh 'send-security-reports.sh'
        }
        success {
            echo 'Pipeline succeeded! Application deployed successfully.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}
