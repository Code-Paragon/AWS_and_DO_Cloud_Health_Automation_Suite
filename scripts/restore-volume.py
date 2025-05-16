import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')

instance_id = 'i-07635d06d850e6aec'

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

instance_volume = volumes['Volumes'][0]
print(instance_volume)

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

if snapshots['Snapshots']:
    latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
    print(latest_snapshot['StartTime'])
    new_volume = ec2_client.create_volume(
        SnapshotId=latest_snapshot['SnapshotId'],
        AvailabilityZone=instance_volume['AvailabilityZone'],
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'dev'
                    }
                ]
            }
        ]
    )

    while True:
        vol = ec2_resource.Volume(new_volume['VolumeId'])
        print(vol.state)
        if vol.state == 'available':
            ec2_resource.Instance(instance_id).attach_volume(
                Device='/dev/xvdb',
                VolumeId=new_volume['VolumeId']
            )
            break
else:
    print("No snapshots found for volume", instance_volume['VolumeId'])
