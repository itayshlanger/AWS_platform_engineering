# CLI Tool for AWS Platform Engineering
# Overview
This project is a Command-Line Interface (CLI) tool designed to enhance productivity through platform engineering in AWS. Built using Python 3, Boto3, and AWS CLI, it offers an efficient way to interact with AWS services. To provide a more convenient and user-friendly experience, we also utilize Jenkins pipelines as a graphical user interface (UI) for managing and executing tasks.(this tool currently works only on ubuntu0
# Features
- AWS Integration: Seamlessly interacts with AWS services using Boto3 and AWS CLI.
- Jenkins Pipeline UI: Provides a graphical interface via Jenkins pipelines for easier task management.
- Platform Engineering: Aimed at increasing productivity and streamlining AWS operations.
# Prerequisites
- sudo apt-get update
-  python3 : sudo apt-get python3
-  boto3 : sudo apt-get python3-boto3
-  AWS CLI : https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
-  Jenkins : https://www.jenkins.io/doc/book/installing/linux/
# Step By Step CLI
- configure your AWS Cli
```bash
aws configure
```
-  To use the CLI tool simply clone this repo and run itay_project.py with the fitting arguments
```bash
git clone https://github.com/itayshlanger/AWS_platform_engineering.git
python3 AWS_platform_engineering/itay_project.py \
--resource <resorce> --action <action>
```
# Step by Step UI
- Access Jenkins at your-IP:8080 and download suggested plugins
- After first set up , go to Manage Jenkins > Plugins > Available plugins
- Search for ThinBackup and install it
- Back at your commandline copy jenkins_conf to your jenkins_home(for example: /var/lib/jenkins)
```
sudo cp -r AWS_platform_engineering.git/jenkins_conf/ /path/to/your/jenkins_home
```
- Change ownership of the files to jenkins
```
sudo chown -R jenkins:jenkins /path/to/your/jenkins_home/backup*
#make sure owned by jenkins
ls -l /path/to/your/jenkins_home
```
- Make an applicative user that is able to run python scripts and give jenkins the privileges to run python scripts as this user.
(make sure to configure awscli on that user change in Jenkinsfiles to match user) 
```
sudo visudo
```
Add at bottom of file
```
jenkins ALL=(ubuntu) NOPASSWD: /usr/bin/python3
```
- Go back to your jenkins consule and go to Manage Jenkins > System > Jenkins Location > change URL to http://your-ip:8080/
  ![image](https://github.com/user-attachments/assets/82234b17-4f02-476a-89d5-006bc3ddf243)
- Go to Manage Jenkins > System > ThinBackup > change Backup dir to /you/path/to/jenkins_home/backup
![image](https://github.com/user-attachments/assets/3128de21-0132-4c23-a8c1-62c9c7fa36b2)
- Restart jenkins
```
sudo systemctl restart jenkins
```
- log in to jenkins and go to Manage Jenkins > ThinBackup > restore (check restore plugins)
- Restart jenkins again and log in with the Username: User and Password : User (Adminasstrive user)
