import os
import urllib
import json
import boto3


# first handler
def start_processing_video(event, context):
    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'], 
            urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return

# second handler
def handle_label_detection(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        
        job_id = message['JobId']
        s3_bucket = message['Video']['S3ObjectName']
        s3_object = message['Video']['S3Bucket']

        labels_data = get_video_labels(job_id)
        put_labels_in_db(labels_data, s3_bucket, s3_object)


def start_label_detection(bucket_name, key):
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
    
    return response


def get_video_labels(job_id):
    pass


def put_labels_in_db(labels_data, s3_bucket, s3_object):
    pass
