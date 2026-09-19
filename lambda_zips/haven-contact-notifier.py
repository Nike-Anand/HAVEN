import json
import boto3

def lambda_handler(event, context):
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'Notified'})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
