import json
import boto3
from botocore.exceptions import ClientError

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = "anthropic.claude-instant-v1"

def lambda_handler(event, context):
    try:
        # Get message from frontend (query param)
        message = event['queryStringParameters']['q']

        # Claude format - general helpful assistant
        prompt = f"Human: You are a helpful assistant. Please provide a friendly and helpful response to the user.\n\nUser: {message}\n\nAssistant:"

        body = {
            "prompt": prompt,
            "max_tokens_to_sample": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]
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