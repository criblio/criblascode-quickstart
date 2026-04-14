# Example: Create Worker Group with Pack

A standalone, self-contained Terraform example that creates a new Cribl Cloud worker group with a pack installed. Use this as a starting point for managing your own Cribl infrastructure.

## What This Creates

1. **Worker Group** - A new Cribl Stream worker group in your organization
   - Hosted in AWS us-east-1 (configurable)
   - 1 GB estimated ingest rate
2. **Pack** - Palo Alto Networks pack installed in the worker group
3. **Commit & Deploy** - Automatically commits and deploys the configuration

## Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.0
- Cribl Cloud API credentials

## Quick Start

```bash
# Initialize Terraform
terraform init

# Set credentials via environment variables
export TF_VAR_cribl_client_id="your-client-id"
export TF_VAR_cribl_client_secret="your-client-secret"
export TF_VAR_cribl_cloud_org="your-org-id"

# Review and apply
terraform plan
terraform apply
```

Or create a `terraform.tfvars` file:

```hcl
cribl_client_id     = "your-client-id"
cribl_client_secret = "your-client-secret"
cribl_cloud_org     = "your-org-id"
worker_group_id     = "my-worker-group"
worker_group_name   = "My Worker Group"
```

Then run:

```bash
terraform init
terraform apply
```

## Variables

### Required

| Variable | Description |
|----------|-------------|
| `cribl_client_id` | Cribl Cloud API Client ID |
| `cribl_client_secret` | Cribl Cloud API Client Secret |
| `cribl_cloud_org` | Cribl Cloud Organization ID |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `workspace_id` | Cribl Cloud Workspace ID | `main` |
| `worker_group_id` | Unique identifier for the worker group | `datacenter-emea` |
| `worker_group_name` | Display name | `datacenter-emea` |
| `worker_group_description` | Description | `Worker group created via Terraform quickstart` |
| `pack_id` | Pack identifier | `cribl-syslog-input` |
| `pack_source` | Pack source URL | GitHub URL for syslog input |

## Files

| File | Purpose |
|------|---------|
| `main.tf` | Worker group and pack resources, outputs |
| `provider.tf` | Cribl provider configuration |
| `variables.tf` | Input variable definitions |
| `commit_deploy.tf` | Commit and deploy workflow |
| `terraform.tfvars.example` | Example variable values |

## Customization

### Change the Cloud Provider or Region

```hcl
resource "criblio_group" "example" {
  # ...
  cloud = {
    provider = "gcp"      # aws, gcp, or azure
    region   = "us-west1"
  }
}
```

### Change the Ingest Rate

```hcl
resource "criblio_group" "example" {
  # ...
  estimated_ingest_rate = 5120  # Values: 1024, 2048, 3072, 4096, 5120, 7168, 10240, 13312, 15360
}
```

### Use a Different Pack

```hcl
resource "criblio_pack" "custom" {
  id       = "your-pack-id"
  group_id = criblio_group.example.id
  source   = "https://github.com/criblpacks/your-pack-repo"
}
```

### Install from Pack Dispensary

```hcl
resource "criblio_pack" "dispensary_pack" {
  id       = "cribl-aws-bedrock-io"
  group_id = criblio_group.example.id
  source   = "https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
}
```

## Outputs

After `terraform apply`, you'll see:

- `worker_group_id` - The ID of your new worker group
- `pack_installed` - Confirmation of pack installation

## Cleanup

```bash
terraform destroy
```

## Next Steps

1. Log into Cribl Cloud to view your new worker group
2. Configure the pack's sources and destinations
3. Deploy workers to the group
4. Add additional packs as needed

## Related Documentation

- [Main README](../../../README.md) - Overview and other examples
- [Terraform README](../../README.md) - Terraform-specific documentation
- [Cribl Terraform Provider](https://github.com/criblio/terraform-provider-criblio)
