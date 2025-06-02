"""
Azure OpenAI Diagnostic Test
This test uses the same configuration as the actual application (azure.py)
to ensure accurate testing and better adaptability.

USAGE:
    python unit_tests/azure_diagnostic_test.py

This will test:
1. The exact same Azure OpenAI configuration used by the application
2. Endpoint connectivity and format
3. API version compatibility
4. Model deployment availability
5. Provide specific recommendations for fixing common issues

EXAMPLE OUTPUT:
    ✅ Successfully imported azure.py configuration
    === Azure OpenAI Diagnostics (Using Actual App Configuration) ===
    API Key: 96259dee... (length: 32)
    Endpoint: https://your-resource.openai.azure.com/
    Using Model: gpt-4.1
    Using API Version: 2024-12-01-preview
    
    0. Testing actual azure.py configuration...
       ✅ Azure.py configuration works! Response: Azure connection test successful
"""
import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI
import requests

# Add the backend directory to path to import azure configuration
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Load environment variables from the root directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'), override=True)

# Configuration constants from azure.py
ACTUAL_MODEL = 'gpt-4.1'
ACTUAL_API_VERSION = "2024-12-01-preview"

# Import the actual configuration from azure.py
AZURE_CONFIG_AVAILABLE = False
call_ai = None

try:
    # Try importing from backend.azure first
    from backend.azure import call_ai
    AZURE_CONFIG_AVAILABLE = True
    print("✅ Successfully imported azure.py configuration")
except ImportError:
    try:
        # Add parent directory to path and try again
        import sys
        import os
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
        from backend.azure import call_ai
        AZURE_CONFIG_AVAILABLE = True
        print("✅ Successfully imported azure.py configuration (with path adjustment)")
    except ImportError:
        print("⚠️  Could not import azure.py - will test configuration manually")

# Get credentials
api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

print("=== Azure OpenAI Diagnostics (Using Actual App Configuration) ===")
print(f"API Key: {api_key[:8]}... (length: {len(api_key) if api_key else 0})")
print(f"Endpoint: {endpoint}")
print(f"Using Model: {ACTUAL_MODEL}")
print(f"Using API Version: {ACTUAL_API_VERSION}")

# Test 0: Test actual azure.py configuration
if AZURE_CONFIG_AVAILABLE:
    print("\n0. Testing actual azure.py configuration...")
    try:
        test_response = call_ai(
            "You are a helpful assistant.", 
            "Say 'Azure connection test successful' in exactly 5 words."
        )
        print(f"   ✅ Azure.py configuration works! Response: {test_response}")
    except Exception as e:
        print(f"   ❌ Azure.py configuration failed: {str(e)}")
else:
    print("\n0. Azure.py configuration not available - proceeding with manual tests")

# Test 1: Check if endpoint is reachable
print("\n1. Testing endpoint connectivity...")
try:
    response = requests.get(endpoint, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Check endpoint format
print("\n2. Checking endpoint format...")
if endpoint and not endpoint.endswith('/'):
    print("   ⚠️  Endpoint should end with '/'")
    corrected_endpoint = endpoint + '/'
    print(f"   Suggested: {corrected_endpoint}")
else:
    print("   ✅ Endpoint format looks correct")

# Test 3: Try actual configuration first, then fallback versions
print("\n3. Testing API versions (starting with actual app configuration)...")
api_versions = [ACTUAL_API_VERSION, "2024-10-21", "2024-02-01", "2023-12-01-preview"]

for version in api_versions:
    try:
        print(f"   Testing API version: {version}")
        client = AzureOpenAI(
            api_key=api_key,
            api_version=version,
            azure_endpoint=endpoint
        )
        
        # Try the actual model first
        model_to_test = ACTUAL_MODEL if version == ACTUAL_API_VERSION else 'gpt-4o'
        completion = client.chat.completions.create(
            model=model_to_test,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print(f"   ✅ Success with API version {version} and model {model_to_test}")
        break
        
    except Exception as e:
        print(f"   ❌ Failed with {version}: {str(e)[:100]}...")

# Test 4: Check actual model first, then common model names
print("\n4. Testing model names (starting with actual app model)...")
model_names = [ACTUAL_MODEL, 'gpt-4o', 'gpt-4', 'gpt-35-turbo', 'gpt-4-turbo']

for model in model_names:
    try:
        print(f"   Testing model: {model}")
        client = AzureOpenAI(
            api_key=api_key,
            api_version=ACTUAL_API_VERSION,
            azure_endpoint=endpoint
        )
        
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print(f"   ✅ Success with model {model}")
        break
        
    except Exception as e:
        error_str = str(e)
        if "model" in error_str.lower() or "deployment" in error_str.lower():
            print(f"   ❌ Model {model} not found")
        else:
            print(f"   ❌ Failed with {model}: {error_str[:50]}...")

# Test 5: Configuration recommendations
print("\n5. Configuration recommendations...")
print(f"   Current endpoint: {endpoint}")
if endpoint and 'qtools.openai.azure.com' in endpoint:
    print("   ⚠️  WARNING: 'qtools.openai.azure.com' appears to be invalid")
    print("   💡 Suggestion: Replace with your actual Azure OpenAI resource name")
    print("      Format: https://YOUR-RESOURCE-NAME.openai.azure.com/")
    
print(f"   Current model: {ACTUAL_MODEL}")
print(f"   Current API version: {ACTUAL_API_VERSION}")
print("   💡 Make sure your Azure deployment matches these settings")

print("\n=== Diagnostic Complete ===")
print("If all tests fail, check:")
print("1. Your Azure OpenAI resource name in the endpoint URL")
print("2. Your API key is valid and has access")
print("3. Your model deployment name matches the configuration")
print("4. Your subscription has access to the specified model and API version")
