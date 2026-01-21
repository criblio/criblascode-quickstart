# Cribl as Code Quickstart - Standalone Example
#
# This is a self-contained example that creates a worker group
# and installs the AWS VPC Flow Logs pack.
#
# Usage:
#   1. Copy this file to your own project
#   2. Update the variable values below
#   3. Run: terraform init && terraform apply

terraform {
  required_version = ">= 1.0"

  required_providers {
    criblio = {
      source  = "criblio/criblio"
      # version = ">= 1.0.0"
    }
  }
}

# Configure the Cribl provider
# Replace with your actual credentials or use environment variables
provider "criblio" {
  client_id       = var.cribl_client_id
  client_secret   = var.cribl_client_secret
  organization_id = var.cribl_cloud_org
  cloud_domain = "cribl.cloud"
}

# Variables - update these or set via terraform.tfvars
variable "cribl_client_id" {
  description = "Cribl Cloud API Client ID"
  type        = string
  sensitive   = true
  default = "29O1dlmBFMbr6tqrkK9b9FxupxTi4xSH"
}

variable "cribl_client_secret" {
  description = "Cribl Cloud API Client Secret"
  type        = string
  sensitive   = true
  default = "MfqmfUha0LuRtI_tWX266fN_pWFLMqqG0gbZ4p1gY2_S7f0036mLrcvqTIHVqiZT"
}

variable "cribl_cloud_org" {
  description = "Cribl Cloud Organization ID"
  type        = string
  default = "youthful-banach-uuinuki"
}

variable "worker_group_id" {
  description = "Unique identifier for the worker group"
  type        = string
  default     = "example-wg"
}

variable "worker_group_name" {
  description = "Display name for the worker group"
  type        = string
  default     = "Example Worker Group"
}

# Create a worker group
resource "criblio_group" "example" {
  id          = var.worker_group_id
  name        = var.worker_group_name
  description = "Worker group created from standalone example"
  product     = "stream"
}

# Install AWS VPC Flow Logs pack
resource "criblio_pack" "pan" {
  id       = "cribl-palo-alto-networks"
  group_id = criblio_group.example.id
  source   = "git+https://github.com/criblpacks/cribl-palo-alto-networks.git"

  depends_on = [criblio_group.example]
}

# Outputs
output "worker_group_id" {
  description = "ID of the created worker group"
  value       = criblio_group.example.id
}

output "pack_installed" {
  description = "Pack installation confirmation"
  value       = "Pack '${criblio_pack.vpcflow.id}' installed successfully"
}
