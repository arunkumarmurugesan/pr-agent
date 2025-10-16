#!/usr/bin/env python3
"""
Verification script for PR-Agent setup
"""

import os
import sys
import requests
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment setup...")
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for PR-Agent functionality (REQUIRED)'
    }
    
    optional_vars = {
        'GITHUB_TOKEN': 'GitHub token for repository access (optional for local testing)'
    }
    
    missing_required = []
    missing_optional = []
    
    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set - {description}")
            missing_required.append(var)
    
    for var, description in optional_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Not set - {description}")
            missing_optional.append(var)
    
    return missing_required, missing_optional

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔗 Testing OpenAI API connection...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple API call
        response = requests.get(
            'https://api.openai.com/v1/models',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ OpenAI API connection successful")
            models = response.json().get('data', [])
            gpt_models = [m for m in models if 'gpt' in m.get('id', '').lower()]
            if gpt_models:
                print(f"✅ Available GPT models: {len(gpt_models)}")
            return True
        else:
            print(f"❌ OpenAI API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def check_repository_structure():
    """Check if repository structure is correct"""
    print("\n📁 Checking repository structure...")
    
    required_dirs = ['terraform', 'ansible', 'kustomization', 'helm', '.github/workflows']
    required_files = [
        'pr_agent_config.yaml',
        'requirements.txt',
        'README.md',
        '.github/workflows/pr-agent.yml'
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - Missing")
            all_good = False
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_good = False
    
    return all_good

def main():
    """Main verification function"""
    print("🚀 PR-Agent Setup Verification")
    print("=" * 40)
    
    # Check environment
    missing_required, missing_optional = check_environment()
    
    # Check repository structure
    structure_ok = check_repository_structure()
    
    # Test OpenAI connection if API key is available
    openai_ok = False
    if 'OPENAI_API_KEY' not in missing_required:
        openai_ok = test_openai_connection()
    else:
        print("\n⚠️  Skipping OpenAI test - API key not set")
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 40)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("   Set them in your .env file or environment")
    else:
        print("✅ All required environment variables are set")
    
    if missing_optional:
        print(f"⚠️  Missing optional environment variables: {', '.join(missing_optional)}")
        print("   These are optional for local testing but required for GitHub Actions")
    
    if structure_ok:
        print("✅ Repository structure is correct")
    else:
        print("❌ Repository structure has issues")
    
    if openai_ok:
        print("✅ OpenAI API connection working")
    elif 'OPENAI_API_KEY' in missing_required:
        print("⚠️  OpenAI API key not set - set OPENAI_API_KEY to test")
    else:
        print("❌ OpenAI API connection failed")
    
    # Overall status
    if not missing_required and structure_ok and openai_ok:
        print("\n🎉 All checks passed! PR-Agent is ready to use.")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
