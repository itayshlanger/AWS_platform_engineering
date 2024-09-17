import argparse
import boto3
from Route53_managment import handle_route53
from S3_managment import handle_s3
from ec2_managment import checking_instances_ids, handle_ec2
ec2 = boto3.resource('ec2', region_name= 'us-east-1')
s3 = boto3.client('s3', region_name= 'us-east-1')
route53 = boto3.client('route53', region_name= 'us-east-1')


def main():
    parser = argparse.ArgumentParser(description='Manage AWS resources.')
    parser.add_argument('-r', '--resource', required=True,
                        choices=['ec2', 's3', 'route53'],
                        help='Type of AWS resource to manage.')
    parser.add_argument('-a', '--action', required=True,
                        choices=['create', 'manage', 'list', 'upload', 'record'],
                        help='Action to perform on the specified resource.')
    parser.add_argument('-t', '--type',
                        choices=['t2.nano', 't4g.nano'],
                        help='Type of EC2 instance (required for EC2 create action).')
    parser.add_argument('-i', '--image', '--ami',
                        choices=['ubuntu', 'linux'],
                        help='Image for EC2 instance (required for EC2 create action).')
    parser.add_argument("--start",
                        help='stating which instance to start (required instance ID for EC2 manage action)')
    parser.add_argument("-n", "--name",
                        help='state if specific name is needed ( default name is "CLI-itay")')
    parser.add_argument("--stop",
                        help='stating which instance to stop (require instance ID for EC2 manage action)')
    parser.add_argument("-p", "--public",
                        choices=['true', 'false'],
                        help='state if public access for S3 bucket is needed (required for S3 create action)')
    parser.add_argument("-f", "--file", help='Specify the file path to upload (required for S3 upload action)')
    parser.add_argument("-d", "--delete",
                        help='specify hosted zone ID to delete a route53 record on(required for route53 manage)')
    parser.add_argument("-u", "--update",
                        help='specify hosted zone ID to update a route53 record on(required for route53 manage')
    parser.add_argument("-c", "--create",
                        help='specify hosted zone ID to create a route53 record on(required for route53 manage')
    parser.add_argument("-v", "--value",
                        help='specify value for a route53 record(required for route53 manage')
    parser.add_argument("--TTL", type=int,
                        help='specify TTL for a route53 record(required for route53 manage')
    parser.add_argument("-RT", "--Rtype",
                        help='specify type of a route53 record(required for route53 manage')

    args = parser.parse_args()

    if args.resource == 'ec2':
        if args.action == 'create':
            if not args.type or not args.image:
                parser.error("Both --type and --image are required for creating EC2 instances.")
            handle_ec2(args.action, instance_type=args.type, ami=args.image, resource=ec2, name=args.name)
        elif args.action == 'manage':
            if not args.start and not args.stop:
                parser.error("at least one argument missing,"
                             " --stop or --start are required for managing EC2 instances.")
            elif args.start and args.stop:
                parser.error('only one argument(--start/--stop) can be used for managing EC2 instances')
            if args.stop or args.start in checking_instances_ids(ec2):
                if args.stop:
                    handle_ec2(args.action, resource=ec2, instance_id=args.stop, arg='stop')
                elif args.start:
                    handle_ec2(args.action, resource=ec2, instance_id=args.start, arg='start')
            else:
                print('error: no EC2 instance found with this ID')
        else:
            handle_ec2(args.action, resource=ec2)
    elif args.resource == 's3':
        if args.action == 'create':
            if not args.public:
                parser.error('--public argument is required for creating S3 buckets.')
            handle_s3(args.action, public=args.public, name=args.name, resource=s3)
        elif args.action == 'upload':
            if not args.name or not args.file:
                parser.error('--name and --file arguments are required for uploading a file to S3 bucket.')
            else:
                handle_s3(args.action, name=args.name, file=args.file, resource=s3)
        else:
            handle_s3(args.action, resource=s3)
    elif args.resource == 'route53':
        if args.action == 'create':
            if not args.name or not args.public:
                parser.error('--name and --public are required for creating route53 hosted zone')
            else:
                handle_route53(args.action, name=args.name, public=args.public, resource=route53)
        elif args.action == 'record':
            if not args.delete and not args.update and not args.create:
                parser.error('at least one from'
                             ' --delete or --update or --create are required for managing route53 hosted zone')
            elif (args.delete and args.update) or (args.delete and args.create) or (args.update and args.create):
                parser.error('please choose only one from'
                             ' --delete or --update or --create to manage route53 hosted zone')
            elif args.create:
                if not args.Rtype or not args.value or not args.TTL or not args.name:
                    parser.error('you must state the all of the following parameters to create a route53 record:'
                                 '\n- TTL'
                                 '\n- value'
                                 '\n- record type'
                                 '\n- name')
                else:
                    handle_route53(args.action, resource=route53, create=args.create,
                                   ttl=args.TTL, rtype=args.Rtype, values=args.value, name=args.name)
            elif args.delete:
                if not args.name or not args.Rtype:
                    parser.error('--name and --Rtype must be stated to delete a route53 record')
                else:
                    handle_route53(args.action, resource=route53, delete=args.delete,
                                   rtype=args.Rtype, name=args.name)
            else:
                if not args.name and not (args.ttl or args.value or args.Rtype):
                    parser.error('--name and at least one from --ttl, --Rtype, --value '
                                 '\nare needed to update a route53 record')
                handle_route53(args.action, resource=route53, update=args.update,
                               ttl=args.TTL, rtype=args.Rtype, values=args.value, name=args.name)
        else:
            handle_route53(args.action, resource=route53)


main()
