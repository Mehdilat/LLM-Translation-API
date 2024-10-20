pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = credentials('github-pat-id')
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        AWS_CREDENTIALS = credentials('aws-credentials-id')
        AWS_DEFAULT_REGION = 'eu-west-3'
        ECR_REPO_URI = '341250327392.dkr.ecr.eu-west-3.amazonaws.com/llm_translation_api'
        DOCKERHUB_REPO = 'mehdilat/llm_translation_api'
        IMAGE_TAG = 'latest'
        LAMBDA_FUNCTION_NAME = 'Project_LLM_translation_API'
    }

    stages {
        /*
        stage('Clone') {
            steps {
                echo 'Cloning Stage'

                git url: 'https://github.com/Mehdilat/Project-LLM-Translation-API.git', credentialsId: 'github-credentials-id'
            }
        }
        */
        
        stage('Build') {
            steps {
                echo 'Building Stage'

                script {

                    def imageTag = "my-app:${env.BUILD_NUMBER}"

                    sh "docker build -t ${imageTag} ."
                    docker.build(DOCKERHUB_REPO + ":${IMAGE_TAG}")
                }
            }
        }

        stage('Build Test') {
            steps {
                echo 'Build Testing Stage'

                error 'STOP'
            }
        }

        stage('Package (Dockerhub)') {
            steps {
                echo 'Packaging Stage (Dockerhub)'

                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKERHUB_CREDENTIALS') {
                    docker.image(DOCKERHUB_REPO + ":${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Package (Amazon ECR)') {
            steps {
                echo 'Packaging Stage (Amazon ECR)'

                script {
                    withAWS(credentials: 'AWS_CREDENTIALS', region: "${AWS_DEFAULT_REGION}") {
                        sh """
                        aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}
                        docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${ECR_REPO_URI}:${IMAGE_TAG}
                        docker push ${ECR_REPO_URI}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment Stage'

                script {
                    withAWS(credentials: 'AWS_CREDENTIALS', region: "${AWS_DEFAULT_REGION}") {
                        sh """
                        aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --image-uri ${ECR_REPO_URI}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deployment Test') {
            steps {
                echo 'Deployment Testing Stage'

                script {
                    withAWS(credentials: 'AWS_CREDENTIALS', region: "${AWS_DEFAULT_REGION}") {
                        // Sample test payload
                        def payload = '{"text": "I love using Hugging Face models!"}'
                        sh """
                        aws lambda invoke --function-name ${LAMBDA_FUNCTION_NAME} --payload '${payload}' output.json
                        cat output.json
                        """
                    }
                }
            }
        }

/*
        stage('Push Changes to GitHub') {
            when {
                expression { currentBuild.result == 'SUCCESS' } // Only execute if all previous stages were successful
            }
            steps {
                script {
                    def gitUser = 'Mehdilat'
                    def gitEmail = 'madilat@gmail.com'

                    // Configure Git user
                    sh """
                    git config user.name "${gitUser}"
                    git config user.email "${gitEmail}"
                    """

                    // Add changes, commit, and push
                    sh """
                    git add .
                    git commit -m "${GIT_COMMIT_MESSAGE}" || echo "No changes to commit"
                    git push https://github.com/Mehdilat/Project-LLM-Translation-API.git HEAD:main
                    """
                }
            }
        }
*/
    }
    
    post {
        always {
            cleanWs()
        }
    }
}