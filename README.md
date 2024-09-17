# CLI Tool for AWS Platform Engineering
# Overview
This project is a Command-Line Interface (CLI) tool designed to enhance productivity through platform engineering in AWS. Built using Python 3, Boto3, and AWS CLI, it offers an efficient way to interact with AWS services. To provide a more convenient and user-friendly experience, we also utilize Jenkins pipelines as a graphical user interface (UI) for managing and executing tasks.(CLI will work with any OS , UI currently working only on ubuntu)
# Features
- AWS Integration: Seamlessly interacts with AWS services using Boto3 and AWS CLI.
- Jenkins Pipeline UI: Provides a graphical interface via Jenkins pipelines for easier task management.
- Platform Engineering: Aimed at increasing productivity and streamlining AWS operations.
# Prerequisites
```
sudo apt-get update
```
-  python3 :
```
sudo apt-get install python3
```
-  boto3 :
```
sudo apt-get install python3-boto3
```
- flask
```
sudo apt-get install python3-flask
```
-  AWS CLI : https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
-  Jenkins : https://www.jenkins.io/doc/book/installing/linux/
# Step By Step CLI installation
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
Learn in more detail at [Usage.md](https://github.com/itayshlanger/AWS_platform_engineering/blob/main/Usage.md)
<br>**In this phase, I developed a Python CLI tool that allows developers to:**

<br>**EC2 Instances**

- Create: Provision new EC2 instances with options for t3.nano or t4g.nano types, and limit to a maximum of two running instances.
- AMI Choice: Choose between the latest Ubuntu or Amazon Linux AMI.
- Manage Instances: Start and stop instances created through the CLI.
- List Instances: List all EC2 instances created via the CLI.

**S3 Buckets**
  
- Create: Create new S3 buckets with options for public or private access.
Confirmation for Public Buckets: Confirm public access with an additional approval step.
- File Upload: Upload files to buckets created through the CLI.
- List Buckets: List all S3 buckets created via the CLI.

**Route53 DNS Records**

- Create Zones: Create DNS zones using Route53.
- Manage DNS Records: Create, update, or delete DNS records for zones created through the CLI.

# Step by Step UI installation
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
- log in to jenkins and go to Manage Jenkins > ThinBackup > restore latest version(check restore plugins as well)
- Restart jenkins again and log in with the Username: User and Password : User (Adminasstrive user)

**Visual examples:**

- <u>Use each build to manage a different resource:</u>
![image](https://github.com/user-attachments/assets/9292d856-962d-41b8-8abf-c1c42d2f03a0)
- <u>For each build different set of parameters will be needed:</u>

1)![1)](https://github.com/user-attachments/assets/fd977abc-0811-416d-b8cf-6b7bc9ee6d1c)
2)![2)](https://github.com/user-attachments/assets/7f9aef92-b158-450a-8ac9-85b1b14e0d8b)

# API
Start the Flask server:
    ```bash
    python app.py
    ```
The API will run on `http://127.0.0.1:2310`.

## API Endpoints

### POST /project

This endpoint handles requests for managing AWS services such as EC2, S3, and Route 53.

**Request Body:**

- `resource` (required): The AWS resource to manage (`ec2`, `s3`, `route53`).
- `action` (required): The action to perform (`record`, `upload`, `create`, `manage`, `list`).
- Other parameters depend on the specific AWS resource and action.
see in more detail at [Usage.md](https://github.com/itayshlanger/AWS_platform_engineering/blob/main/Usage.md)


