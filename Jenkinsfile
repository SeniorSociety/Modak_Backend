def NAME_OF_STAGE
pipeline {
    agent {
        docker {
            image 'dwenup/jenkins-image:101.0.5'
            args '-u root:sudo -v /var/run:/var/run'
        }
    }
    environment { 
                AWS_S3_STORAGE_BUCKET_NAME = credentials('AWS_S3_STORAGE_BUCKET_NAME')
                AWS_S3_BUCKET_URL          = credentials('AWS_S3_BUCKET_URL')
                SECRET_KEY                 = credentials('SECRET_KEY')
                ALGORITHMS                 = credentials('ALGORITHMS')
                DB_ENGINE                  = credentials('DB_ENGINE')
                DB_NAME                    = credentials('DB_NAME')
                DB_USER                    = credentials('DB_USER')
                DB_PASSWORD                = credentials('DB_PASSWORD')
                DB_HOST                    = credentials('DB_HOST')
                DB_PORT                    = credentials('DB_PORT')
                AWS_IAM_ACCESS_KEY_ID      = credentials('AWS_IAM_ACCESS_KEY_ID')
                AWS_IAM_SECRET_ACCESS_KEY  = credentials('AWS_IAM_SECRET_ACCESS_KEY')
                IMAGENAME                  = credentials('IMAGENAME')
                DOCKERHUB_CREDENTIALS      = credentials('DWENUP_DOCKERHUB')
                AWS_REGION_NAME            = credentials('AWS_REGION_NAME')
                AWS_LOG_GROUP              = credentials('AWS_LOG_GROUP')
                AWS_LOG_STREAM             = credentials('AWS_LOG_STREAM')
                AWS_LOGGER_NAME            = credentials('AWS_LOGGER_NAME')
                BACKEND_FIRST_INSTANCE_IP  = credentials('BACKEND_FIRST_INSTANCE_IP')
                BACKEND_SECOND_INSTANCE_IP = credentials('BACKEND_SECOND_INSTANCE_IP')
                HOKINS_TOKEN               = credentials('HOKINS_TOKEN')
    }
    stages {
        stage('Start') {
            steps {
                script {
                    blocks = [
                        [
                            "type": "section",
                            "text": [
                                "type": "mrkdwn",
                                "text": "*<BACKEND PIPELINE START!>*"
                            ]
                        ],
                        [
                            "type": "divider"
                        ]
                        ,
                        [
                            "type": "section",
                            "fields": [
                                [
                                    "type": "mrkdwn",
                                    "text": "*Branch:*\n<${env.GIT_URL}|${env.GIT_BRANCH}>"
                                ],
                                [
                                    "type": "mrkdwn",
                                    "text": "*BuildTag:*\n${env.BUILD_TAG}"
                                ],
                            ]
                        ]
	                ]
                    slackSend (color: '#0FFF22', blocks: blocks)
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    NAME_OF_STAGE = "${env.STAGE_NAME}"
                    sh 'echo "dwen is handsome!"'
                    sh """
                    echo 'AWS_IAM_ACCESS_KEY_ID       = "${env.AWS_IAM_ACCESS_KEY_ID}"' >> my_settings.py
                    echo 'AWS_IAM_SECRET_ACCESS_KEY   = "${env.AWS_IAM_SECRET_ACCESS_KEY}"' >> my_settings.py
                    echo 'AWS_S3_STORAGE_BUCKET_NAME  = "${env.AWS_S3_STORAGE_BUCKET_NAME}"' >> my_settings.py
                    echo 'AWS_S3_BUCKET_URL           = "${env.AWS_S3_BUCKET_URL}"' >> my_settings.py
                    echo 'SECRET_KEY                  = "${env.SECRET_KEY}"' >> my_settings.py
                    echo 'ALGORITHMS                  = "${env.ALGORITHMS}"' >> my_settings.py
                    echo 'AWS_REGION_NAME             = "${env.AWS_REGION_NAME}"' >> my_settings.py
                    echo 'AWS_LOG_GROUP               = "${env.AWS_LOG_GROUP}"' >> my_settings.py
                    echo 'AWS_LOG_STREAM              = "${env.AWS_LOG_STREAM}"' >> my_settings.py
                    echo 'AWS_LOGGER_NAME             = "${env.AWS_LOGGER_NAME}"' >> my_settings.py
                    echo 'DATABASES = {
                            "default" : {
                                "ENGINE"    : "${env.DB_ENGINE}",
                                "NAME"      : "${env.DB_NAME}",
                                "USER"      : "${env.DB_USER}",
                                "PASSWORD"  : "${env.DB_PASSWORD}",
                                "HOST"      : "${env.DB_HOST}",
                                "PORT"      : "${env.DB_PORT}",
                            }
                        }' >> my_settings.py
                    """
                    app = docker.build "${env.IMAGENAME}"
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    NAME_OF_STAGE = "${env.STAGE_NAME}"
                    app.inside {
                        sh 'python3 manage.py test'
                    }
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    NAME_OF_STAGE = "${env.STAGE_NAME}"
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                }
            }
        }
        stage('Delete') {
            steps {
                script {
                    NAME_OF_STAGE = "${env.STAGE_NAME}"
                    sh "docker rmi '${env.IMAGENAME}:${env.BUILD_NUMBER}'"
                    sh "docker rmi '${env.IMAGENAME}:latest'"
                }
            }
        }
        stage('Deploy #1') {
            steps {
                script {
                    NAME_OF_STAGE = "${env.STAGE_NAME}"
                }
                sshagent(credentials : ['real-ssh-key']) {
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@'${BACKEND_FIRST_INSTANCE_IP}' 'docker pull '${env.IMAGENAME}:latest' && docker stop \$(docker ps -aq) && docker container prune -f && docker image prune -f && docker run -dp 8000:8000 '${env.IMAGENAME}:latest''"
                }
            }
        }
        stage('Deploy #2') {
            steps {
                script {
                    NAME_OF_STAGE = "${env.STAGE_NAME}"
                }
                sshagent(credentials : ['real-ssh-key']) {
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@'${BACKEND_SECOND_INSTANCE_IP}' 'docker pull '${env.IMAGENAME}:latest' && docker stop \$(docker ps -aq) && docker container prune -f && docker image prune -f && docker run -dp 8000:8000 '${env.IMAGENAME}:latest''"
                }
            }
        }
        stage('Finish') {
            steps {
                script {
                    slackSend (color: '#0075FC', message: "*<BACKEND PIPELINE FINISHED>*\n<${env.RUN_DISPLAY_URL}|JenkinsPipeLine>")
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        failure {
            slackSend (color: '#FF1001', message: """
            <!channel>\n*<$NAME_OF_STAGE FAILED!>*\nMore Info at : <${env.RUN_DISPLAY_URL}/consoleFull|Console log>
            """)
        }
    }
}


