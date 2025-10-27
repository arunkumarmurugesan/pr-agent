#!/usr/bin/env python3
"""
Local test script for PR-Agent functionality
This script simulates PR-Agent review on local files
"""

import os
import subprocess
import sys
from pathlib import Path

def install_pr_agent():
    """Install PR-Agent if not already installed"""
    print("📦 Installing PR-Agent...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pr-agent[all]"], 
                      check=True, capture_output=True, text=True)
        print("✅ PR-Agent installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PR-Agent: {e}")
        return False

def test_pr_agent_with_sample_files():
    """Test PR-Agent with sample files"""
    print("🧪 Testing PR-Agent with sample files...")
    
    # Check if we have sample files
    sample_files = [
        "terraform/main.tf",
        "ansible/playbook.yml", 
        "kustomization/deployment.yaml",
        "helm/values.yaml"
    ]
    
    existing_files = [f for f in sample_files if Path(f).exists()]
    if not existing_files:
        print("❌ No sample files found to test with")
        return False
    
    print(f"✅ Found {len(existing_files)} sample files to analyze")
    
    # Test with each file type
    for file_path in existing_files:
        print(f"\n🔍 Analyzing {file_path}...")
        try:
            # Use pr-agent to analyze the file
            result = subprocess.run([
                sys.executable, "-m", "pr_agent.cli", 
                "improve", 
                "--file_path", file_path,
                "--extra_instructions", "Focus on security issues, best practices, and code quality. Look for hardcoded secrets, insecure configurations, and missing validations."
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Analysis completed for {file_path}")
                if result.stdout:
                    print("📝 Analysis output:")
                    print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
            else:
                print(f"⚠️  Analysis had issues for {file_path}: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Analysis timed out for {file_path}")
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
    
    return True

def test_with_openai_api():
    """Test OpenAI API connection"""
    print("\n🔗 Testing OpenAI API connection...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    try:
        # Simple test with OpenAI API
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        response = client.models.list()
        models = [model.id for model in response.data if 'gpt' in model.id.lower()]
        
        print(f"✅ OpenAI API connection successful")
        print(f"✅ Found {len(models)} GPT models available")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 PR-Agent Local Test")
    print("=" * 40)
    
    # Check environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        return False
    
    print("✅ OPENAI_API_KEY found in environment")
    
    # Install PR-Agent
    if not install_pr_agent():
        return False
    
    # Test OpenAI API
    if not test_with_openai_api():
        return False
    
    # Test with sample files
    if not test_pr_agent_with_sample_files():
        return False
    
    print("\n🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Add OPENAI_API_KEY to GitHub repository secrets")
    print("3. Create a pull request to test the automation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



