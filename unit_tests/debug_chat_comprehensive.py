"""
Debug script for OutreachAI live chat feature
Tests all components and identifies issues
"""
import sys
import os
sys.path.append('/Users/aarush.tiyyagura/code/OutreachAI')

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("  ✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"  ❌ Streamlit import failed: {e}")
        return False
    
    try:
        from backend.azure import call_ai
        print("  ✅ Azure backend imported successfully")
    except ImportError as e:
        print(f"  ❌ Azure backend import failed: {e}")
        return False
    
    try:
        import requests
        print("  ✅ Requests imported successfully")
    except ImportError as e:
        print(f"  ❌ Requests import failed: {e}")
        return False
    
    return True

def test_azure_connection():
    """Test direct Azure OpenAI connection"""
    print("\n🔍 Testing Azure OpenAI connection...")
    
    try:
        from backend.azure import call_ai
        
        test_system = "You are a helpful assistant."
        test_user = "Say 'Hello, Azure connection is working!'"
        
        response = call_ai(test_system, test_user)
        print(f"  ✅ Azure connection working! Response: {response[:50]}...")
        return True
    except Exception as e:
        print(f"  ❌ Azure connection failed: {e}")
        return False

def test_fastapi_backend():
    """Test if FastAPI backend is running"""
    print("\n🔍 Testing FastAPI backend...")
    
    import requests
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"  ✅ FastAPI backend responding (status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("  ❌ FastAPI backend not running (connection refused)")
        return False
    except requests.exceptions.Timeout:
        print("  ❌ FastAPI backend timeout")
        return False
    except Exception as e:
        print(f"  ❌ FastAPI backend error: {e}")
        return False

def test_chat_endpoint():
    """Test the specific chat endpoint"""
    print("\n🔍 Testing chat endpoint...")
    
    import requests
    
    test_data = {
        "user_message": "Test message",
        "initial_context": "Test context",
        "debate_topic": "Test topic",
        "chat_history": []
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/chat/", json=test_data, timeout=10)
        if response.status_code == 200:
            print("  ✅ Chat endpoint working")
            return True
        else:
            print(f"  ❌ Chat endpoint error (status: {response.status_code})")
            try:
                error_detail = response.json()
                print(f"     Error details: {error_detail}")
            except:
                print(f"     Raw response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ❌ Chat endpoint not accessible (connection refused)")
        return False
    except Exception as e:
        print(f"  ❌ Chat endpoint error: {e}")
        return False

def test_chat_function_direct():
    """Test the chat function with direct Azure call"""
    print("\n🔍 Testing chat function (direct Azure)...")
    
    try:
        # Import the chat function
        from frontend.chat import generate_chat_response_direct
        
        # Test parameters
        user_message = "How can I improve my debate skills?"
        initial_context = "Student showed good structure but needs work on evidence integration."
        debate_topic = "Technology should be regulated more strictly"
        chat_history = []
        
        response = generate_chat_response_direct(user_message, initial_context, debate_topic, chat_history)
        print(f"  ✅ Direct chat function working! Response length: {len(response)} chars")
        print(f"     Preview: {response[:100]}...")
        return True
    except Exception as e:
        print(f"  ❌ Direct chat function failed: {e}")
        return False

def check_environment():
    """Check environment variables and configuration"""
    print("\n🔍 Checking environment configuration...")
    
    # Check for .env file
    env_path = "/Users/aarush.tiyyagura/code/OutreachAI/.env"
    if os.path.exists(env_path):
        print("  ✅ .env file found")
    else:
        print("  ❌ .env file not found")
        return False
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    if api_key:
        print(f"  ✅ AZURE_OPENAI_API_KEY found (length: {len(api_key)})")
    else:
        print("  ❌ AZURE_OPENAI_API_KEY not found")
        return False
    
    if endpoint:
        print(f"  ✅ AZURE_OPENAI_ENDPOINT found: {endpoint}")
    else:
        print("  ❌ AZURE_OPENAI_ENDPOINT not found")
        return False
    
    return True

def provide_recommendations(results):
    """Provide recommendations based on test results"""
    print("\n" + "="*50)
    print("📋 DIAGNOSIS & RECOMMENDATIONS")
    print("="*50)
    
    if not results['imports']:
        print("❌ CRITICAL: Import issues detected")
        print("   → Install missing packages: pip install streamlit requests python-dotenv")
    
    if not results['environment']:
        print("❌ CRITICAL: Environment configuration issues")
        print("   → Create .env file with Azure OpenAI credentials")
        print("   → Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
    
    if not results['azure']:
        print("❌ CRITICAL: Azure OpenAI connection failed")
        print("   → Check your API key and endpoint")
        print("   → Verify your Azure OpenAI deployment")
    
    if not results['fastapi']:
        print("⚠️  WARNING: FastAPI backend not running")
        print("   → Start backend: uvicorn backend.backend:app --reload")
        print("   → Or use direct Azure mode (recommended for now)")
    
    if not results['chat_endpoint'] and results['fastapi']:
        print("❌ ERROR: Chat endpoint not working")
        print("   → Check backend/chat.py for errors")
        print("   → Verify chat router is properly included")
    
    if results['azure'] and results['chat_direct']:
        print("✅ GOOD NEWS: Direct chat functionality works!")
        print("   → Use render_chat_interface(context, topic, use_api=False)")
    
    print("\n🎯 IMMEDIATE ACTION PLAN:")
    if results['azure'] and results['chat_direct']:
        print("1. ✅ Chat can work with direct Azure connection")
        print("2. 🔧 Ensure use_api=False in your chat calls")
        print("3. 📝 Optional: Start FastAPI backend for API mode")
    else:
        print("1. 🔧 Fix Azure OpenAI connection first")
        print("2. 📝 Verify environment variables")
        print("3. 🔄 Re-run this debug script")

def main():
    print("🔧 OUTREACHAI CHAT DEBUG TOOL")
    print("="*50)
    
    # Run all tests
    results = {
        'imports': test_imports(),
        'environment': check_environment(),
        'azure': test_azure_connection(),
        'fastapi': test_fastapi_backend(),
        'chat_endpoint': test_chat_endpoint(),
        'chat_direct': test_chat_function_direct()
    }
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():<15}: {status}")
    
    # Provide recommendations
    provide_recommendations(results)
    
    print("\n🏁 Debug complete!")

if __name__ == "__main__":
    main()
