import json
import boto3
from botocore.exceptions import ClientError

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = "mistral.mixtral-8x7b-instruct-v0:1"

def lambda_handler(event, context):
    try:
        # Get message from frontend (query param)
        message = event['queryStringParameters']['q']

        # Very simple prompt
        prompt = f"Hello! I'm here to chat with you. What's on your mind?\n\nUser: {message}\nAssistant:"

        body = {
            "prompt": prompt,
            "max_tokens": 500,
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
        reply = result['outputs'][0]['text'].strip()
        
        # Clean up the response
        if reply.startswith('User:'):
            reply = reply.split('Assistant:')[-1].strip()
        if reply.startswith('Bot:'):
            reply = reply.split('Bot:')[-1].strip()

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'reply': reply})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}