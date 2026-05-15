This Markdown guide covers the complete Docker lifecycle for your image processing project, from writing the `Dockerfile` to pushing it to **Amazon ECR**.

---

# <PROJECT_NAME>: Docker & ECR Lifecycle Guide

A comprehensive reference for containerizing Python applications and hosting them on **Amazon Elastic Container Registry (ECR)**.

## 1. Dockerfile Format & Syntax
The `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image.

### Recommended `Dockerfile` for Python
```dockerfile
# 1. Base Image: Use a lightweight version of Python
FROM python:3.11-slim

# 2. Set Working Directory: All subsequent commands run here
WORKDIR /app

# 3. Install System Dependencies (Required for Pillow/Image processing)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy Requirements first (Optimizes Docker layer caching)
COPY requirements.txt .

# 5. Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
COPY . .

# 7. Entry Point: The command to run your script
CMD ["python", "app.py"]
```

### Common Dockerfile Instructions
* **`FROM`**: Defines the parent image (e.g., `python:3.9`, `alpine`, `ubuntu`).
* **`WORKDIR`**: Sets the "home" folder inside the container.
* **`COPY`**: Moves files from your local machine into the container.
* **`RUN`**: Executes commands during the build phase (e.g., installing packages).
* **`ENV`**: Sets environment variables inside the container.
* **`CMD`**: The default command that runs when the container starts.

---

## 2. Docker CLI: Build & Local Testing
Before pushing to the cloud, ensure the image builds and runs locally.

```bash
# Build the image
docker build -t <IMAGE_NAME> .

# List local images to verify
docker images

# Run the container locally (for testing)
docker run --env-file .env <IMAGE_NAME>
```
* `<IMAGE_NAME>`: The name of your local image (e.g., `image-proc`).

---

## 3. Pushing to Amazon ECR
To push to AWS, you must authenticate your local Docker client to your private ECR registry.

### Step 1: Authenticate
```bash
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```

### Step 2: Create Repository (If it doesn't exist)
```bash
aws ecr create-repository --repository-name <IMAGE_NAME> --region <REGION>
```

### Step 3: Tag and Push
```bash
# Tag the local image to match the ECR URI
docker tag <IMAGE_NAME>:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<IMAGE_NAME>:latest

# Push to AWS
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<IMAGE_NAME>:latest
```
* `<AWS_ACCOUNT_ID>`: Your 12-digit AWS Account ID.
* `<REGION>`: The AWS region (e.g., `ap-south-1`).

---

## 4. Troubleshooting & Common Issues

| Issue | Potential Cause | Resolution Technique |
| :--- | :--- | :--- |
| **`Exec format error`** | Building on Mac M1/M2 (ARM) but deploying to Linux (AMD64). | Build using: `docker buildx build --platform linux/amd64 -t <IMAGE_NAME> .` |
| **`ModuleNotFoundError`** | Dependency missing from `requirements.txt`. | Add the module to `requirements.txt` and rebuild the image. |
| **`Permission Denied` (Docker)** | Docker daemon not running or user lacks permissions. | Run `sudo service docker start` or add your user to the `docker` group. |
| **`Retrying in X seconds` during push** | ECR Authentication has expired (tokens last 12 hours). | Re-run the `aws ecr get-login-password` authentication command. |
| **Large Image Size** | Using a heavy base image or not cleaning up cache. | Use `python:slim` or `python:alpine` and combine `RUN` commands to reduce layers. |
| **`No space left on device`** | Too many old images/containers taking up disk space. | Run `docker system prune -a` to wipe unused data. |



---

### **Final Tip for Success**
Always use a **`.dockerignore`** file in your project root. Add entries like `__pycache__`, `.git`, and `.env` to prevent sensitive or unnecessary files from being baked into your image.

```plaintext
# Git
.git
.gitignore

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Python build artifacts
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.venv/
venv/
ENV/
env/
bin/
include/
lib/

# Environment variables and secrets
.env
.venv
*.env
*.secrets
auth.json

# IDEs and editors
.vscode/
.idea/
*.swp
*.swo
.project
.pydevproject
.settings/

# Testing and coverage
.pytest_cache/
.tox/
.nox/
.coverage
.cache
nosetests.xml
coverage.xml
*.cover
*.log

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```