import json
import boto3
from datetime import datetime
import os

# DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FileUploads')

# SNS client
sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']# use environment variables


def lambda_handler(event, context):
    # Extract S3 info from event
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        object_size = record['s3']['object']['size']
        event_time = record['eventTime']  # ISO 8601 timestamp

        # File type detection
        file_extension = object_key.split('.')[-1].lower()

        # Format timestamp
        try:
            upload_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()
        except ValueError:
            # fallback if microseconds not present
            upload_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%SZ').isoformat()

        # Store metadata in DynamoDB with error handling
        try:
            table.put_item(
                Item={
                    'file_name': object_key,
                    'bucket_name': bucket_name,
                    'size_bytes': object_size,
                    'upload_time': upload_time,
                    'file_type': file_extension
                }
            )
        except Exception as e:
            print(f"Error writing to DynamoDB: {e}")

        # Send SNS notification with error handling
        message = f"New file uploaded: {object_key} ({object_size} bytes) in bucket {bucket_name}"
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="File Upload Notification"
            )
        except Exception as e:
            print(f"Error publishing SNS: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('File processed successfully!')
    }
