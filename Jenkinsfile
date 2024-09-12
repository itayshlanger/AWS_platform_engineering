pipeline {
    agent any

    stages {
        stage('Run Python Script') {
            steps {
                script {

                    def command = "python3 Itay_project.py -r ec2 --action ${ACTION}"

                    if (action == 'create') {
                        command += " --type ${type} --ami ${AMI}"
                    }

                    // Execute the command
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
