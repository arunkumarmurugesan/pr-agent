#!/usr/bin/env python3
"""
Test script for the official PR-Agent
"""

import os
import subprocess
import sys

def test_official_pr_agent():
    """Test the official PR-Agent installation and commands"""
    print("🧪 Testing Official PR-Agent")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_KEY') or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found")
        print("Set it with: export OPENAI_KEY='your-key-here'")
        return False
    
    print(f"✅ OpenAI API key found: {api_key[:20]}...")
    
    # Test PR-Agent installation
    print("\n📦 Testing PR-Agent installation...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "pr-agent[all]"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ PR-Agent installed successfully")
        else:
            print(f"⚠️  PR-Agent installation had issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Error installing PR-Agent: {e}")
        return False
    
    # Test PR-Agent help
    print("\n🔍 Testing PR-Agent commands...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pr_agent.cli", "help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ PR-Agent help command successful")
            print("Available commands:")
            # Show first few lines of help
            help_lines = result.stdout.split('\n')[:10]
            for line in help_lines:
                if line.strip():
                    print(f"  {line}")
        else:
            print(f"❌ PR-Agent help failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error testing PR-Agent: {e}")
        return False
    
    print("\n🎉 Official PR-Agent is working!")
    print("\n📋 Next steps:")
    print("1. Push your code to GitHub")
    print("2. Add OPENAI_KEY to GitHub repository secrets")
    print("3. Create a pull request to test the automation")
    print("4. The PR-Agent will automatically review your PR!")
    
    return True

if __name__ == "__main__":
    success = test_official_pr_agent()
    sys.exit(0 if success else 1)
