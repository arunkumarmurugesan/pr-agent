# Variables file - this is a good practice
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

# Issue: Missing validation
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the web servers"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Issue: Default is too permissive
}
