pipeline {
    tools {
        dockerTool 'DEFAULT_DOCKER'
    }
    agent any

    environment {
        PROJECT_NAME = 'uk-weather-services'
        NEXUS_SERVICE_HOST = 'nexus-service'
        NEXUS_TRUSTED_HOST = 'nexus-service.saturn-cicd.svc.cluster.local'
        NEXUS_PORT = 8081
        NEXUS_URI = 'cicd/nexus/repository'
        PYTHON_HOSTED_URI = 'saturn-python-hosted'
        PYTHON_GROUP_URI = 'saturn-python-group'
        DEPENDENCY_TRACK_API_HOST = 'dependency-track-api-service'
        DEPENDENCY_TRACK_API_PORT = 8080
    }

    stages {

        stage('1. Setup Python 3.14 (Non-root)') {
            steps {
                sh '''
                    if [ ! -f "$WORKSPACE/python-local/python/bin/python3.14" ]; then
                        echo "Installing Python locally without root...${WORKSPACE}"
                        mkdir -p $WORKSPACE/python-local
                        cd $WORKSPACE/python-local

                        curl -LO https://github.com/astral-sh/python-build-standalone/releases/download/20260814/cpython-3.14.7+20260814-x86_64_v4-unknown-linux-gnu-install_only.tar.gz
                        tar -xzf cpython-3.14.7+20260814-x86_64_v4-unknown-linux-gnu-install_only.tar.gz

                        mkdir -p $WORKSPACE/.local/bin
                        ln -sf $WORKSPACE/python-local/python/bin/python3 $WORKSPACE/.local/bin/python3
                        ln -sf $WORKSPACE/python-local/python/bin/pip3 $WORKSPACE/.local/bin/pip3

                        rm -rf *.tar.gz
                    fi
                    export PATH="$WORKSPACE/python-local/python/bin:$PATH"

                    python3 --version
                    pip3 --version
                '''
            }
        }

        stage('2. Install packages') {
            steps {
                echo 'Install packages...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'nexus-cicd-admin',
                                                      usernameVariable: 'NEXUS_USER',
                                                      passwordVariable: 'NEXUS_PASS')]) {

                      sh '''
                            export PATH="$WORKSPACE/python-local/python/bin:$PATH"

                            pip3 install --no-cache-dir --upgrade pip
                            pip3 install --no-cache-dir build twine ruff pytest

                            if [ -f requirements-dev.txt ]; then
                                pip3 install --no-cache-dir \
                                    --extra-index-url http://${NEXUS_USER}:${NEXUS_PASS}@${NEXUS_TRUSTED_HOST}:${NEXUS_PORT}/${NEXUS_URI}/${PYTHON_GROUP_URI}/simple \
                                    --trusted-host ${NEXUS_TRUSTED_HOST} \
                                    -r requirements-dev.txt
                            fi
                        '''

                    }
                }
            }
        }

        stage('3. Lint & Test inside Container') {
            steps {
                echo 'Running ruff and pytest...'
                sh '''
                    export PATH="$WORKSPACE/python-local/python/bin:$PATH"
                    ruff check .
                    pytest --junitxml=report.xml
                '''
            }
        }

        stage('4a. Build Package ') {
            steps {
                echo 'Building .whl & .tar.gz...'
                sh """
                    export PATH="$WORKSPACE/python-local/python/bin:$PATH"

                    rm -rf dist build *.egg-info
                    python3 -m build
                """
            }
        }

        stage('5. Upload to Nexus and Generate SBOM') {
            when {
                buildingTag()
            }
            steps {
                script {
                    def gitTag = env.TAG_NAME ?: env.BRANCH_NAME
                    def cleanVersion = gitTag.replaceAll(/^v/, '')

                    echo 'Uploading to Nexus...when it is a tag'
                    withCredentials([usernamePassword(credentialsId: 'nexus-cicd-admin',
                                                      usernameVariable: 'NEXUS_USER',
                                                      passwordVariable: 'NEXUS_PASS'),
                                                      string(credentialsId: 'DT_API_KEY', variable: 'DT_API_KEY')]) {
                        sh '''
                            export PATH="$WORKSPACE/python-local/python/bin:$PATH"
                            python3 twine_non_ssl.py upload \
                                --repository-url http://${NEXUS_SERVICE_HOST}:${NEXUS_PORT}/${NEXUS_URI}/${PYTHON_HOSTED_URI}/ \
                                -u ${NEXUS_USER} -p "${NEXUS_PASS}" \
                                --verbose \
                                dist/*

                            python3 -m venv .sbom-venv
                            .sbom-venv/bin/pip install --no-cache-dir cyclonedx-bom==7.2.1
                            .sbom-venv/bin/cyclonedx-py requirements -i requirements.txt -o bom.json --output-format json
                            rm -rf .sbom-venv

                            curl -sS -X POST "http://${DEPENDENCY_TRACK_API_HOST}:${DEPENDENCY_TRACK_API_PORT}/api/v1/bom" \
                                -H "X-Api-Key: $DT_API_KEY" \
                                -F "autoCreate=true" \
                                -F "projectName=${PROJECT_NAME}" \
                                -F "projectVersion=''' + cleanVersion + '''" \
                                -F "isLatest=true" \
                                -F "bom=@bom.json"
                        '''
                    }
                }
            }
        }

        stage('6. Dockerize (Only on Tag & if Dockerfile exists)') {
            when {
                allOf {
                    buildingTag()
                    expression { fileExists 'Dockerfile' }
                }
            }
            steps {
                script {
                    def imageName = env.PROJECT_NAME
                    def gitTag = env.TAG_NAME ?: env.BRANCH_NAME
                    def cleanVersion = gitTag.replaceAll(/^v/, '')
                    def registry = "saturn:30088"
                    def fullImageName = "${registry}/${imageName}"
                    def imageTag = "${fullImageName}:${cleanVersion}"
                    def latestTag = "${fullImageName}:latest"

                    withCredentials([usernamePassword(credentialsId: 'nexus-cicd-admin',
                                                     usernameVariable: 'nexus_user',
                                                     passwordVariable: 'nexus_password'),
                                                     usernamePassword(credentialsId: 'nexus-cicd-admin-ro',
                                                     usernameVariable: 'nexus_ro_user',
                                                     passwordVariable: 'nexus_ro_pass')]) {

                        sh '''
                            mkdir -p "${WORKSPACE}/.docker-config"
                            export DOCKER_CONFIG="${WORKSPACE}/.docker-config"
                            echo "$nexus_password" | docker login ''' + registry + ''' -u "$nexus_user" --password-stdin

                            docker build \
                                --build-arg NEXUS_HOST='''+ registry + ''' \
                                --build-arg NEXUS_INDEX=${NEXUS_URI}/${PYTHON_GROUP_URI}/simple \
                                --build-arg NEXUS_USER="$nexus_ro_user" \
                                --build-arg NEXUS_PASS="$nexus_ro_pass" \
                                -t ''' + imageTag + ''' \
                                -t ''' + latestTag + ''' \
                                .

                            docker push ''' + imageTag + '''
                            docker push ''' + latestTag + '''

                            rm -rf "${WORKSPACE}/.docker-config"
                            docker rmi ''' + imageTag + ' ' + latestTag + ''' || true
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'report.xml'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}