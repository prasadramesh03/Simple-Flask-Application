variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_cidr_az2" {
  description = "CIDR block for the second public subnet in AZ 2"
  type        = string
  default     = "10.0.1.0/24"  # Adjust the CIDR block for the second subnet as needed
}


variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "devops-project"
}
