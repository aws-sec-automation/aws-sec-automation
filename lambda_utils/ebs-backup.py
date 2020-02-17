import boto3
import collections
import datetime
def lambda_handler(event, context):
    # TODO implement
    AccountId = 123456 #CHANGE
    ec = boto3.client('ec2')
    to_tag = collections.defaultdict(list)

    reservations = ec.describe_instances(
            Filters=[
                {'Name': 'tag-key', 'Values': ['backup', 'Backup']},
            ]
        )['Reservations']
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    for instance in instances:
        #read retention tag if exists-> how long keep each snapshot
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = 7

        print(retention_days)
        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                # skip non-EBS volumes
                continue
            vol_id = dev['Ebs']['VolumeId']
            print ("Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId']))

            snap = ec.create_snapshot(
                VolumeId=vol_id,
            )
            to_tag[retention_days].append(snap['SnapshotId'])
            print(to_tag)

    for retention_days in to_tag.keys():
        # get the date X days in the future
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        # format the date as YYYY-MM-DD
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        ec.create_tags(
            Resources=to_tag[retention_days],
            Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
            ]
        )

    iam = boto3.client('iam')
    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    account_ids = [AccountId]
    snapshot_response = ec.describe_snapshots(OwnerIds=account_ids, Filters=filters)
    for snap in snapshot_response['Snapshots']:
        print ("Deleting snapshot %s" % snap['SnapshotId'])
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
