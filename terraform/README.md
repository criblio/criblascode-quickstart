# Cribl as Code - Terraform

Deploy a Cribl Cloud worker group with the AWS VPC Flow Logs pack using Terraform.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.0
- Cribl Cloud API credentials (Client ID, Client Secret, Organization ID)

## Quick Start

```bash
# 1. Configure credentials
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# 2. Initialize Terraform
terraform init

# 3. Review the plan
terraform plan

# 4. Apply
terraform apply
```

## Files

| File | Purpose |
|------|---------|
| `provider.tf` | Cribl provider configuration |
| `variables.tf` | Input variable definitions |
| `main.tf` | Worker group and pack resources |
| `outputs.tf` | Output values after apply |
| `terraform.tfvars.example` | Example variable values |

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
| `worker_group_id` | Worker group identifier | `quickstart-wg` |
| `worker_group_name` | Worker group display name | `quickstart-worker-group` |
| `worker_group_description` | Worker group description | `Worker group created via Terraform quickstart` |
| `pack_id` | Pack identifier | `cribl-aws-vpcflow-logs` |
| `pack_source` | Pack source URL | GitHub URL for AWS VPC Flow Logs |

## Outputs

| Output | Description |
|--------|-------------|
| `worker_group_id` | ID of the created worker group |
| `worker_group_name` | Display name of the worker group |
| `pack_installed` | Confirmation message for pack installation |

## Authentication

The provider supports multiple authentication methods. This quickstart uses client credentials:

```hcl
provider "criblio" {
  client_id       = var.cribl_client_id
  client_secret   = var.cribl_client_secret
  organization_id = var.cribl_cloud_org
}
```

You can also use environment variables:

```bash
export CRIBL_CLIENT_ID="your-client-id"
export CRIBL_CLIENT_SECRET="your-client-secret"
export CRIBL_ORGANIZATION_ID="your-org-id"
```

## State Management

By default, Terraform state is stored locally. For team environments, configure a remote backend:

```hcl
terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "cribl/terraform.tfstate"
    region = "us-east-1"
  }
}
```

## Extending

### Add Another Pack

```hcl
resource "criblio_pack" "another_pack" {
  id       = "pack-name"
  group_id = criblio_group.worker_group.id
  source   = "https://github.com/criblpacks/pack-repo"
}
```

### Add Multiple Worker Groups

```hcl
variable "worker_groups" {
  default = {
    "dev"  = { name = "Development", description = "Dev environment" }
    "prod" = { name = "Production", description = "Prod environment" }
  }
}

resource "criblio_group" "groups" {
  for_each    = var.worker_groups
  id          = each.key
  name        = each.value.name
  description = each.value.description
  product     = "stream"
}
```

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Resources

- [Cribl Terraform Provider](https://github.com/criblio/terraform-provider-criblio)
- [Terraform Registry - Cribl Provider](https://registry.terraform.io/providers/criblio/criblio/latest)
- [Cribl Documentation](https://docs.cribl.io)
