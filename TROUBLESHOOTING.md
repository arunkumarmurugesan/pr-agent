# PR-Agent Troubleshooting Guide

## Issue: No Comments Appearing in PR

### Solution 1: Check if PR-Agent is Triggered
The official PR-Agent GitHub Action runs when:
1. A new PR is opened
2. New commits are pushed to the PR

### Solution 2: Verify Environment Variables
Make sure you have set the following secrets in your GitHub repository:

1. Go to: `https://github.com/arunkumarmurugesan/pr-agent/settings/secrets/actions`
2. Add these secrets:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

### Solution 3: Check Actions Tab
1. Go to your PR: https://github.com/arunkumarmurugesan/pr-agent/pull/1
2. Click on the "Checks" tab or "Actions" tab
3. Look for the "PR Agent" workflow run
4. Click on it to see if there are any errors

### Solution 4: Manual Trigger
If the automatic trigger isn't working, you can manually trigger PR-Agent by:

1. Go to your PR on GitHub
2. Add a comment with one of these commands:
   - `/review` - Get a comprehensive PR review
   - `/improve` - Get code improvement suggestions
   - `/describe` - Generate PR description and title

### Solution 5: Alternative - Use PR-Agent Directly
Instead of relying on GitHub Actions, you can use PR-Agent directly:

```bash
# Install PR-Agent
pip install pr-agent[all]

# Review the PR
python -m pr_agent.cli --pr_url=https://github.com/arunkumarmurugesan/pr-agent/pull/1 review

# Improve code
python -m pr_agent.cli --pr_url=https://github.com/arunkumarmurugesan/pr-agent/pull/1 improve

# Describe PR
python -m pr_agent.cli --pr_url=https://github.com/arunkumarmurugesan/pr-agent/pull/1 describe
```

## Common Issues

### Issue: "Authentication failed"
**Solution**: Make sure your `GITHUB_TOKEN` has the necessary permissions:
- `pull-requests: write` - To post comments
- `contents: read` - To read repository contents
- `metadata: read` - To read metadata

### Issue: "OpenAI API key invalid"
**Solution**: Verify your OpenAI API key is correct:
1. Check that the key starts with `sk-`
2. Make sure it's added as `OPENAI_API_KEY` secret (not `OPENAI_KEY`)
3. Test the key with the OpenAI API directly

### Issue: "No changes detected"
**Solution**: Make sure your PR has actual file changes and is not empty

## Testing Locally

To test PR-Agent locally:

```bash
# Set your environment variables
export OPENAI_API_KEY="your-api-key-here"
export GITHUB_TOKEN="your-github-token-here"

# Run PR-Agent on a local file
python -m pr_agent.cli improve --file_path=terraform/main.tf

# Or test with your PR
python -m pr_agent.cli --pr_url=https://github.com/arunkumarmurugesan/pr-agent/pull/1 review
```

## Next Steps

1. **Check your Actions run**: Go to the Actions tab and see if the workflow completed successfully
2. **Try manual trigger**: Add a comment to your PR with `/review`
3. **Check secrets**: Verify your `OPENAI_API_KEY` is set correctly
4. **Review logs**: Check the workflow logs for any errors

## Resources

- [PR-Agent Documentation](https://github.com/qodo-ai/pr-agent)
- [PR-Agent GitHub Action](https://github.com/marketplace/actions/pr-agent)
- [Troubleshooting Guide](https://www.qodo.ai/blog/technical-faq-and-troubleshooting/)
