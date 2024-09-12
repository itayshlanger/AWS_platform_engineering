pipeline {
    agent any
stages {
        stage('Run Python Script') {
            steps {
                script {

                    def command = "python3 your_script.py -r ec2 --action ${ACTION}"

                    if (action == 'create') {
                        command += " --type ${Type} --ami ${AMI}"
                    } 
                    sh command
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // Perform any cleanup tasks here if needed
        }
    }
}
