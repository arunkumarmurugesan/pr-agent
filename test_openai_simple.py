#!/usr/bin/env python3
"""
Simple OpenAI API test with SSL workaround
"""

import os
import ssl
import urllib.request
import urllib.error
import json

def test_openai_with_ssl_workaround():
    """Test OpenAI API with SSL workaround"""
    print("🔗 Testing OpenAI API with SSL workaround...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    # Create SSL context that doesn't verify certificates
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        # Test with a simple API call
        url = 'https://api.openai.com/v1/models'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        request = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(request, context=ssl_context, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                models = data.get('data', [])
                gpt_models = [m for m in models if 'gpt' in m.get('id', '').lower()]
                print(f"✅ OpenAI API connection successful!")
                print(f"✅ Found {len(gpt_models)} GPT models available")
                return True
            else:
                print(f"❌ OpenAI API error: {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Invalid API key - please check your OPENAI_API_KEY")
        else:
            print(f"❌ HTTP error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    print("🧪 Simple OpenAI API Test")
    print("=" * 30)
    
    success = test_openai_with_ssl_workaround()
    
    if success:
        print("\n🎉 OpenAI API is working! Your setup is ready.")
        print("Note: This test bypassed SSL verification for testing purposes.")
        print("The actual PR-Agent will use proper SSL verification.")
    else:
        print("\n❌ OpenAI API test failed. Please check your API key.")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
