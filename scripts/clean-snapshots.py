import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name='eu-central-1')

volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['Prod']
            }
        ]
    )

for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    for snap in sorted_by_date[2:]:
        # Delete Snapshot
        response = ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
        print(response)