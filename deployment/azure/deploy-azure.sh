#!/bin/bash

# Azure Deployment Script for Coachr AI
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

echo "🚀 Starting Azure deployment for Coachr AI..."

# Step 1: Create Resource Group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 2: Create Azure Container Registry
echo "🏗️ Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Step 3: Get ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)
echo "📝 ACR Login Server: $ACR_LOGIN_SERVER"

# Step 4: Build and push Docker image
echo "🔨 Building Docker image..."
docker build -t $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG .

echo "📤 Pushing image to ACR..."
az acr login --name $ACR_NAME
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG

# Step 5: Create Container Apps environment
echo "🌍 Creating Container Apps environment..."
az containerapp env create \
  --name $CONTAINER_ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Step 6: Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Step 7: Deploy Container App
echo "🚀 Deploying Container App..."
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

echo "✅ Deployment completed successfully!"
echo "🌐 Your application is available at: https://$APP_URL"
echo ""
echo "📋 Next steps:"
echo "1. Test your application at the URL above"
echo "2. Configure custom domain (optional)"
echo "3. Set up monitoring and alerts"
echo "4. Configure CI/CD pipeline"
