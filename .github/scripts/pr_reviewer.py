#!/usr/bin/env python3
"""
Simple PR-Agent: Automated Pull Request Reviewer
Reviews code changes and posts comments on GitHub PRs
"""

import os
import sys
import subprocess
from pathlib import Path
import json
import base64
from github import Github
from openai import OpenAI

def get_pr_info():
    """Extract PR information from GitHub Actions context"""
    pr_number = os.getenv('GITHUB_EVENT')
    if not pr_number or not os.path.exists(pr_number):
        # Try alternative method
        pr_number = os.getenv('GITHUB_EVENT_PATH')
        if not pr_number or not os.path.exists(pr_number):
            # Fall back to command line
            pr_number = sys.argv[1] if len(sys.argv) > 1 else None
    
    if pr_number and os.path.exists(pr_number):
        with open(pr_number, 'r') as f:
            event_data = json.load(f)
            return event_data.get('pull_request', {}).get('number')
    
    return None

def get_changed_files():
    """Get list of changed files in the PR"""
    workspace_dir = os.getcwd()
    
    # Fetch base branch
    subprocess.run(['git', 'fetch', 'origin', 'main'], capture_output=True, cwd=workspace_dir)
    
    # Get changed files
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'origin/main...HEAD'],
        capture_output=True,
        text=True,
        cwd=workspace_dir
    )
    if result.returncode == 0:
        return [f.strip() for f in result.stdout.split('\n') if f.strip()]
    return []

def get_file_content(file_path):
    """Get content of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return ""

def review_with_openai(content, file_path):
    """Use OpenAI to review code"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    
    client = OpenAI(api_key=api_key)
    
    # Determine file type for context
    file_ext = Path(file_path).suffix
    file_type = ""
    if file_ext in ['.tf', '.tfvars']:
        file_type = "Terraform infrastructure code"
    elif file_ext in ['.yml', '.yaml']:
        if 'ansible' in file_path:
            file_type = "Ansible playbook"
        elif 'kustomization' in file_path:
            file_type = "Kubernetes Kustomize configuration"
    elif file_ext in ['.py']:
        file_type = "Python code"
    
    prompt = f"""Review the following {file_type} code for:
1. Security vulnerabilities (hardcoded secrets, insecure configurations)
2. Best practices and code quality
3. Missing error handling or validation
4. Infrastructure as Code compliance

File: {file_path}

```{file_ext}
{content[:4000]}  # Limit content size
```

Provide a concise review with specific recommendations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer specializing in security, best practices, and infrastructure as code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return None

def post_comment_to_pr(repo_name, pr_number, comment):
    """Post comment to GitHub PR"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("No GITHUB_TOKEN found")
        return False
    
    try:
        github = Github(token)
        repo = github.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))
        pr.create_issue_comment(comment)
        print(f"Comment posted to PR #{pr_number}")
        return True
    except Exception as e:
        print(f"Error posting comment: {e}")
        return False

def main():
    """Main review function"""
    print("🚀 Starting PR Review...")
    
    # Get repository name
    repo_name = os.getenv('GITHUB_REPOSITORY')
    if not repo_name:
        print("❌ GITHUB_REPOSITORY not found")
        return 1
    
    # Get PR number from GitHub Actions environment
    pr_number = os.getenv('GITHUB_EVENT_PATH')
    if pr_number and os.path.exists(pr_number):
        try:
            with open(pr_number, 'r') as f:
                event_data = json.load(f)
                pr_number = str(event_data.get('number', ''))
        except:
            pr_number = None
    
    if not pr_number:
        print("❌ Could not determine PR number")
        return 1
    
    print(f"📍 Repository: {repo_name}")
    print(f"📍 PR Number: {pr_number}")
    
    # Get changed files
    changed_files = get_changed_files()
    print(f"📁 Changed files: {len(changed_files)}")
    
    if not changed_files:
        print("⚠️  No changed files found")
        return 0
    
    # Focus on Terraform, Ansible, Kustomize, and Helm files
    relevant_files = [
        f for f in changed_files 
        if any(x in f for x in ['.tf', 'ansible/', 'kustomization/', 'helm/'])
    ]
    
    if not relevant_files:
        print("⚠️  No relevant files to review (Terraform, Ansible, Kubernetes, Helm)")
        return 0
    
    # Generate reviews for each file
    reviews = []
    for file_path in relevant_files[:5]:  # Limit to 5 files
        print(f"\n🔍 Reviewing: {file_path}")
        content = get_file_content(file_path)
        if content:
            review = review_with_openai(content, file_path)
            if review:
                reviews.append(f"## 📝 Review: `{file_path}`\n\n{review}")
    
    # Post comment to PR
    if reviews:
        comment = "\n\n---\n\n".join(reviews)
        comment = f"# 🤖 Automated PR Review\n\n{comment}\n\n---\n\n*Generated by PR-Agent*"
        post_comment_to_pr(repo_name, pr_number, comment)
    
    print("\n✅ PR Review completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
