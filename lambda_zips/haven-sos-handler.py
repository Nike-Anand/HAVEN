import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('user_id', 'unknown')
        location = body.get('location', {})
        
        sos_id = str(uuid.uuid4())
        sos_table = dynamodb.Table('haven_sos_events')
        sos_table.put_item(Item={
            'sos_id': sos_id,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat(),
            'location': location,
            'status': 'active'
        })
        
        return {
            'statusCode': 200,
            'body': json.dumps({'sos_id': sos_id, 'status': 'activated'})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
