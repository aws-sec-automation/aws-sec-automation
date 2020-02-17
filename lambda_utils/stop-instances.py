import json
import boto3
def lambda_handler(event, context):
    # TODO implement
    ec = boto3.client('ec2')

    reservations = ec.describe_instances(
            Filters=[
                {'Name': 'tag:Env', 'Values': ['pruebas', 'Pruebas']},
            ]
        )['Reservations']
    ids=[]
    for r in reservations:
        instances=r['Instances']
        instances_ids = [d['InstanceId'] for d in instances]
        ids.extend(instances_ids)

    ec.stop_instances(
        InstanceIds=ids
    )

    return {
        'statusCode': 200,
        'body': json.dumps('ok')
    }
