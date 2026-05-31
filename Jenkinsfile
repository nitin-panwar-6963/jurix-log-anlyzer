pipeline {
    agent any

    environment {
        NAMESPACE = "jurix"
        IMAGE = "jurixai"
    }

    stages {

        stage("cloning") {
            steps {

                echo "cloning the code from github...."

                git branch: 'main',
                    url: 'https://github.com/nitin-panwar-6963/Nitin-Jurix-AI.git'

                echo "code clone successful......"
            }
        }

        stage("build") {
            steps {

                echo "build docker image....."

                sh "docker build -t $IMAGE ."

                echo "docker image build successfully ..."
            }
        }

        stage("pushing") {
            steps {

                echo "push to docker hub ...."

                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker',
                        usernameVariable: 'dockerhubuser',
                        passwordVariable: 'dockerHubpass'
                    )
                ]) {

                    sh '''
                    docker login -u $dockerhubuser -p $dockerHubpass

                    docker tag $IMAGE:latest $dockerhubuser/$IMAGE:latest

                    docker push $dockerhubuser/$IMAGE:latest
                    '''

                    echo "successfully pushed to docker hub...."
                }
            }
        }

        stage("build namespace") {
            steps {

                sh '''
                kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE
                '''

                echo "successfully created namespace ....."
            }
        }

        stage("secret setup") {
            steps {

                withCredentials([
                    string(
                        credentialsId: 'groq-api-key',
                        variable: 'GROQ_API_KEY'
                    )
                ]) {

                    sh '''
                    kubectl create secret generic jurix-secret \
                    --from-literal=GROQ_API_KEY=$GROQ_API_KEY \
                    -n $NAMESPACE \
                    --dry-run=client -o yaml | kubectl apply -f -
                    '''

                    echo "Secret created successfully..."
                }
            }
        }

        stage("cluster app") {
            steps {

                echo "creating kubernetes resources..."

                sh '''
                kubectl apply -f k8s/Deployment.yml -n $NAMESPACE

                kubectl apply -f k8s/Service.yml -n $NAMESPACE

                kubectl apply -f k8s/ingress.yml -n $NAMESPACE
                '''

                echo "created successfully ....."
            }
        }


        stage("deploy") {
            steps {

                echo "start deploying app ....."

                sh "kubectl port-forward service/jurix-service -n jurix 8000:8000 --address=0.0.0.0"
            }
        }
    }
     post {
        failure {
            script {
                echo '🚨 [ALERT] Build Failed! Gathering live console trace for JurixAI SRE...'
                
                def liveLogs = ""
                try {
                    liveLogs = currentBuild.rawBuild.getLog(120).join('\n')
                } catch (Exception e) {
                    liveLogs = "🚨 Jenkins Build Crash Trace:\nJob: ${env.JOB_NAME} failed at Build #${env.BUILD_NUMBER}."
                }
                
                // 🛠️ PURE BASH ESCAPING LAYER: Bina kisi Groovy import ya library ke
                // Hum raw string ko seedhe shell argument me bhejenge aur env variables se double quotes handle karenge
                env.RAW_LOGS_DATA = liveLogs
                
                echo "📡 Sending direct payload matrix via Curl to JurixAI Backend..."
                
                // Bash script runtime par khud sahi JSON ready karega bina pipeline crash kiye
                sh """
                    # Newlines, Tabs aur Carriage Returns ko pure escape karna python/curl compatible banane ke liye
                    CLEAN_LOGS=\$(echo "\$RAW_LOGS_DATA" | sed 's/\\\\/\\\\\\\\/g' | sed 's/"/\\\\"/g' | awk '{printf "%s\\\\n", \$0}' | sed 's/\\t/\\\\t/g')
                    
                    # Exact JSON payload structure bundle inside curl block
                    curl -X POST \
                    -H "Content-Type: application/json" \
                    -d "{
                        \\\"job_name\\\": \\\"${env.JOB_NAME}\\\",
                        \\\"build_number\\\": \\\"${env.BUILD_NUMBER}\\\",
                        \\\"logs\\\": \\\"\$CLEAN_LOGS\\\"
                    }" \
                    http://localhost:5000/webhook/jenkins-failure
                """
            }
        }
    }
}
