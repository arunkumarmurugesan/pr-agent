#!/usr/bin/env python3
"""
Simple PR-Agent test to demonstrate functionality
"""

import os
import subprocess
import sys

def test_pr_agent_commands():
    """Test available PR-Agent commands"""
    print("🔍 Testing PR-Agent available commands...")
    
    try:
        # Show help to see available commands
        result = subprocess.run([
            sys.executable, "-m", "pr_agent.cli", "help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ PR-Agent help command successful")
            print("Available commands:")
            print(result.stdout)
        else:
            print(f"❌ PR-Agent help failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error testing PR-Agent: {e}")

def main():
    print("🧪 Simple PR-Agent Command Test")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return False
    
    print("✅ OPENAI_API_KEY found")
    
    # Test PR-Agent commands
    test_pr_agent_commands()
    
    print("\n📋 Correct PR-Agent Usage:")
    print("For GitHub PRs:")
    print("  python -m pr_agent.cli --pr_url=https://github.com/user/repo/pull/123 review")
    print("  python -m pr_agent.cli --pr_url=https://github.com/user/repo/pull/123 improve")
    print("  python -m pr_agent.cli --pr_url=https://github.com/user/repo/pull/123 describe")
    
    print("\nFor local files:")
    print("  python -m pr_agent.cli improve --file_path=path/to/file")
    
    return True

if __name__ == "__main__":
    main()



