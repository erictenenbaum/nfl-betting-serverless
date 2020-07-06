import boto3
import json
import os

# aws boto3 config for S3 and DynamoDB connection
session = boto3.Session(aws_access_key_id=os.getenv('ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
dynamodb = session.resource('dynamodb')
s3 = boto3.client('s3', aws_access_key_id=os.getenv('ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
# dynamodb = boto3.client('dynamodb', aws_access_key_id=os.getenv('ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))


# lambda that gets triggered when .json file is uploaeded to /clean-data path.
# function bulk uploads the list of data to specified dynamo table with boto3 batch_writer
# batch_writer handles the 25 BatchWriteItem limit for you
def upload_data(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3_json_obj = s3.get_object(Bucket=bucket, Key=key)
    s3_json_data = s3_json_obj['Body'].read().decode('utf-8')
    json_data = json.loads(s3_json_data)
    table = dynamodb.Table(json_data['DynamoDB_Table'])
    with table.batch_writer() as batch:
        for document in json_data['data']:
            batch.put_item(Item=document)

    return {
        "statusCode": 200,
        "body": {
            "message": "success!"
        }
    }







