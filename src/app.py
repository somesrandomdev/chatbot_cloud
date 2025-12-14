import json
import boto3
from botocore.exceptions import ClientError

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = "anthropic.claude-instant-v1"

def lambda_handler(event, context):
    try:
        # Get message from frontend (query param)
        message = event['queryStringParameters']['q']

        # Simple conversational format
        prompt = f"Hello! How can I help you today?\n\nUser: {message}\n\nAssistant:"

        body = {
            "prompt": prompt,
            "max_tokens_to_sample": 1000,
            "temperature": 0.7,
            "top_p": 0.9
        }

        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType='application/json',
            accept='application/json'
        )

        result = json.loads(response['body'].read())
        reply = result['completion'].strip()

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'reply': reply})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}