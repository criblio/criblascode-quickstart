# Cribl as Code - Terraform

Deploy and manage Cribl Cloud worker groups and packs using Terraform. This approach gives you infrastructure-as-code benefits: version control, code review, and repeatable deployments.

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

After `apply` completes, the configuration is automatically committed and deployed to your worker group.

## Files

| File | Purpose |
|------|---------|
| `provider.tf` | Cribl provider configuration |
| `variables.tf` | Input variable definitions |
| `main.tf` | Worker group and pack resources |
| `commit_deploy.tf` | Commit and deploy workflow |
| `outputs.tf` | Output values after apply |
| `terraform.tfvars.example` | Example variable values |
| `examples/` | Standalone example configurations |

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

## Commit and Deploy Workflow

Cribl requires configuration changes to be committed and deployed before they take effect on workers. The `commit_deploy.tf` file handles this automatically:

1. **Commit** - Saves all configuration changes with a commit message
2. **Get Version** - Retrieves the latest config version after commit
3. **Deploy** - Pushes the committed configuration to workers

```hcl
# Step 1: Commit configuration changes
resource "criblio_commit" "stream_commit" {
  effective = true
  group     = var.worker_group_id
  message   = "Deploy Stream configuration via Terraform"
}

# Step 2: Get the latest config version
data "criblio_config_version" "stream_config_version" {
  id         = var.worker_group_id
  depends_on = [criblio_commit.stream_commit]
}

# Step 3: Deploy the configuration
resource "criblio_deploy" "stream_deploy" {
  id      = var.worker_group_id
  version = data.criblio_config_version.stream_config_version.items[...]
}
```

When you add new resources (packs, pipelines, etc.), add them to the `depends_on` list in the commit resource to ensure proper ordering.

## Examples

| Example | Description |
|---------|-------------|
| [create-wg-with-pack](examples/create-wg-with-pack/) | Create a new worker group and install a pack |
| [install-packs](examples/install-packs/) | Install packs into an existing worker group |

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

Don't forget to add the new pack to the `depends_on` list in `criblio_commit.stream_commit`.

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

### Install Pack from Pack Dispensary

Packs can be installed from the [Pack Dispensary](https://packs.cribl.io) using `.crbl` URLs:

```hcl
resource "criblio_pack" "bedrock" {
  id       = "cribl-bedrock-io"
  group_id = var.worker_group_name
  source   = "https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
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
- [Pack Dispensary](https://packs.cribl.io)
- [Cribl Documentation](https://docs.cribl.io)
