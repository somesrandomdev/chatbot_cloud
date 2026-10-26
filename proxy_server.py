from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def chat():
    q = request.args.get('q')
    if not q:
        return jsonify({'error': 'No query provided'}), 400
    
    # Forward the request to the AWS API Gateway endpoint
    aws_api_url = 'https://rrryzcultj.execute-api.us-east-1.amazonaws.com/prod'
    print(f"Forwarding request to: {aws_api_url}?q={q}")
    try:
        response = requests.get(f'{aws_api_url}?q={q}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)