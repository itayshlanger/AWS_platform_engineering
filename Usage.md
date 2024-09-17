# Usage
**The CLI tool supports various commands and arguments to manage AWS resources. Below is a description of the available commands and their options.**

## Arguments
**Resource Type**

-r, --resource (required): Type of AWS resource to manage. Choices are:
- ec2 - Manage EC2 instances.
- s3 - Manage S3 buckets.
- route53 - Manage Route 53 records.

**Actions**

-a, --action (required): Action to perform on the specified resource. Choices are:
- create - Create a new resource.
- manage - Manage existing resources.
- list - List resources.
- upload - Upload a file to an S3 bucket.
- record - Manage Route 53 records.

## EC2 Arguments
**-t, --type: Type of EC2 instance. Choices are:**

- t2.nano
- t4g.nano

**-i, --image: Image for EC2 instance. Choices are:**

- ubuntu
- linux

**--start: Instance ID to start (required for the manage action).**

**--stop: Instance ID to stop (required for the manage action).**

## S3 Arguments
**-p, --public: Specify if public access is needed for the S3 bucket. Choices are:**

- true
- false

**-f, --file: File path to upload (required for the upload action).**

## Route 53 Arguments
**-d, --delete: Hosted zone ID to delete a Route 53 record (required for manage action).**

**-u, --update: Hosted zone ID to update a Route 53 record (required for manage action).**

**-c, --create: Hosted zone ID to create a Route 53 record (required for manage action).**

**-v, --value: Value for a Route 53 record (required for manage action).**

**--TTL: TTL for a Route 53 record (required for manage action).**

**-RT, --Rtype: Type of a Route 53 record (required for manage action).**

## General Arguments
**-n, --name: Specify a name (default is "CLI-itay").**

# Examples
**Here are some examples of how to use the CLI tool:**

**Creating an EC2 Instance**
```
python itay_project.py -r ec2 -a create -t t2.nano -i ubuntu
```
**Managing an EC2 Instance**
```
python itay_project.py -r ec2 -a manage --start i-1234567890abcdef
```
**Uploading a File to an S3 Bucket**
```
python itay_project.py -r s3 -a upload -f /path/to/file.txt -p true
```
**Managing Route 53 Records**
```
python itay_project.py -r route53 -a record -c Z1234567890 -v example.com -TTL 300 -RT A
```
