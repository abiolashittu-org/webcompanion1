pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('5f8b634a-148a-4067-b996-07b4b3276fba')
        NVDAPIKEY = credentials('ed62b912-6db4-4d3a-a445-a1799077253e')
        SCANNER_HOME = tool 'sonar-scanner'
        DOCKERHUB_USERNAME = 'shittuay'
        DEPLOYMENT_NAME = 'webcompanion'
        IMAGE_TAG = "v.0.${env.BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${DEPLOYMENT_NAME}:${IMAGE_TAG}"
        NAMESPACE = 'webcompanion'
        BRANCH_NAME = "${GIT_BRANCH.split('/')[1]}"
    }

    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/dev'], [name: '*/qa'], [name: '*/prod']], userRemoteConfigs: [[url: 'https://github.com/abiolashittu-org/webcompanion1.git']]])
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=webcompanion -Dsonar.projectName=webcompanion"
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        waitForQualityGate abortPipeline: false, credentialsId: 'sonar-token'
                    }
                }
            }
        }
        stage('Pytest') {
            steps {
                script {
                    sh "python3 -m venv venv"
                    sh "source venv/bin/activate"
                    sh "pip install -r requirements.txt --no-cache-dir"
                    sh "pip install pytest pytest-flask"
                    sh "pytest"
                }
            }
        }
        stage('OWASP') {
            steps {
                dependencyCheck additionalArguments: "--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey ${env.NVDAPIKEY}", odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                script {
                    sh "trivy fs ."
                }
            }
        }
        stage("Login to DockerHub") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Successful"
            }
        }
        stage("Docker Build") {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME --build-arg EMAIL=$EMAIL --build-arg SMTP_SERVER=$SMTP_SERVER --build-arg PORT=$PORT --build-arg SMTP_SERVER_PASS=$SMTP_SERVER_PASS ."
                    echo "Image built successfully"
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $IMAGE_NAME"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $IMAGE_NAME"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    dir('./k8s') {
                        kubeconfig(credentialsId: '3f12ff7b-93cb-4ea5-bc21-79bcf5fb1925', serverUrl: '') {
                            if (env.BRANCH_NAME == 'dev') {
                                sh "sed -i 's/IMAGE_TAG/${env.IMAGE_TAG}/g' overlays/dev/kustomization.yaml"
                                sh "kustomize build overlays/dev | kubectl apply -f -"
                                slackSend channel: '#alerts', color: 'good', message: "Webcompanion with tag ${env.IMAGE_TAG} deployed to dev"
                            } else if (env.BRANCH_NAME == 'qa') {
                                sh "sed -i 's/IMAGE_TAG/${env.IMAGE_TAG}/g' overlays/qa/kustomization.yaml"
                                sh "kustomize build overlays/qa | kubectl apply -f -"
                                slackSend channel: '#alerts', color: 'good', message: "Webcompanion with tag ${env.IMAGE_TAG} deployed to qa"
                            } else if (env.BRANCH_NAME == 'prod') {
                                sh "sed -i 's/IMAGE_TAG/${env.IMAGE_TAG}/g' overlays/prod/kustomization.yaml"
                                sh "kustomize build overlays/prod | kubectl apply -f -"
                                slackSend channel: '#alerts', color: 'good', message: "Webcompanion with tag ${env.IMAGE_TAG} deployed to prod"
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            slackSend channel: '#alerts', color: 'good', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
        failure {
            slackSend channel: '#alerts', color: 'danger', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
        always {
            cleanWs()
        }
    }
}
