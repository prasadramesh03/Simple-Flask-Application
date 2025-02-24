// Jenkinsfile
def qualityGate = load 'pipeline/quality-gates.groovy'

pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'your-registry/flask-app'
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Code Quality') {
            steps {
                script {
                    def qualityCheck = qualityGate.check()
                    if (!qualityCheck) {
                        error "Quality gate failed"
                    }
                }
                sh 'pylint app/'
                sh 'pytest app/tests/'
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'trivy image $DOCKER_IMAGE:$BUILD_NUMBER'
                sh 'snyk test'
            }
        }
        
        stage('Build & Push') {
            steps {
                sh """
                    docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .
                    docker push $DOCKER_IMAGE:$BUILD_NUMBER
                """
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh """
                    kubectl apply -f kubernetes/deployments/staging/
                    kubectl set image deployment/flask-app \
                    flask-app=$DOCKER_IMAGE:$BUILD_NUMBER -n staging
                """
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh 'pytest integration_tests/'
            }
        }
        
        stage('Production Approval') {
            steps {
                timeout(time: 24, unit: 'HOURS') {
                    input message: 'Approve deployment to production?'
                }
            }
        }
        
        stage('Deploy to Production') {
            steps {
                sh """
                    kubectl apply -f kubernetes/deployments/production/
                    kubectl set image deployment/flask-app \
                    flask-app=$DOCKER_IMAGE:$BUILD_NUMBER -n production
                """
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#deployments',
                      color: 'good',
                      message: "Deployment successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#deployments',
                      color: 'danger',
                      message: "Deployment failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
    }
}
