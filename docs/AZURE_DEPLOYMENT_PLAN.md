# 🚀 Azure Deployment Plan for Coachr AI

## 📋 Overview
Deploy the Coachr AI debate coaching application (Streamlit frontend + FastAPI backend) to Azure cloud infrastructure for production use.

## 🏗️ Current Application Architecture

### **Frontend:**
- **Streamlit** web application (`app.py`)
- Modern UI with chat interface
- File upload capabilities (audio/text)
- Real-time AI feedback display

### **Backend:**
- **FastAPI** server (`backend/backend.py`)
- Audio transcription with Whisper
- Text processing endpoints
- Live chat API with Azure OpenAI
- File handling for uploads

### **Dependencies:**
- Azure OpenAI integration
- Whisper for audio transcription
- Heavy ML dependencies (torch, transformers)
- Audio processing libraries (pydub)

## 🎯 Deployment Strategy Options

### **Option 1: Azure Container Apps (Recommended)**
✅ **Best for**: Scalable, managed containerized applications
- Automatic scaling based on demand
- Built-in load balancing
- Integrated with Azure services
- Cost-effective pay-per-use model

### **Option 2: Azure App Service**
✅ **Best for**: Traditional web applications
- Easy deployment from GitHub
- Built-in CI/CD pipelines
- Custom domains and SSL certificates
- May struggle with large ML dependencies

### **Option 3: Azure Virtual Machines**
✅ **Best for**: Full control over environment
- Complete customization
- Handle any dependency requirements
- More complex management required

**🏆 RECOMMENDATION: Azure Container Apps** - Best balance of scalability, cost, and ease of management for this ML-heavy application.

## 📈 Step-by-Step Deployment Plan

### **Phase 1: Application Preparation** (1-2 days)

#### Step 1.1: Containerization
- [ ] Create `Dockerfile` for the combined application
- [ ] Create `docker-compose.yml` for local testing
- [ ] Optimize dependencies for production
- [ ] Test container builds locally

#### Step 1.2: Configuration Management
- [ ] Create production-ready environment configuration
- [ ] Set up Azure Key Vault for secrets management
- [ ] Update environment variable loading for cloud deployment
- [ ] Create health check endpoints

#### Step 1.3: Code Optimization
- [ ] Separate frontend and backend into different containers (optional)
- [ ] Optimize Whisper model loading for faster startup
- [ ] Add proper logging and monitoring
- [ ] Implement graceful error handling for production

### **Phase 2: Azure Infrastructure Setup** (1 day)

#### Step 2.1: Resource Group Creation
```bash
# Create resource group
az group create --name coachr-ai-rg --location eastus
```

#### Step 2.2: Container Registry Setup
```bash
# Create Azure Container Registry
az acr create --resource-group coachr-ai-rg --name coachrai --sku Basic
```

#### Step 2.3: Azure Container Apps Environment
```bash
# Create Container Apps environment
az containerapp env create \
  --name coachr-ai-env \
  --resource-group coachr-ai-rg \
  --location eastus
```

#### Step 2.4: Storage and Database (if needed)
- [ ] Set up Azure Blob Storage for file uploads
- [ ] Consider Azure Database for user data (future)
- [ ] Configure backup and disaster recovery

### **Phase 3: Application Deployment** (1-2 days)

#### Step 3.1: Container Build and Push
```bash
# Build and push to Azure Container Registry
docker build -t coachrai.azurecr.io/coachr-ai:latest .
docker push coachrai.azurecr.io/coachr-ai:latest
```

#### Step 3.2: Deploy to Container Apps
```bash
# Deploy the container app
az containerapp create \
  --name coachr-ai-app \
  --resource-group coachr-ai-rg \
  --environment coachr-ai-env \
  --image coachrai.azurecr.io/coachr-ai:latest \
  --target-port 8501 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10
```

#### Step 3.3: Environment Variables and Secrets
- [ ] Configure Azure OpenAI credentials
- [ ] Set up application-specific environment variables
- [ ] Test secret access from the application

### **Phase 4: Production Configuration** (1 day)

#### Step 4.1: Custom Domain and SSL
- [ ] Configure custom domain (e.g., app.coachr-ai.com)
- [ ] Set up SSL certificates
- [ ] Configure DNS settings

#### Step 4.2: Scaling and Performance
- [ ] Configure auto-scaling rules
- [ ] Set up performance monitoring
- [ ] Optimize for cold start times

#### Step 4.3: Security and Compliance
- [ ] Configure network security groups
- [ ] Set up Web Application Firewall (WAF)
- [ ] Implement rate limiting
- [ ] Review data privacy compliance

### **Phase 5: Monitoring and CI/CD** (1-2 days)

#### Step 5.1: Monitoring Setup
- [ ] Configure Azure Application Insights
- [ ] Set up custom dashboards
- [ ] Create alerts for errors and performance issues
- [ ] Implement health checks

#### Step 5.2: CI/CD Pipeline
- [ ] Set up GitHub Actions for automatic deployment
- [ ] Create staging environment
- [ ] Implement automated testing
- [ ] Configure rollback procedures

## 📁 Required Files for Deployment

### **1. Dockerfile**
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8501 8000

# Create startup script
COPY start.sh .
RUN chmod +x start.sh

# Start both services
CMD ["./start.sh"]
```

### **2. start.sh**
```bash
#!/bin/bash
# Start FastAPI backend in background
uvicorn backend.backend:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### **3. requirements-prod.txt** (Optimized)
```txt
streamlit==1.40.1
fastapi==0.115.12
uvicorn==0.33.0
openai==1.70.0
openai-whisper==20240930
python-dotenv==1.0.0
requests==2.32.3
pydub==0.25.1
python-multipart==0.0.20
azure-identity==1.15.0
azure-keyvault-secrets==4.7.0
# Remove unnecessary heavy dependencies for production
```

### **4. .dockerignore**
```
__pycache__/
*.pyc
.env
.git/
*.md
unit_tests/
test_cases/
.DS_Store
temp_uploaded_audio.wav
```

## 💰 Cost Estimation

### **Azure Container Apps**
- **Basic tier**: ~$50-100/month for low-medium traffic
- **Production tier**: ~$200-500/month for high availability

### **Azure OpenAI**
- **Model usage**: Variable based on API calls
- **Estimated**: $100-300/month for moderate usage

### **Storage and Networking**
- **Blob Storage**: ~$10-20/month
- **Bandwidth**: ~$20-50/month

### **Total Estimated Cost: $180-870/month**

## 🚨 Critical Considerations

### **Performance Optimization**
- Whisper model loading can be slow (30+ seconds)
- Consider using smaller models for faster response
- Implement model caching strategies
- Use Azure Container Apps scaling to handle demand

### **Security Requirements**
- Secure API key management
- File upload size limits and validation
- Rate limiting to prevent abuse
- Data encryption in transit and at rest

### **Scalability Challenges**
- Large ML models consume significant memory
- Audio processing is CPU-intensive
- Consider GPU instances for heavy workloads
- Implement request queuing for high traffic

## 🛠️ Alternative Deployment Options

### **Hybrid Approach**
- **Frontend**: Azure Static Web Apps (cheaper)
- **Backend**: Azure Container Apps
- **ML Processing**: Azure Functions (serverless)

### **Serverless Approach**
- Use Azure Functions for individual endpoints
- Azure Static Web Apps for frontend
- More complex but potentially more cost-effective

## 📋 Pre-Deployment Checklist

- [ ] Azure subscription with appropriate permissions
- [ ] Azure CLI installed and configured
- [ ] Docker installed for container building
- [ ] GitHub repository set up for CI/CD
- [ ] Domain name purchased (optional)
- [ ] Azure OpenAI access confirmed and working
- [ ] Application tested locally with production settings
- [ ] Backup and disaster recovery plan created
- [ ] Security review completed
- [ ] Performance testing completed

## 🚀 Next Steps

1. **Start with Phase 1** - Application preparation and containerization
2. **Test locally** with Docker to ensure everything works
3. **Set up basic Azure infrastructure** (Phase 2)
4. **Deploy minimum viable version** (Phase 3)
5. **Iterate and improve** based on real usage (Phases 4-5)

## 📞 Support and Resources

- **Azure Documentation**: https://docs.microsoft.com/azure/
- **Container Apps Guide**: https://docs.microsoft.com/azure/container-apps/
- **Streamlit Cloud Deployment**: https://docs.streamlit.io/streamlit-cloud
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

**Total Timeline: 5-8 days for full production deployment**
**Minimum viable deployment: 2-3 days**
