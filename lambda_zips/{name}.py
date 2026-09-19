import json
import boto3

def lambda_handler(event, context):
    headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type,Authorization', 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'}
    if event.get('requestContext', {}).get('http', {}).get('method', '') == 'OPTIONS': return {'statusCode': 200, 'headers': headers, 'body': ''}
    try:
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'status': 'Notified', 'contacts': []})}
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}
