import os
import json
from botocore.exceptions import ClientError


def list_all_buckets(resource):
    list_of_all_buckets = []
    # List all buckets
    bucket_list = resource.list_buckets()
    buckets = bucket_list['Buckets']
    # Loop through all buckets to check their tags
    for bucket in buckets:
        bucket_name = bucket['Name']
        list_of_all_buckets.append(bucket_name)
    return list_of_all_buckets


def check_s3_from_cli(resource):
    list_of_buckets_created_by_cli = []
    try:
        # List all buckets
        bucket_list = resource.list_buckets()
        buckets = bucket_list['Buckets']
        # Loop through all buckets to check their tags
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Get the tags for the current bucket
                tag_list = resource.get_bucket_tagging(Bucket=bucket_name)
                tags = tag_list['TagSet']
                # Check if the 'Created: CLI-itay' tag exists
                for tag in tags:
                    if tag['Key'] == 'Creation' and tag['Value'] == 'CLI-itay':
                        list_of_buckets_created_by_cli.append(bucket_name)
                        break
            except ClientError as e:
                # If the bucket doesn't have any tags or an error occurs, we ignore it
                pass
    except ClientError as e:
        print("Error:", e)
    return list_of_buckets_created_by_cli


def handle_s3(action, public=None, name=None, file=None, resource=None):
    if action == 'create':
        print('Creating S3 bucket ...')
        if name is None:
            name = 'cli-itay'
        try:
            resource.create_bucket(Bucket=name)
            print("Bucket", name, "created successfully.")
            resource.put_bucket_tagging(
                Bucket=name,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'Creation',
                            'Value': 'CLI-itay'
                        }
                    ]
                }
            )
            if public == 'true':
                sure = False
                while not sure:
                    double_check = input('Are you sure you want to make your Bucket public?(yes/no): ')
                    if double_check == 'yes':
                        resource.put_public_access_block(
                            Bucket=name,
                            PublicAccessBlockConfiguration={
                                'BlockPublicAcls': False,
                                'IgnorePublicAcls': False,
                                'BlockPublicPolicy': False,
                                'RestrictPublicBuckets': False
                            }
                        )
                        policy_resource = "arn:aws:s3:::" + name + "/*"
                        bucket_policy = {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Sid": "PublicReadGetObject",
                                    "Effect": "Allow",
                                    "Principal": "*",
                                    "Action": "s3:GetObject",
                                    "Resource": policy_resource
                                }
                            ]
                        }
                        bucket_policy = json.dumps(bucket_policy)
                        resource.put_bucket_policy(Bucket=name, Policy=bucket_policy)
                        print("Bucket", name, "is now public.")
                        sure = True
                    elif double_check == 'no':
                        # # Ensure the bucket is private
                        # resource.put_bucket_acl(Bucket=name, ACL='private')
                        print("Bucket", name, "is private.")
                        sure = True
                    else:
                        print('Error: invalid input (yes/no), please try again!')
            else:
                # Ensure the bucket is private
                # resource.put_bucket_acl(Bucket=name, ACL='private')
                print("Bucket", name, "is private.")

        except ClientError as e:
            print("Error:", e)
    elif action == 'upload':
        if name in check_s3_from_cli(resource):
            print('Uploading file to', name, 'bucket ...')
            try:
                # Extract the file name from the file path
                file_name = os.path.basename(file)
                # Upload the file
                resource.upload_file(file, name, file_name)
                print('File', file_name, 'uploaded successfully to bucket', name)

            except ClientError as e:
                print("Error uploading file:", e)
        elif name in list_all_buckets(resource):
            print('Error: the bucket', name, 'was not created by this CLI and cannot be interacted with.')
        else:
            print('Error: bucket not found!')
    elif action == 'list':
        print("Listing S3 buckets...")
        list_of_buckets = check_s3_from_cli(resource)
        if not list_of_buckets:
            print('No buckets were created by this CLI yet.')
        else:
            print('The S3 buckets created from this CLI are:')
            for bucket in list_of_buckets:
                print(bucket)
    else:
        print("Invalid action for S3. Use 'create', 'upload', or 'list'.")
