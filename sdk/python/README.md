# Cribl as Code - Python SDK

Deploy and manage Cribl Cloud worker groups and packs using Python.

## Prerequisites

- Python 3.9+
- Cribl Cloud API credentials (Client ID, Client Secret, Organization ID)

## Quick Start

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env with your values

# 4. Run the quickstart
python3 create_wg_with_pack.py
```

## Configuration

Edit your `.env` file with your Cribl Cloud credentials:

```bash
# Required
CRIBL_CLIENT_ID=your-client-id
CRIBL_CLIENT_SECRET=your-client-secret
CRIBL_ORGANIZATION_ID=your-org-id

# Optional (defaults shown)
CRIBL_WORKSPACE=main
CRIBL_DOMAIN=cribl.cloud          # Use "cribl-staging.cloud" for staging

# Worker Group (optional)
WORKER_GROUP_ID=quickstart-wg
WORKER_GROUP_NAME=Quickstart Worker Group

# Pack (optional)
PACK_ID=cribl-aws-vpcflow-logs
PACK_SOURCE=git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git
```

### Finding Your Credentials

1. Log into [Cribl Cloud](https://cribl.cloud)
2. Go to **Settings > API Credentials**
3. Create a new credential and note the Client ID and Secret
4. Your Organization ID is in the URL: `https://{workspace}-{org-id}.cribl.cloud`

## Project Structure

```
sdk/python/
├── config.py              # Configuration & environment variables
├── auth.py                # Authentication helpers
├── worker_groups.py       # Worker group operations
├── packs.py               # Pack operations
├── create_wg_with_pack.py # Main quickstart script
├── requirements.txt       # Python dependencies
└── .env.example           # Example configuration
```

## Usage

### Run the Quickstart Script

```bash
# With defaults from .env
python3 create_wg_with_pack.py

# Override with environment variables
WORKER_GROUP_ID=my-wg WORKER_GROUP_NAME="My Worker Group" python3 create_wg_with_pack.py
```

### Use Modules Directly

Each module can be imported and used independently:

```python
from worker_groups import create_worker_group, list_worker_groups, delete_worker_group
from packs import install_pack, list_packs, delete_pack

# Create a worker group
create_worker_group(
    group_id="production-wg",
    name="Production Worker Group",
    description="Handles production data"
)

# Install a pack from GitHub
install_pack(
    group_id="production-wg",
    source="git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git",
    pack_id="cribl-aws-vpcflow-logs"
)

# Install a pack from Pack Dispensary
install_pack(
    group_id="production-wg",
    source="https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
)

# List all worker groups
groups = list_worker_groups()

# List packs in a group
packs = list_packs("production-wg")

# Clean up
delete_pack("production-wg", "cribl-aws-vpcflow-logs")
delete_worker_group("production-wg")
```

### Interactive Python Session

```bash
source venv/bin/activate
python3
```

```python
>>> from worker_groups import list_worker_groups
>>> groups = list_worker_groups()
>>> for g in groups.items:
...     print(g.id, g.name)
```

## Module Reference

### config.py

Loads configuration from environment variables and `.env` file.

| Variable | Description |
|----------|-------------|
| `CRIBL_BASE_URL` | Constructed API URL |
| `CRIBL_TOKEN_URL` | OAuth token endpoint |
| `CRIBL_AUDIENCE` | OAuth audience |
| `validate_config()` | Raises error if required vars missing |

### auth.py

Creates authenticated API clients.

| Function | Description |
|----------|-------------|
| `get_client()` | Returns client for org-level operations |
| `get_group_client(group_id)` | Returns client scoped to a worker group |

### worker_groups.py

Worker group CRUD operations.

| Function | Description |
|----------|-------------|
| `create_worker_group(group_id, name, description)` | Create a new worker group |
| `list_worker_groups()` | List all worker groups |
| `get_worker_group(group_id)` | Get a specific worker group |
| `delete_worker_group(group_id)` | Delete a worker group |

### packs.py

Pack CRUD operations (requires group context).

| Function | Description |
|----------|-------------|
| `install_pack(group_id, source, pack_id)` | Install a pack |
| `list_packs(group_id)` | List packs in a group |
| `get_pack(group_id, pack_id)` | Get pack details |
| `delete_pack(group_id, pack_id)` | Uninstall a pack |

## Pack Sources

Packs can be installed from:

**GitHub:**
```
git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git
```

**Pack Dispensary:**
```
https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl
```

Browse available packs at [packs.cribl.io](https://packs.cribl.io)

## Troubleshooting

### "Missing required environment variables"

Ensure your `.env` file has the required credentials:
- `CRIBL_CLIENT_ID`
- `CRIBL_CLIENT_SECRET`
- `CRIBL_ORGANIZATION_ID`

### "Unexpected status code 400 from token endpoint"

Check that you're using the correct domain:
- Production: `CRIBL_DOMAIN=cribl.cloud`
- Staging: `CRIBL_DOMAIN=cribl-staging.cloud`

### "name attribute must be unique"

The worker group already exists. Either:
- Use a different `WORKER_GROUP_ID`
- Delete the existing group first

### Connection timeout

Verify the API URL format is correct:
- Should be: `https://{workspace}-{org-id}.{domain}/api/v1`
- Check `CRIBL_WORKSPACE` and `CRIBL_ORGANIZATION_ID`

## Resources

- [Cribl Python SDK](https://github.com/criblio/cribl_control_plane_sdk_python)
- [Cribl API Documentation](https://docs.cribl.io/stream/api-reference/)
- [Pack Dispensary](https://packs.cribl.io)
