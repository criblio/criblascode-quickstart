# Example: Create Worker Group with Pack

A standalone, self-contained Terraform example that creates a Cribl Cloud worker group with the AWS VPC Flow Logs pack installed.

## Usage

```bash
# Initialize
terraform init

# Set credentials via environment variables
export TF_VAR_cribl_client_id="your-client-id"
export TF_VAR_cribl_client_secret="your-client-secret"
export TF_VAR_cribl_cloud_org="your-org-id"

# Apply
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

## What This Creates

1. **Worker Group** - A new Cribl Stream worker group in your organization
2. **Pack** - AWS VPC Flow Logs pack installed in the worker group

## Customization

To use a different pack, modify the `criblio_pack` resource:

```hcl
resource "criblio_pack" "custom" {
  id       = "your-pack-id"
  group_id = criblio_group.example.id
  source   = "https://github.com/criblpacks/your-pack-repo"
}
```

## Cleanup

```bash
terraform destroy
```
