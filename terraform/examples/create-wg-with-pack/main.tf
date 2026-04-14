# Cribl as Code Quickstart - Standalone Example
#
# This is a self-contained example that creates a worker group
# and installs the AWS VPC Flow Logs pack.
#
# Usage:
#   1. Copy this file to your own project
#   2. Update the variable values in tfvars
#   3. Run: terraform init && terraform apply

# Create a worker group
resource "criblio_group" "example" {
  id          = var.worker_group_id
  name        = var.worker_group_name
  description = "Worker group created from standalone example"
  product     = "stream"
  provisioned = true
  on_prem = false
  estimated_ingest_rate = 1024
  # values allowed [1024,2048,3072,4096,5120,7168,10240,13312,15360]
  cloud = {
    provider = "aws"
    region   = "us-east-1"
  }
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
  value       = "Pack '${criblio_pack.pan.id}' installed successfully"
}
