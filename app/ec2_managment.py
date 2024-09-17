def checking_instances_ids(resource):
    instance_id_list = []
    for i in resource.instances.all():
        if i.tags:
            for idx, tag in enumerate(i.tags):
                if tag['Key'] == 'Creation':
                    if str(tag['Value']) == "CLI_Itay":
                        instance_id_list.append(i.id)
    return instance_id_list


def check_running_instances(resource):
    num_of_running_instances = 0
    for i in resource.instances.all():
        if i.tags:
            for idx, tag in enumerate(i.tags):
                if tag['Key'] == 'Creation':
                    if str(tag['Value']) == "CLI_Itay":
                        instance = resource.Instance(i.id)
                        if instance.state['Name'] == 'running':
                            num_of_running_instances += 1
    return num_of_running_instances


# EC2 - a function for each of the possible actions
def handle_ec2(action, instance_type=None, ami=None, resource=None, instance_id=None, arg=None, name=None):
    if action == 'create':
        if name is None:
            name = 'CLI_Itay'
        if check_running_instances(resource) < 2:
            if ami == "ubuntu":
                ami = "ami-0e86e20dae9224db8"
            elif ami == "linux":
                ami = "ami-0182f373e66f89c85"
            print('Creating EC2 instance named:', name, '\nwith AMI:', ami, '\nand type:', instance_type, '...')
            instances = resource.create_instances(
                ImageId=ami,
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1,
                KeyName="Security-itay",
                SecurityGroupIds=("sg-021b36fb94e7c77b6",),
                SubnetId="subnet-0f2d85780bc598bd6",
                # making a way to recognize instances created with CLI
                # another way would be inserting my IP address to specify instances created only by a specific user
                TagSpecifications=[{'ResourceType': 'instance',
                                    'Tags': [{
                                        'Key': 'Name',
                                        'Value': name},
                                        {'Key': 'Creation',
                                         'Value': "CLI_Itay"}
                                    ]
                                    }
                                   ],
            )
            instance = instances[0]
            instance.wait_until_running()
            instance.reload()
            # presenting the instance created
            print('#############################################')
            print('Instance created successfully !')
            print("Instance Name:", name)
            print("Instance ID:", instance.id)
            print("Public IP:", instance.public_ip_address)
            print("Instance Type:", instance_type)
            print("Instance AMI:", ami)
        else:
            print('error: too many instance are currently running\n'
                  'currently running instances:', check_running_instances(resource),
                  '\nnumber of running instances allowed: 2')

    elif action == 'manage':

        if arg == 'stop':
            if instance_id in checking_instances_ids(resource):
                resource.instances.filter(InstanceIds=[instance_id]).stop()
                print("stopping EC2 instance...")
            else:
                print('Error: this instance was not created by this CLI and cannot be managed.')
        elif arg == 'start':
            if check_running_instances(resource) < 2:
                if instance_id in checking_instances_ids(resource):
                    resource.instances.filter(InstanceIds=[instance_id]).start()
                    print("starting EC2 instance...")
                else:
                    print('Error: this instance was not created by this CLI and cannot be managed.')

            else:
                print('error: too many instance are currently running\n'
                      'currently running instances:', check_running_instances(resource), '(only 2 allowed)')

    elif action == 'list':
        print("Listing EC2 instances created by this CLI...")
        num_of_instances = 0
        for i in resource.instances.all():
            if i.tags:
                for idx, tag in enumerate(i.tags):
                    if tag['Key'] == 'Creation':
                        if str(tag['Value']) == "CLI_Itay":
                            instance = resource.Instance(i.id)
                            if instance.state['Name'] == 'running':
                                num_of_instances += 1
                                print(i.id, 'is running')
                            elif instance.state['Name'] == 'terminated':
                                num_of_instances += 1
                                print(i.id, 'is terminated')
                            elif instance.state['Name'] == 'stopped' or 'stopping':
                                num_of_instances += 1
                                print(i.id, 'is stopped')
        if num_of_instances <= 0:
            print('No instances created by this CLI yet.')
    else:
        print("Invalid action for EC2. Use 'create', 'manage', or 'list'.")
