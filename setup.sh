#!/bin/bash

# PR-Agent Setup Script
# This script helps set up the PR-Agent environment

set -e

echo "🚀 Setting up PR-Agent Automation..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version check passed: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed successfully"

# Create .env file template
echo "📝 Creating environment configuration template..."
cat > .env.template << EOF
# PR-Agent Configuration
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_REPOSITORY=your_username/your_repo_name
GITHUB_PR_NUMBER=1

# Optional: Custom model settings
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000
EOF

echo "✅ Environment template created: .env.template"

# Create sample test script
echo "🧪 Creating test script..."
cat > test_pr_agent.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for PR-Agent functionality
"""

import os
import sys
from pathlib import Path

def test_pr_agent():
    """Test PR-Agent with sample files"""
    print("🧪 Testing PR-Agent with sample files...")
    
    # Check if required environment variables are set
    required_vars = ['OPENAI_API_KEY', 'GITHUB_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment")
        return False
    
    # Test with sample files
    sample_dirs = ['terraform', 'ansible', 'kustomization', 'helm']
    
    for dir_name in sample_dirs:
        if Path(dir_name).exists():
            print(f"✅ Found {dir_name} directory")
        else:
            print(f"❌ Missing {dir_name} directory")
    
    print("🎉 PR-Agent setup test completed!")
    return True

if __name__ == "__main__":
    success = test_pr_agent()
    sys.exit(0 if success else 1)
EOF

chmod +x test_pr_agent.py

echo "✅ Test script created: test_pr_agent.py"

# Create GitHub Actions secrets setup guide
echo "📋 Creating GitHub Actions setup guide..."
cat > GITHUB_ACTIONS_SETUP.md << 'EOF'
# GitHub Actions Setup Guide

## Required Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click on "Settings" tab
3. Navigate to "Secrets and variables" → "Actions"
4. Click "New repository secret" and add:

### OPENAI_API_KEY
- **Name**: `OPENAI_API_KEY`
- **Value**: Your OpenAI API key
- **Description**: Required for PR-Agent AI functionality

### GITHUB_TOKEN
- **Name**: `GITHUB_TOKEN`
- **Value**: Automatically provided by GitHub Actions
- **Description**: Used for repository access (no action needed)

## Workflow Permissions

The workflow requires the following permissions:
- `pull-requests: write` - To post comments
- `contents: read` - To read repository contents
- `issues: write` - To create issues for critical findings

These permissions are automatically granted when using `GITHUB_TOKEN`.

## Testing the Setup

1. Create a test pull request with changes to sample files
2. Check the "Actions" tab to see the workflow running
3. Review the PR comments for automated feedback

## Troubleshooting

- Ensure all secrets are properly set
- Check workflow logs for detailed error messages
- Verify file patterns match your repository structure
EOF

echo "✅ GitHub Actions setup guide created: GITHUB_ACTIONS_SETUP.md"

echo ""
echo "🎉 PR-Agent setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Copy .env.template to .env and fill in your API keys"
echo "2. Add secrets to your GitHub repository (see GITHUB_ACTIONS_SETUP.md)"
echo "3. Test the setup with: python test_pr_agent.py"
echo "4. Create a pull request to test the automation"
echo ""
echo "Happy coding! 🚀"



