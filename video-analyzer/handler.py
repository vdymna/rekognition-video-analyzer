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

        label_detection_data = get_label_detection_data(job_id)
        video_labels = transform_data(label_detection_data, s3_bucket, s3_object)

        put_labels_in_db(video_labels)


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


def get_label_detection_data(job_id):
    """Get rekognition label detection data by job id."""
    rekognition_client = boto3.client('rekognition')
    
    response_data = rekognition_client.get_label_detection(JobId=job_id)
    next_token = response_data.get('NextToken', None)

    while next_token:
        next_page_data = rekognition_client.get_label_detection(JobId=job_id, NextToken=next_token)
        next_token = next_page_data.get('NextToken', None)
        
        response_data['Labels'].extend(next_page_data['Labels'])

    return response_data


def transform_data(labels_data, s3_bucket, s3_object):
    """Transform video labels data for DynamoDB."""
    del labels_data['JobStatus']
    del labels_data['NextToken']
    del labels_data['ResponseMetadata']

    labels_data['VideoName'] = s3_object
    labels_data['VideoBucket'] = s3_bucket
    
    labels_data = recursive_format_item(labels_data)

    return labels_data


def recursive_format_item(data):
    """Recursively convert all floats to string value in the data dictionary."""
    if isinstance(data, dict):
        return { k: recursive_format_item(v) for k, v in data.items() }

    if isinstance(data, list):
        return [ recursive_format_item(v) for v in data ]

    if isinstance(data, float):
        return str(data)

    return data


def put_labels_in_db(labels_data):
    """Save data to DynamoDB table."""
    dynamodb = boto3.resource('dynamodb')
    
    print(labels_data)
    
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    videos_table = dynamodb.Table(table_name)
    videos_table.put_item(labels_data)
