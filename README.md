# PR-Agent Automation

This repository contains PR-Agent automation setup with GitHub Actions for automated code review, security analysis, and best practices validation across multiple technologies.

## 🚀 Features

- **Automated PR Reviews**: Comprehensive code review for Terraform, Ansible, Kubernetes, and Helm
- **Security Analysis**: Automated security vulnerability detection
- **Best Practices Validation**: Enforces coding standards and best practices
- **Multi-Technology Support**: Covers Infrastructure as Code (IaC) and configuration management tools
- **GitHub Actions Integration**: Seamless CI/CD pipeline integration

## 📁 Repository Structure

```
pr-agent/
├── .github/
│   └── workflows/
│       └── pr-agent.yml          # GitHub Actions workflow
├── terraform/                    # Terraform examples and tests
│   ├── main.tf
│   └── variables.tf
├── ansible/                      # Ansible examples and tests
│   ├── playbook.yml
│   └── roles/
│       └── web/
│           └── tasks/
│               └── main.yml
├── kustomization/               # Kubernetes Kustomize examples
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── helm/                        # Helm chart examples
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       └── deployment.yaml
├── pr_agent_config.yaml         # PR-Agent configuration
└── README.md
```

## 🛠️ Setup

### Prerequisites

1. **GitHub Repository**: Fork or clone this repository
2. **OpenAI API Key**: Required for PR-Agent functionality
3. **GitHub Token**: For repository access (automatically provided by GitHub Actions)

### Configuration

1. **Add Secrets to GitHub Repository**:
   - Go to your repository settings
   - Navigate to "Secrets and variables" → "Actions"
   - Add the following secrets:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `GITHUB_TOKEN`: GitHub token (automatically provided)

2. **Customize PR-Agent Configuration**:
   - Edit `pr_agent_config.yaml` to customize review settings
   - Modify technology-specific configurations as needed
   - Adjust security and best practices rules

### GitHub Actions Workflow

The workflow automatically triggers on:
- Pull request opened
- Pull request synchronized (new commits)
- Pull request reopened
- Pull request review submitted

## 🔍 Supported Technologies

### Terraform
- **Security Checks**: Hardcoded secrets, resource naming, security groups
- **Best Practices**: Variable usage, state management, resource tagging
- **File Patterns**: `*.tf`, `*.tfvars`, `*.tf.json`

### Ansible
- **Security Checks**: Hardcoded passwords, privilege escalation, file permissions
- **Best Practices**: Ansible-vault usage, error handling, idempotency
- **File Patterns**: `*.yml`, `*.yaml`, `playbooks/*`, `roles/*`

### Kubernetes (Kustomize)
- **Security Checks**: Resource limits, security contexts, RBAC
- **Best Practices**: Image tags, health checks, ConfigMaps/Secrets
- **File Patterns**: `*.yaml`, `*.yml`, `kustomization.yaml`

### Helm
- **Security Checks**: Hardcoded values, chart security, privilege escalation
- **Best Practices**: Values files, chart versioning, template usage
- **File Patterns**: `Chart.yaml`, `values*.yaml`, `templates/*`

## 📋 Review Categories

### Security Issues
- **Critical**: Hardcoded secrets, privilege escalation, insecure connections
- **High**: Missing resource limits, public access, insecure configurations
- **Medium**: Missing tags, hardcoded values, missing documentation

### Best Practices
- Variable usage and configuration management
- Resource tagging and documentation
- Error handling and validation
- Security context and permissions

## 🚦 Workflow Process

1. **Trigger**: PR is created or updated
2. **Analysis**: PR-Agent analyzes changed files
3. **Review**: Generates comprehensive review comments
4. **Security Scan**: Performs security vulnerability analysis
5. **Best Practices**: Validates against coding standards
6. **Comments**: Posts detailed feedback on the PR

## 📝 Sample Files

The repository includes sample files with intentional issues to demonstrate PR-Agent capabilities:

- **Terraform**: Infrastructure with security and best practice issues
- **Ansible**: Playbooks with configuration and security problems
- **Kubernetes**: Manifests with resource and security misconfigurations
- **Helm**: Charts with templating and security issues

## 🔧 Customization

### Adding New Technologies

1. Update `pr_agent_config.yaml` with new technology configuration
2. Add file patterns and specific checks
3. Update GitHub Actions workflow if needed

### Modifying Review Rules

1. Edit security and best practices rules in `pr_agent_config.yaml`
2. Adjust severity levels and thresholds
3. Add custom validation rules

### Workflow Customization

1. Modify `.github/workflows/pr-agent.yml`
2. Add additional review steps
3. Configure different triggers or conditions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample files
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the GitHub Issues section
2. Review the PR-Agent documentation
3. Create a new issue with detailed information

## 🔗 Related Links

- [PR-Agent Documentation](https://github.com/Codium-ai/pr-agent)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs)