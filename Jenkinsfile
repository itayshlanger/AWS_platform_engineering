pipeline {
    agent any
stages {
        stage('Run Python Script') {
            steps {
                script {

                    def command = "python3 Itay_project.py -r ec2 --action ${ACTION}"

                    if (action == 'create') {
                        command += " --type ${Type} --ami ${AMI}"
                    } else if (action == 'start') {
			command = "python3 Itay_project.py -r ec2 --action manage --start ${Name}"
		    } else if (action == 'stop') {
                        command = "python3 Itay_project.py -r ec2 --action manage --stop ${Name}"
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
