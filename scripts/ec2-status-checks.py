import boto3
import schedule
#Checks Health and status as a scheduled Task


ec2_client = boto3.client('ec2', region_name='af-south-1')
ec2_resource = boto3.resource('ec2', region_name='af-south-1')

def check_instance_status():
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(
            f"Instance {status['InstanceId']} is {state} with instance status {ins_status} and system status {sys_status}")
    print("#####################################################\n")

schedule.every(5).seconds.do(check_instance_status)

while True:
    schedule.run_pending()