# BrightMart Catalog App — Deployment Documentation

**Author:** [Your Name]  
**Date:** March 29, 2026  
**Application:** BrightMart Product Catalog (Python Flask)  
**Cloud Provider:** AWS (ECS/Fargate)

---

## 1. Docker Container Creation & Local Testing

### 1.1 Application Overview

BrightMart Catalog is a Python Flask web application that displays a product catalog with six sample retail items. The app uses a responsive, modern dark-mode UI built with vanilla HTML/CSS and serves content on port 5000.

**Project structure:**

```
brightmart-app/
├── app.py                  # Flask application (routes, sample product data)
├── requirements.txt        # Python dependencies (Flask 3.1.0)
├── Dockerfile              # Container build instructions
├── .dockerignore           # Files excluded from Docker image
├── cloudformation.yaml     # AWS CloudFormation IaC template
└── templates/
    └── index.html          # Responsive product catalog UI
```

### 1.2 Dockerfile Explanation

The Dockerfile uses `python:3.11-slim` as the base image to keep the container lightweight. Dependencies are installed in a separate `COPY/RUN` step before copying application code, which leverages Docker's layer caching for faster rebuilds.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### 1.3 Build & Run Locally

```bash
# Build the Docker image
docker build -t brightmart-app .

# Run the container
docker run -p 5000:5000 brightmart-app
```

Open **http://localhost:5000** in a browser to verify. The catalog page should display six product cards with pricing and "Add to Cart" buttons.

**Screenshot:** *(Insert screenshot of running app here)*

---

## 2. Cloud Deployment (AWS ECS/Fargate)

### 2.1 Push Image to Amazon ECR

```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name brightmart-app --region us-east-1

# Tag and push the image
docker tag brightmart-app:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/brightmart-app:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/brightmart-app:latest
```

### 2.2 Deploy with CloudFormation (IaC)

```bash
aws cloudformation create-stack \
  --stack-name brightmart-stack \
  --template-body file://cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=AppImage,ParameterValue=<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/brightmart-app:latest
```

Wait for the stack to complete:

```bash
aws cloudformation wait stack-create-complete --stack-name brightmart-stack
```

### 2.3 Get Public URL

```bash
aws cloudformation describe-stacks --stack-name brightmart-stack \
  --query "Stacks[0].Outputs[?OutputKey=='ServiceURL'].OutputValue" --output text
```

Open the returned URL in a browser to verify the live deployment.

**Public URL:** *(Insert public URL here)*  
**Screenshot:** *(Insert screenshot of deployed app here)*

---

## 3. IaC Template Explanation

The `cloudformation.yaml` template provisions the following AWS resources:

| Resource | Purpose |
|---|---|
| **VPC + 2 Public Subnets** | Isolated network with internet access across two availability zones |
| **Internet Gateway + Route Table** | Enables outbound/inbound traffic to the public subnets |
| **ALB Security Group** | Allows inbound HTTP (port 80) from anywhere |
| **ECS Security Group** | Allows traffic from the ALB to container port 5000 only |
| **ECS Cluster** | Logical grouping for the Fargate service |
| **IAM Execution Role** | Grants ECS permission to pull images from ECR and write logs |
| **Task Definition** | Defines container image, CPU (256), memory (512 MB), and port mapping |
| **Application Load Balancer** | Routes public HTTP traffic to the ECS service |
| **ECS Service** | Runs 1 Fargate task and registers it with the ALB target group |
| **CloudWatch Log Group** | Captures container logs with 7-day retention |

---

## 4. Cleanup Instructions

```bash
# Delete CloudFormation stack (removes all provisioned resources)
aws cloudformation delete-stack --stack-name brightmart-stack
aws cloudformation wait stack-delete-complete --stack-name brightmart-stack

# Delete ECR repository and images
aws ecr delete-repository --repository-name brightmart-app --force --region us-east-1
```

Verify in the AWS Console that no ECS clusters, load balancers, or VPCs remain to avoid charges.

---

## 5. Lessons Learned

- **Docker layer caching**: Separating `COPY requirements.txt` from `COPY .` speeds up rebuilds when only application code changes.
- **Fargate simplicity**: Fargate eliminates the need to manage EC2 instances — AWS handles the underlying compute.
- **IaC benefits**: The entire infrastructure can be created or torn down with a single CLI command, ensuring consistency and easy cleanup.
- **Free-tier awareness**: The Fargate task uses 0.25 vCPU / 512 MB, which falls within AWS free-tier limits for new accounts.
