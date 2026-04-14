# Claude Helper for Cribl as Code Quickstart

This file provides context for Claude to help users get started with this repository.

## Repository Purpose

This is a quickstart repo for Cribl.Cloud administrators who want to manage Cribl Stream infrastructure as code instead of using the UI (ClickOps). It provides two paths:

1. **Terraform** (`terraform/`) - For teams using Terraform for infrastructure management
2. **Python SDK** (`sdk/python/`) - Modular Python scripts for flexibility and exploration

## Common User Goals

Users typically want to:
1. Set up API credentials and run their first deployment
2. Create a worker group in Cribl Cloud
3. Install packs from the Pack Dispensary
4. Understand how to extend the examples for their environment

## Prerequisites Check

Before helping users run the quickstarts, verify they have:

### For Terraform
- Terraform 1.x installed (`terraform --version`)
- Cribl Cloud API credentials

### For Python
- Python 3.9+ installed (`python3 --version`)
- Cribl Cloud API credentials

## Credential Setup

Users get credentials from Cribl Cloud:
1. Log into https://cribl.cloud (or https://cribl-staging.cloud for staging)
2. Navigate to **Settings > API Credentials**
3. Create new API credential
4. Note: Client ID, Client Secret, Organization ID

### Finding the Organization ID
The Organization ID is in the Cribl Cloud URL after logging in:
`https://{workspace}-{org-id}.cribl.cloud` - the `{org-id}` part is the Organization ID.

### Finding the Workspace
Most users use `main` as their workspace. It's visible in the URL:
`https://{workspace}-{org-id}.cribl.cloud`

## Terraform Quickstart

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# User edits terraform.tfvars with credentials
terraform init
terraform plan
terraform apply
```

Key files:
- `terraform.tfvars` - User credentials (gitignored)
- `main.tf` - Resource definitions
- `commit_deploy.tf` - Handles commit and deploy workflow

## Python SDK Quickstart

```bash
cd sdk/python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# User edits .env with credentials
python3 create_wg_with_pack.py
```

### Python Module Structure

```
sdk/python/
├── config.py              # Configuration & environment variables
├── auth.py                # Authentication (get_client, get_group_client)
├── worker_groups.py       # create, list, get, delete worker groups
├── packs.py               # install, list, get, delete packs
├── create_wg_with_pack.py # Main quickstart script
├── requirements.txt
└── .env.example
```

### Using Python Modules Directly

```python
# Create a worker group
from worker_groups import create_worker_group
create_worker_group("my-wg", "My Worker Group")

# Install a pack
from packs import install_pack
install_pack("my-wg", "git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git")

# List groups
from worker_groups import list_worker_groups
groups = list_worker_groups()
```

### Running with Custom Values

```bash
WORKER_GROUP_ID=my-wg WORKER_GROUP_NAME="My Group" python3 create_wg_with_pack.py
```

## Environment Variables

### Required
```bash
CRIBL_CLIENT_ID=your-client-id
CRIBL_CLIENT_SECRET=your-client-secret
CRIBL_ORGANIZATION_ID=your-org-id
```

### Optional (with defaults)
```bash
CRIBL_WORKSPACE=main
CRIBL_DOMAIN=cribl.cloud               # Use "cribl-staging.cloud" for staging
WORKER_GROUP_ID=quickstart-wg
WORKER_GROUP_NAME=Quickstart Worker Group
PACK_ID=cribl-aws-vpcflow-logs
PACK_SOURCE=git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git
```

## Common Errors and Solutions

### "Cannot POST" or 404 errors
**Cause**: Incorrect API URL format
**Solution**: URL should be `https://{workspace}-{orgId}.{domain}/api/v1`
- Note the DASH between workspace and orgId
- Check `CRIBL_WORKSPACE` and `CRIBL_ORGANIZATION_ID`

### "Unexpected status code 400 from token endpoint"
**Cause**: Wrong auth URLs for environment
**Solution**:
- For staging, set `CRIBL_DOMAIN=cribl-staging.cloud`
- The code automatically uses staging auth URLs when domain contains "staging"

### Authentication errors
**Cause**: Invalid or expired credentials
**Solution**:
- Verify Client ID and Client Secret are correct
- Regenerate credentials in Cribl Cloud if needed
- Check credentials have sufficient permissions

### "name attribute must be unique"
**Cause**: Worker group already exists
**Solution**:
- Use a different `WORKER_GROUP_ID`
- Or delete existing group first

### Pack installation fails
**Cause**: Various - group doesn't exist, invalid source URL
**Solution**:
- Verify worker group was created successfully
- For GitHub: `git+https://github.com/criblpacks/pack-name.git`
- For Dispensary: `https://packs.cribl.io/dl/pack-name/version/pack-name-version.crbl`

### Terraform provider errors
**Cause**: Provider not initialized
**Solution**: Run `terraform init`

## API URL Format Reference

**Production:**
- Base: `https://{workspace}-{orgId}.cribl.cloud/api/v1`
- Auth: `https://login.cribl.cloud/oauth/token`
- Audience: `https://api.cribl.cloud`

**Staging:**
- Base: `https://{workspace}-{orgId}.cribl-staging.cloud/api/v1`
- Auth: `https://login.cribl-staging.cloud/oauth/token`
- Audience: `https://api.cribl-staging.cloud`

**Worker Group context** (for pack operations):
- Add `/m/{groupId}` to base URL

## Pack Sources

**GitHub:**
```
git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git
```

**Pack Dispensary:**
```
https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl
```

Browse packs at https://packs.cribl.io

## Helpful Commands

```bash
# Terraform
terraform init          # Initialize provider
terraform plan          # Preview changes
terraform apply         # Apply changes
terraform destroy       # Remove all resources

# Python
python3 -m venv venv              # Create virtual environment
source venv/bin/activate          # Activate (Linux/Mac)
pip install -r requirements.txt   # Install dependencies
python3 create_wg_with_pack.py    # Run quickstart
```

## Project Structure

```
criblascode-quickstart/
├── CLAUDE.md                    # This file
├── README.md                    # Main documentation
├── terraform/
│   ├── main.tf                  # Pack resources
│   ├── variables.tf             # Input variables
│   ├── provider.tf              # Cribl provider config
│   ├── commit_deploy.tf         # Commit/deploy workflow
│   ├── terraform.tfvars.example
│   └── examples/
│       ├── create-wg-with-pack/
│       └── install-packs/
└── sdk/
    └── python/
        ├── config.py            # Configuration loader
        ├── auth.py              # Authentication helpers
        ├── worker_groups.py     # Worker group operations
        ├── packs.py             # Pack operations
        ├── create_wg_with_pack.py
        ├── requirements.txt
        └── .env.example
```
