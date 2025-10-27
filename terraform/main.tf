# Sample Terraform configuration with some issues for PR-Agent to catch
provider "aws" {
  region = "us-west-2"
}

# Issue: Hardcoded values instead of variables
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"  # Hardcoded AMI
  instance_type = "t2.micro"
  
  # Issue: No security group attached
  # Issue: No tags
  # Issue: No user data for hardening
  
  root_block_device {
    volume_size = 20
    volume_type = "gp2"
    # Issue: No encryption
  }
}

# Issue: Security group with overly permissive rules
resource "aws_security_group" "web_sg" {
  name        = "web-security-group"
  description = "Security group for web servers"
  
  # Issue: Too permissive ingress rules
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Issue: Open to all IPs
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Issue: No tags
}

# Issue: Hardcoded password in user data
resource "aws_instance" "database" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.small"
  
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y mysql-server
    systemctl start mysqld
    mysql -u root -p'MyHardcodedPassword123!'  # Issue: Hardcoded password
  EOF
  
  # Issue: No security group
  # Issue: No tags
}



