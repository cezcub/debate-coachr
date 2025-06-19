#!/bin/bash

# Azure Deployment Script for Coachr AI (Cloud Build Version)
# This version uses Azure Container Registry build tasks instead of local Docker builds
# Run this script to deploy the application to Azure Container Apps

set -e

# Configuration
RESOURCE_GROUP="coachr-ai-rg"
LOCATION="eastus"
ACR_NAME="coachraiacr"
CONTAINER_APP_NAME="coachr-ai-app"
CONTAINER_ENV_NAME="coachr-ai-env"
IMAGE_NAME="coachr-ai"
IMAGE_TAG="latest"

echo "Starting Azure deployment for Coachr AI (Cloud Build)..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI is not installed. Please install it first:"
    echo "   brew install azure-cli"
    exit 1
fi

# Check if user is logged in to Azure
if ! az account show &> /dev/null; then
    echo "Please log in to Azure first:"
    echo "   az login"
    exit 1
fi

# Check required environment variables
if [[ -z "$AZURE_OPENAI_API_KEY" ]]; then
    echo "AZURE_OPENAI_API_KEY environment variable is required"
    echo "   export AZURE_OPENAI_API_KEY='your-api-key'"
    exit 1
fi

if [[ -z "$AZURE_OPENAI_ENDPOINT" ]]; then
    echo "AZURE_OPENAI_ENDPOINT environment variable is required"
    echo "   export AZURE_OPENAI_ENDPOINT='your-endpoint'"
    exit 1
fi

echo "Prerequisites checked successfully"

# Step 1: Create Resource Group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION || echo "Resource group already exists"

# Step 2: Create Azure Container Registry
echo "Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true || echo "ACR already exists"

# Step 3: Get ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)
echo "ACR Login Server: $ACR_LOGIN_SERVER"

# Step 4: Build image using Azure Container Registry build tasks (no local Docker required)
echo "Building Docker image in Azure (this may take a few minutes)..."
az acr build --registry $ACR_NAME --image $IMAGE_NAME:$IMAGE_TAG --file deployment/docker/Dockerfile .

echo "Image built and pushed to ACR successfully"

# Step 5: Create Container Apps environment
echo "Creating Container Apps environment..."
az containerapp env create \
  --name $CONTAINER_ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION || echo "Environment already exists"

# Step 6: Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Step 7: Deploy Container App
echo "Deploying Container App..."
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_ENV_NAME \
  --image $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8501 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 5 \
  --cpu 2.0 \
  --memory 4.0Gi \
  --secrets azure-openai-key="$AZURE_OPENAI_API_KEY" \
  --env-vars AZURE_OPENAI_API_KEY=secretref:azure-openai-key AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT"

# Step 8: Get the application URL
APP_URL=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)

echo "Deployment completed successfully!"
echo "Your application is available at: https://$APP_URL"
echo ""
echo "Next steps:"
echo "1. Test your application at the URL above"
echo "2. Configure custom domain (optional)"
echo "3. Set up monitoring and alerts"
echo "4. Configure CI/CD pipeline"
