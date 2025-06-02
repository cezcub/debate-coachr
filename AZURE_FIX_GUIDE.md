# Azure OpenAI Connection Fix Guide

## 🔍 Issue Identified
The connection error occurs because the Azure OpenAI endpoint URL is incorrect.

**Current URL:** `https://qtools.openai.azure.com/`
**Error:** DNS resolution failed - this domain doesn't exist.

## ✅ Solution Steps

### 1. Find Your Correct Azure OpenAI Endpoint

Go to the Azure Portal and follow these steps:

1. **Login to Azure Portal:** https://portal.azure.com
2. **Navigate to your Azure OpenAI resource:**
   - Search for "Azure OpenAI" in the search bar
   - Click on your OpenAI resource
3. **Get the endpoint URL:**
   - In the resource overview, look for "Endpoint"
   - It should look like: `https://YOUR-RESOURCE-NAME.openai.azure.com/`

### 2. Update Your .env File

Replace the endpoint in `/Users/aarush.tiyyagura/code/OutreachAI/.env`:

```env
AZURE_OPENAI_ENDPOINT='https://YOUR-ACTUAL-RESOURCE-NAME.openai.azure.com/'
```

### 3. Verify Your Model Deployment

In the Azure Portal:
1. Go to your Azure OpenAI resource
2. Click "Model deployments" or "Deployments"
3. Verify you have a model deployed named `gpt-4o`
4. If not, deploy a model or update the model name in the code

### 4. Test the Connection

Run this command to test:
```bash
cd /Users/aarush.tiyyagura/code/OutreachAI
python simple_test.py
```

## 🔧 Common Azure OpenAI Endpoint Formats

- **Correct:** `https://my-openai-resource.openai.azure.com/`
- **Incorrect:** `https://qtools.openai.azure.com/` ❌
- **Incorrect:** `https://my-openai-resource.azure.com/` ❌

## 📋 Verification Checklist

- [ ] Endpoint URL ends with `.openai.azure.com/`
- [ ] API key is 32 characters long
- [ ] Model deployment exists in Azure portal
- [ ] Resource is in an active subscription
- [ ] No typos in resource name

## 🆘 If Still Having Issues

1. **Check Resource Status:** Ensure your Azure OpenAI resource is active
2. **Verify Subscription:** Make sure your Azure subscription hasn't expired
3. **Check Region:** Some features may not be available in all regions
4. **Model Availability:** Verify GPT-4 is available in your region

## 📞 Next Steps After Fix

Once you have the correct endpoint:
1. Update the `.env` file
2. Run `python simple_test.py` to verify
3. Test the full application with `streamlit run app.py`
