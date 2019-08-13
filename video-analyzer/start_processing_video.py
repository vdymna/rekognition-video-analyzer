import os
import urllib
import boto3


def handler(event, context):
    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'], 
            urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return


def start_label_detection(bucket_name, key):
    """Start rekognition label detection for S3 object."""
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={
            'S3Object': { 
                'Bucket': bucket_name, 
                'Name': key 
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
        })
    
    return