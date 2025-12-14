# AI Chat Assistant

A modern, responsive AI-powered chatbot built with HTML, CSS, JavaScript, and AWS Lambda. Features a sleek UI design and integrates with Mistral AI through AWS Bedrock for natural language processing.

## 🌟 Features

- **Modern UI/UX**: Gradient design with smooth animations and typing indicators
- **AI-Powered**: Uses Mistral AI via AWS Bedrock for intelligent responses
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Chat**: Instant messaging with loading animations
- **Error Handling**: Graceful error handling with user-friendly messages
- **Cross-Origin Support**: Configured for web deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   AWS Lambda    │    │  AWS Bedrock    │
│   (HTML/CSS/JS) │───▶│   (Python)      │───▶│  (Mistral AI)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────▶│   Amplify       │◀─────────────┘
                         │   Hosting       │
                         └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- AWS Account with Bedrock access
- AWS CLI configured
- Amplify CLI (optional, for local development)

### Deployment Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/somesrandomdev/chatbot_cloud.git
   cd chatbot_cloud/deepseek-chatbot
   ```

2. **Deploy to AWS Amplify**
   - Connect your GitHub repository to AWS Amplify
   - Select the `main` branch
   - Amplify will automatically build and deploy using `amplify.yml`

3. **Configure Lambda Environment**
   - Update the `API_URL` in `index.html` with your deployed Lambda endpoint
   - Ensure your Lambda function has proper IAM permissions for Bedrock

## 📁 Project Structure

```
deepseek-chatbot/
├── index.html          # Main frontend interface
├── amplify.yml         # Amplify deployment configuration
├── requirements.txt    # Python dependencies
├── src/
│   └── app.py         # Lambda function code
└── amplify/           # Amplify project configuration
    ├── backend/       # Backend resources
    └── #current-cloud-backend/
```

## 💻 Code Explanation

### Frontend (`index.html`)

The frontend is a single-page application with:

#### HTML Structure
- **Chat Container**: Main chat interface with header, messages area, and input
- **Header**: Displays the app title and AI model information
- **Messages Area**: Scrollable container for chat messages
- **Input Section**: Text input and send button

#### CSS Styling
```css
/* Modern gradient background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Chat bubble animations */
.msg {
    animation: fadeIn 0.3s ease-in;
}

/* Typing indicator */
.typing-dot {
    animation: typing 1.4s ease-in-out infinite;
}
```

#### JavaScript Functionality
- **Message Handling**: `addMsg()` function for adding messages to chat
- **API Communication**: `send()` function for sending messages to Lambda
- **Real-time Updates**: Automatic scrolling and loading states
- **Error Handling**: Graceful error messages for API failures

### Backend (`src/app.py`)

The Lambda function handles AI request processing:

#### Key Components

**1. AWS Bedrock Integration**
```python
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = "mistral.mixtral-8x7b-instruct-v0:1"
```

**2. Request Processing**
```python
def lambda_handler(event, context):
    # Extract message from query parameters
    message = event['queryStringParameters']['q']
    
    # Prepare prompt for Mistral AI
    prompt = f"User: {message}\nAssistant:"
    
    # Invoke model with configuration
    body = {
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9
    }
```

**3. Response Cleaning**
```python
# Remove malformed markers and clean response
reply = re.sub(r'^(User:|Bot:|Assistant:)\s*', '', reply)
reply = re.sub(r'\s*(User:|Bot:|Assistant:)\s*', ' ', reply)
```

**4. CORS Headers**
```python
return {
    'statusCode': 200,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': json.dumps({'reply': reply})
}
```

### Deployment Configuration (`amplify.yml`)

The `amplify.yml` file configures the deployment process:

```yaml
version: 1
applications:
  - appRoot: .
    frontend:
      phases:
        preBuild:
          commands:
            - echo "Starting deployment"
        build:
          commands:
            - echo "Static site ready"
      artifacts:
        baseDirectory: .
        files:
          - '**/*'
      cache:
        paths: []
```

## 🔧 Configuration

### Environment Variables

Update these values in your deployment:

1. **API_URL** in `index.html`:
   ```javascript
   const API_URL = 'https://your-lambda-url.execute-api.region.amazonaws.com/prod/chat';
   ```

2. **AWS Region** in `app.py`:
   ```python
   bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
   ```

### AWS Permissions

Ensure your Lambda execution role has these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:region::model/mistral/mixtral-8x7b-instruct-v0:1"
        }
    ]
}
```

## 🛠️ Local Development

### Running Locally

1. **Setup Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Test Lambda Function**
   ```python
   # Run src/app.py directly
   python src/app.py
   ```

3. **Serve Frontend**
   ```bash
   # Using Python's built-in server
   python -m http.server 8000
   
   # Or using Node.js
   npx serve .
   ```

### Testing the Chatbot

1. Open `index.html` in a browser
2. Type a message and click Send
3. Check browser console for any errors
4. Verify Lambda logs in AWS CloudWatch

## 🐛 Troubleshooting

### Common Issues

**1. IAM Role Permissions Error**
```
ERROR: Unable to assume specified IAM Role
```
**Solution**: Check Amplify project IAM role permissions in AWS Console

**2. CORS Errors**
```
Access to fetch blocked by CORS policy
```
**Solution**: Verify CORS headers in Lambda function response

**3. Lambda Timeout**
```
Task timed out after 30.00 seconds
```
**Solution**: Reduce `max_tokens` or optimize prompt

**4. Bedrock Model Access**
```
AccessDeniedException: User is not authorized to perform bedrock:InvokeModel
```
**Solution**: Request model access in AWS Bedrock console

### Debug Steps

1. **Check CloudWatch Logs**
   ```bash
   aws logs filter-log-events --log-group-name /aws/lambda/your-function-name
   ```

2. **Test API Endpoint**
   ```bash
   curl -X GET "https://your-api-url?q=Hello"
   ```

3. **Verify Environment Variables**
   - Check Lambda console for environment variables
   - Confirm API_URL in frontend matches deployed endpoint

## 📊 Performance

- **Response Time**: ~2-5 seconds per message
- **UI Load Time**: <1 second
- **Memory Usage**: ~128MB Lambda allocation
- **Supported Models**: Mistral AI, Claude, Titan (configurable)

## 🔒 Security

- **CORS**: Configured for web access
- **IAM**: Principle of least privilege for Lambda role
- **API Keys**: No hardcoded credentials
- **Input Validation**: Basic sanitization in response cleaning

## 📈 Future Enhancements

- [ ] Add conversation history
- [ ] Implement user authentication
- [ ] Add file upload support
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Custom model fine-tuning
- [ ] Analytics and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Mistral AI** for the powerful language model
- **AWS** for cloud infrastructure and Bedrock service
- **Amplify** for seamless deployment and hosting
- **Open Source Community** for inspiration and tools

---

**Live Demo**: [https://main.d1o1mxplv0h3ig.amplifyapp.com](https://main.d1o1mxplv0h3ig.amplifyapp.com)

**Support**: For issues and questions, please open a GitHub issue or contact the development team.