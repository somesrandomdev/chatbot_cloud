import json
import boto3
from botocore.exceptions import ClientError
import re

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = "mistral.mixtral-8x7b-instruct-v0:1"

def lambda_handler(event, context):
    try:
        # Get message from frontend (query param)
        message = event['queryStringParameters']['q']

        # Very simple prompt
        prompt = f"User: {message}\nAssistant:"

        body = {
            "prompt": prompt,
            "max_tokens": 300,
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
        
        # Clean up the response - remove User:, Bot:, Assistant: markers
        reply = re.sub(r'^(User:|Bot:|Assistant:)\s*', '', reply)
        reply = re.sub(r'\s*(User:|Bot:|Assistant:)\s*', ' ', reply)
        
        # Remove any repeated words or phrases
        reply = re.sub(r'\b(\w+)\s+\1\b', r'\1', reply)
        
        # Final cleanup - take first meaningful sentence
        sentences = reply.split('.')
        if len(sentences) > 0:
            reply = sentences[0].strip()
            if not reply.endswith('.'):
                reply += '.'

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'reply': reply})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}