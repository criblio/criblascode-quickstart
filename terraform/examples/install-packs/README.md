# Example: Install Packs into Existing Worker Group

A standalone Terraform example that installs packs into an existing Cribl Cloud worker group. Use this when you already have worker groups and want to add functionality through packs.

## What This Does

- Installs packs into a worker group that already exists
- Demonstrates installing from both GitHub and Pack Dispensary
- Automatically commits and deploys the configuration

**Note:** This example does NOT create a new worker group. The target worker group must already exist in your Cribl Cloud organization.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.0
- Cribl Cloud API credentials
- An existing worker group in Cribl Cloud

## Quick Start

```bash
# Initialize Terraform
terraform init

# Configure credentials
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Review and apply
terraform plan
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
| `worker_group_name` | Target worker group name | `default` |
| `pack_id` | Pack identifier | `cribl-syslog-input` |
| `pack_source` | Pack source URL | GitHub URL for syslog input |

## Files

| File | Purpose |
|------|---------|
| `main.tf` | Pack installation resources |
| `provider.tf` | Cribl provider configuration |
| `variables.tf` | Input variable definitions |
| `commit_deploy.tf` | Commit and deploy workflow |
| `outputs.tf` | Output values |
| `terraform.tfvars.example` | Example variable values |

## Example: Install Multiple Packs

The default configuration installs two packs:

```hcl
# Pack from GitHub
resource "criblio_pack" "aws_pan_logs" {
  id       = var.pack_id
  group_id = var.worker_group_name
  source   = var.pack_source
  spec     = "main"
}

# Pack from Pack Dispensary
resource "criblio_pack" "bedrock" {
  id       = "cribl-bedrock-io"
  group_id = var.worker_group_name
  source   = "https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
}
```

## Pack Sources

Packs can be installed from two sources:

### GitHub (for pack development or specific versions)

```hcl
resource "criblio_pack" "from_github" {
  id       = "cribl-syslog-input"
  group_id = var.worker_group_name
  source   = "git+https://github.com/criblpacks/cribl-syslog-input.git"
  spec     = "main"  # branch, tag, or commit
}
```

### Pack Dispensary (recommended for production)

```hcl
resource "criblio_pack" "from_dispensary" {
  id       = "cribl-aws-bedrock-io"
  group_id = var.worker_group_name
  source   = "https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
}
```

Browse available packs at [packs.cribl.io](https://packs.cribl.io).

## Customization

### Target a Different Worker Group

Update `terraform.tfvars`:

```hcl
worker_group_name = "production-wg"
```

### Add More Packs

Add additional `criblio_pack` resources to `main.tf`:

```hcl
resource "criblio_pack" "new_pack" {
  id       = "pack-name"
  group_id = var.worker_group_name
  source   = "https://packs.cribl.io/dl/pack-name/1.0.0/pack-name-1.0.0.crbl"
}
```

Then add it to the `depends_on` list in `commit_deploy.tf`:

```hcl
resource "criblio_commit" "stream_commit" {
  depends_on = [
    criblio_pack.aws_pan_logs,
    criblio_pack.bedrock,
    criblio_pack.new_pack,  # Add new packs here
  ]
}
```

## Cleanup

To remove the packs:

```bash
terraform destroy
```

## Troubleshooting

### Worker Group Not Found

Ensure the `worker_group_name` matches an existing worker group in your Cribl Cloud organization.

### Pack Already Installed

If the pack already exists, Terraform will update it to match the specified source/version. To force reinstallation, use `terraform taint criblio_pack.pack_name`.

### Deploy Fails

Ensure you have deploy permissions for the target worker group.

## Related Documentation

- [Main README](../../../README.md) - Overview and other examples
- [Terraform README](../../README.md) - Terraform-specific documentation
- [create-wg-with-pack](../create-wg-with-pack/) - Example for creating a new worker group
- [Pack Dispensary](https://packs.cribl.io)
