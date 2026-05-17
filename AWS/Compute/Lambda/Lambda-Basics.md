# AWS Lambda Basics

AWS Lambda is a serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers.

## Core Architecture & Programming Model

### Function Handler
The specific method or function in your code that AWS Lambda executes when the function is invoked.

- **How it works**: When a Lambda function is triggered, the execution environment looks for the handler (specified during configuration, e.g., `index.handler` in Node.js or `lambda_function.lambda_handler` in Python). The handler function typically takes an `event` object (containing the invocation payload data) and a `context` object (containing runtime metadata) as arguments.
- **Purpose**: It serves as the primary entry point for your serverless application logic.

**Code Example (Python):**
```python
# The lambda_handler is the configured entry point
def lambda_handler(event, context):
    # Process the incoming event data
    name = event.get('name', 'World')
    
    return {
        'statusCode': 200,
        'body': f"Hello, {name}!"
    }
```

### Execution Environment
The isolated runtime microVM (built on Firecracker) where your code executes, managing resources, dependencies, and environment variables.

- **How it works**: When Lambda receives a request, it automatically provisions a secure, highly isolated execution environment using Firecracker microVMs. It downloads your deployment package, initializes the specific runtime (like Python, Java, or Node.js), runs the initialization code (anything defined outside the handler), and finally executes the handler itself.
- **Cold vs. Warm Starts**: 
  - *Cold Start*: When Lambda creates a brand-new execution environment (e.g., after an update or scaling up due to high traffic), resulting in slightly higher latency.
  - *Warm Start*: When Lambda reuses a previously spun-up execution environment for a new request, resulting in near-instant execution.

### Deployment Packages
The two formats used to package function code: `.zip` file archives or container images (up to 10 GB) conforming to the OCI specification.

- **.zip File Archives**: The traditional and most common way to deploy Lambda functions. You compress your code and any specific dependencies into a single ZIP file. (Limits: 50 MB zipped, 250 MB unzipped).
- **Container Images**: You can package your code and dependencies as a Docker container image (up to 10 GB). This format is ideal for machine learning workloads, heavy binary dependencies, or organizations already using standard container tooling (CI/CD). Lambda provides base images for standard runtimes.

**CLI Commands:**
```bash
# Update function code using a .zip file
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://my-deployment-package.zip

# Update function code using a container image deployed to ECR
aws lambda update-function-code \
    --function-name my-function \
    --image-uri 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-lambda-image:latest
```

### Lambda Layers
A distribution mechanism to centrally manage and share common code, libraries, or custom runtimes across multiple Lambda functions without bloating deployment packages.

- **How it works**: You package libraries, custom runtimes, or other dependencies into a ZIP file and upload it as a Layer. When you attach this Layer to a Lambda function, the contents are dynamically extracted into the `/opt` directory in the execution environment during runtime.
- **Benefits**: 
  - Keeps deployment packages small, making deployments faster and allowing you to use the inline AWS console code editor.
  - Promotes code reuse (e.g., centrally managing a database connection library or the AWS SDK across hundreds of microservices).
  - You can include up to 5 layers per Lambda function.

**CLI Commands:**
```bash
# Publish a new layer version
aws lambda publish-layer-version \
    --layer-name my-shared-lib \
    --description "Common database and logging utilities" \
    --zip-file fileb://layer.zip

# Attach a layer to an existing Lambda function
aws lambda update-function-configuration \
    --function-name my-function \
    --layers arn:aws:lambda:us-east-1:123456789012:layer:my-shared-lib:1
```
