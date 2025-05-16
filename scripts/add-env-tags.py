import boto3

ec2_client_frankfort = boto3.client('ec2', region_name='eu-central-1')
ec2_resource_frankfurt = boto3.resource('ec2', region_name='eu-central-1')

ec2_client_paris = boto3.client('ec2', region_name='eu-west-3')
ec2_resource_paris = boto3.resource('ec2', region_name='eu-west-3')

instance_ids_frankfurt = []
instance_ids_paris = []

reservations_frankfurt = ec2_client_frankfort.describe_instances()['Reservations']

for reservation in reservations_frankfurt:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids_frankfurt.append(instance['InstanceId'])


response = ec2_resource_frankfurt.create_tags(
    Resources=instance_ids_frankfurt,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod',
        }
    ]
    )

reservations_paris = ec2_client_paris.describe_instances()['Reservations']

for reservation in reservations_paris:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids_paris.append(instance['InstanceId'])


response = ec2_resource_paris.create_tags(
    Resources=instance_ids_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev',
        }
    ]
    )