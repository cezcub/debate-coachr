# 🚀 Quick Start: Deploy Coachr AI to Azure

## 📋 Prerequisites

1. **Azure Account** with active subscription
2. **Azure CLI** installed and configured
3. **Docker** installed on your local machine
4. **Git** for version control
5. **Azure OpenAI** service set up and working

## ⚡ Quick Deployment (15 minutes)

### Step 1: Prepare Environment Variables
```bash
export AZURE_OPENAI_API_KEY="your-api-key-here"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
```

### Step 2: Test Locally (Optional but Recommended)
```bash
# Test the application with Docker
./test-local.sh

# Visit http://localhost:8501 to verify everything works
# Stop the test container when done:
docker stop coachr-ai-test && docker rm coachr-ai-test
```

### Step 3: Deploy to Azure
```bash
# Login to Azure
az login

# Run the deployment script
./deploy-azure.sh
```

### Step 4: Access Your Application
The script will output your application URL:
```
✅ Deployment completed successfully!
🌐 Your application is available at: https://your-app-url.azurecontainerapps.io
```

## 🛠️ Manual Deployment Steps

If you prefer to deploy manually or customize the process:

### 1. Create Azure Resources
```bash
# Create resource group
az group create --name coachr-ai-rg --location eastus

# Create container registry
az acr create --resource-group coachr-ai-rg --name coachraiacr --sku Basic --admin-enabled true

# Create container environment
az containerapp env create --name coachr-ai-env --resource-group coachr-ai-rg --location eastus
```

### 2. Build and Push Container
```bash
# Get ACR login server
ACR_SERVER=$(az acr show --name coachraiacr --resource-group coachr-ai-rg --query loginServer --output tsv)

# Build image
docker build -t $ACR_SERVER/coachr-ai:latest .

# Login and push
az acr login --name coachraiacr
docker push $ACR_SERVER/coachr-ai:latest
```

### 3. Deploy Container App
```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name coachraiacr --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name coachraiacr --query passwords[0].value --output tsv)

# Deploy application
az containerapp create \
  --name coachr-ai-app \
  --resource-group coachr-ai-rg \
  --environment coachr-ai-env \
  --image $ACR_SERVER/coachr-ai:latest \
  --registry-server $ACR_SERVER \
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
```

## 🔄 Setting Up CI/CD

### 1. GitHub Secrets
Add these secrets to your GitHub repository:
- `AZURE_CREDENTIALS`: Azure service principal credentials
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint

### 2. Create Azure Service Principal
```bash
az ad sp create-for-rbac --name "coachr-ai-sp" --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/coachr-ai-rg \
  --sdk-auth
```

Copy the JSON output to GitHub secrets as `AZURE_CREDENTIALS`.

### 3. Enable Auto-Deployment
The `.github/workflows/deploy.yml` file is already configured. Push to the `main` branch to trigger automatic deployment.

## 📊 Monitoring and Management

### View Application Logs
```bash
az containerapp logs show --name coachr-ai-app --resource-group coachr-ai-rg --follow
```

### Scale the Application
```bash
az containerapp update --name coachr-ai-app --resource-group coachr-ai-rg \
  --min-replicas 2 --max-replicas 10
```

### Update Environment Variables
```bash
az containerapp update --name coachr-ai-app --resource-group coachr-ai-rg \
  --set-env-vars NEW_VAR=value
```

## 🚨 Troubleshooting

### Common Issues

**Container fails to start:**
- Check logs: `az containerapp logs show --name coachr-ai-app --resource-group coachr-ai-rg`
- Verify environment variables are set correctly
- Ensure Azure OpenAI credentials are valid

**High startup time:**
- The Whisper model loading can take 30+ seconds
- Consider using a smaller model for faster startup
- Increase memory allocation if needed

**Out of memory errors:**
- Increase memory: `--memory 8.0Gi`
- Optimize Whisper model size
- Implement model caching

### Performance Optimization

**For faster cold starts:**
1. Use smaller Whisper models
2. Pre-download models in Docker build
3. Implement application-level caching

**For better scalability:**
1. Increase max replicas
2. Use Azure Front Door for global distribution
3. Implement database for session persistence

## 💰 Cost Management

### Monitor Costs
- Set up Azure Cost Management alerts
- Monitor container app metrics
- Use spot instances for development

### Optimization Tips
- Use minimum replicas = 0 for development
- Schedule scaling based on usage patterns
- Consider Azure Functions for infrequent usage

## 🔒 Security Best Practices

### Implemented Security Features
- Non-root container user
- Secrets stored in Azure Key Vault
- Network security groups
- HTTPS-only access

### Additional Security
- Set up Web Application Firewall (WAF)
- Implement rate limiting
- Add authentication (Azure AD B2C)
- Regular security scanning

## 📈 Next Steps

1. **Custom Domain**: Configure your own domain name
2. **SSL Certificate**: Set up custom SSL certificates
3. **Monitoring**: Configure Application Insights
4. **Backup**: Set up automated backups
5. **User Management**: Add authentication and user accounts
6. **Database**: Add persistent storage for user data
7. **CDN**: Configure Azure CDN for global performance

## 📞 Support

- **Azure Documentation**: https://docs.microsoft.com/azure/container-apps/
- **GitHub Issues**: Report issues in the repository
- **Azure Support**: Use Azure portal for infrastructure issues

---

**🎉 Congratulations! Your Coachr AI application is now running on Azure!**
