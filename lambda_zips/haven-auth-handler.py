import json
import uuid

def lambda_handler(event, context):
    try:
        path = event.get('rawPath', '')
        if '/auth/login' in path or '/auth/signup' in path:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
                },
                'body': json.dumps({'token': 'mock-jwt-token-12345'})
            }
        elif '/auth/profile' in path:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
                },
                'body': json.dumps({'user_id': str(uuid.uuid4()), 'email': 'test@example.com'})
            }
        
        return {'statusCode': 404, 'body': 'Not Found'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
