from botocore.exceptions import ClientError
import uuid


def get_list_of_hostedzones_from_cli(resource):
    hosted_zones = resource.list_hosted_zones()
    list_of_tagged_zones = []
    for zone in hosted_zones['HostedZones']:
        hosted_zone_id = zone['Id'].replace("/hostedzone/", "")
        try:
            tags_response = resource.list_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=hosted_zone_id
            )
            for tag in tags_response['ResourceTagSet']['Tags']:
                if tag['Key'] == 'Created' and tag['Value'] == 'CLI-Itay':
                    list_of_tagged_zones.append(zone)
                    break

        except ClientError as e:
            print("Error fetching tags for hosted zone", hosted_zone_id, ":", e)
    return list_of_tagged_zones


def handle_route53(action, name=None, public=None, resource=None, delete=None, update=None, create=None,
                   values=None, ttl=None, rtype=None,):
    if action == 'create':
        print('Creating route53 hosted zone...')
        hosted_zone_id = ''
        if public == 'true':
            try:
                # Create the hosted zone with a unique CallerReference
                hosted_zone = resource.create_hosted_zone(
                    Name=name,
                    CallerReference=str(uuid.uuid4()),
                    HostedZoneConfig={
                        'Comment': 'Hosted zone created via CLI',
                        'PrivateZone': False,
                    }
                )
                hosted_zone_id = hosted_zone['HostedZone']['Id'].replace("/hostedzone/", "")
                print("Hosted zone for domain", name, "created successfully. \nHosted zone ID:", hosted_zone_id)
            except ClientError as e:
                print("Error creating hosted zone:", e)
        else:
            try:
                # Create the hosted zone with a unique CallerReference
                hosted_zone = resource.create_hosted_zone(
                    Name=name,
                    CallerReference=str(uuid.uuid4()),
                    VPC={
                        'VPCRegion': 'us-east-1',
                        'VPCId': 'vpc-0a567a6d2b2cf7dec'
                    },
                    HostedZoneConfig={
                        'Comment': 'Hosted zone created via CLI',
                        'PrivateZone': True,
                    }
                )
                hosted_zone_id = hosted_zone['HostedZone']['Id'].replace("/hostedzone/", "")
                print("Hosted zone for domain", name, "created successfully. \nHosted zone ID:", hosted_zone_id)
            except ClientError as e:
                print("Error creating hosted zone:", e)

            # Add a tag to the hosted zone
        try:
            resource.change_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=hosted_zone_id,  # Extract the hosted zone ID
                AddTags=[
                    {
                        'Key': 'Created',
                        'Value': 'CLI-Itay'
                    }
                ]
            )
        except ClientError as e:
            print("Error adding tag:", e)

    elif action == 'record':
        hosted_zones = get_list_of_hostedzones_from_cli(resource)
        for zone in hosted_zones:
            if create or update or delete == zone['Id'].replace('/hostedzone/', ''):
                if update:
                    # checking if record exist on hosted zone
                    record_list = resource.list_resource_record_sets(HostedZoneId=update)
                    success = False
                    for record_set in record_list['ResourceRecordSets']:
                        if name.__add__('.') == record_set['Name']:
                            if rtype is None:
                                rtype = record_set['Type']
                            if ttl is None:
                                ttl = record_set.get('TTL', 'No TTL')
                            if values is None:
                                values = [record['Value'] for record in record_set.get('ResourceRecords', [])]
                            try:
                                change_batch = {
                                    'Changes': [
                                        {
                                            'Action': 'UPSERT',
                                            'ResourceRecordSet': {
                                                'Name': name.__add__('.'),
                                                'Type': rtype,
                                                'TTL': ttl,
                                                'ResourceRecords': [{'Value': value} for value in values]
                                            }
                                        }
                                    ]
                                }
                                resource.change_resource_record_sets(
                                    HostedZoneId=update,
                                    ChangeBatch=change_batch
                                )
                                # Confirm the update
                                print("Updated record", name, "of type", rtype, "in hosted zone", update)
                                success = True
                            except ClientError as e:
                                print("Error updating Route 53 record:", e)
                    if not success:
                        print('Error: no record with the name', name, 'was found')
                elif delete:
                    # checking if record exist on hosted zone
                    record_list = resource.list_resource_record_sets(HostedZoneId=delete)
                    success = False
                    for record_set in record_list['ResourceRecordSets']:
                        if name.__add__('.') == record_set['Name']:
                            print('deleting hosted zone record ...')
                            ttl = record_set.get('TTL', 'No TTL')
                            values = [record['Value'] for record in record_set.get('ResourceRecords', [])]
                            try:
                                # Prepare the change batch for the delete request
                                change_batch = {
                                    'Changes': [
                                        {
                                            'Action': 'DELETE',
                                            'ResourceRecordSet': {
                                                'Name': name.__add__('.'),
                                                'Type': rtype,
                                                'TTL': ttl,
                                                'ResourceRecords': [{'Value': value} for value in values]
                                            }
                                        }
                                    ]
                                }
                                resource.change_resource_record_sets(
                                    HostedZoneId=delete,
                                    ChangeBatch=change_batch
                                )

                                # Confirm the deletion
                                print("Deleted record", name, "of type", rtype, "in hosted zone", delete)
                                success = True

                            except ClientError as e:
                                print("Error deleting Route 53 record:", e)
                    if not success:
                        print('Error: no record with the name', name, 'was found')
                elif create:
                    print('Creating a record for hosted zone :', create, '...')
                    resource.change_resource_record_sets(
                        ChangeBatch={
                            'Changes': [
                                {
                                    'Action': 'CREATE',
                                    'ResourceRecordSet': {
                                        'Name': name,
                                        'ResourceRecords': [
                                            {
                                                'Value': values,
                                            },
                                        ],
                                        'TTL': ttl,
                                        'Type': rtype,
                                    },
                                },
                            ],
                            'Comment': 'Created by CLI',
                        },
                        HostedZoneId=create,
                    )
                    print('succsesfuly created record', name)
            else:
                print('Error: no hosted zone created by this CLI matches this ID')
    elif action == 'list':
        print("Listing Route 53 records...")
        try:
            tagged_zones = get_list_of_hostedzones_from_cli(resource)
            if tagged_zones:
                print("Hosted zones created by this CLI:")
                for tagged_zone in tagged_zones:
                    print(tagged_zone['Name'], "ID:", tagged_zone['Id'].replace("/hostedzone/", ""))
            else:
                print("No hosted zones created by this CLI were found.")

        except ClientError as e:
            print("Error listing hosted zones:", e)
    else:
        print("Invalid action for Route 53. Use 'create', 'manage', or 'list'.")
