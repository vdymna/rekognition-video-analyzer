import urllib
import boto3


def start_processing_video(event, context):
    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'], 
            urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return

def start_label_detection(bucket_name, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={
            'S3Object': { 
                'Bucket': bucket_name, 
                'Name': key 
            }
        })
    
    return
