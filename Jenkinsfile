pipeline {

    agent any

    environment {
        IMAGE_NAME = "harshhh21/week9-cicd"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "week9-app"
        APP_PORT = "5000"
        DEPLOY_STATE = "${WORKSPACE}/.last_successful_build"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Creating Python virtual environment and installing dependencies'

                sh '''
                    python3 -m venv venv
                    ./venv/bin/python -m pip install --upgrade pip
                    ./venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests'

                sh '''
                    ./venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image'

                sh """
                    docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} \
                    -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Docker Push') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh """
                        echo "\$DOCKER_PASSWORD" | docker login \
                        -u "\$DOCKER_USERNAME" \
                        --password-stdin

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest

                        docker logout
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                script {

                    sh '''
                        if [ -f "$DEPLOY_STATE" ]; then
                            cp "$DEPLOY_STATE" "$WORKSPACE/.previous_build"
                        else
                            echo "" > "$WORKSPACE/.previous_build"
                        fi
                    '''

                    sh """
                        docker rm -f ${CONTAINER_NAME} || true

                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${APP_PORT}:5000 \
                            -e APP_VERSION=${IMAGE_TAG} \
                            ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                script {

                    def healthResult = sh(
                        script: """
                            sleep 5
                            curl --fail --silent http://localhost:${APP_PORT}/health
                        """,
                        returnStatus: true
                    )

                    if (healthResult != 0) {
                        error("Health check failed")
                    }

                    echo "Health check passed for version ${IMAGE_TAG}"
                }
            }
        }

        stage('Record Successful Deployment') {
            steps {
                sh '''
                    echo "$IMAGE_TAG" > "$DEPLOY_STATE"
                    echo "Recorded successful deployment: $IMAGE_TAG"
                '''
            }
        }
    }

    post {

        failure {
            script {

                echo 'Pipeline failed. Checking whether rollback is possible.'

                def previousBuild = ''

                if (fileExists('.previous_build')) {
                    previousBuild = readFile('.previous_build').trim()
                }

                if (previousBuild) {

                    echo "Rolling back to previous successful version: ${previousBuild}"

                    sh """
                        docker rm -f ${CONTAINER_NAME} || true

                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${APP_PORT}:5000 \
                            -e APP_VERSION=${previousBuild} \
                            ${IMAGE_NAME}:${previousBuild}
                    """

                    sh """
                        sleep 5
                        curl --fail --silent http://localhost:${APP_PORT}/health
                    """

                    echo "Rollback completed successfully to version ${previousBuild}"

                } else {

                    echo 'No previous successful deployment found. Rollback skipped.'
                }
            }
        }

        success {
            echo 'CI/CD pipeline completed successfully.'
        }
    }
}
