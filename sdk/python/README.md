# Cribl as Code - Python SDK

Deploy a Cribl Cloud worker group with the AWS VPC Flow Logs pack using Python.

## Prerequisites

- Python 3.9+
- Cribl Cloud API credentials (Client ID, Client Secret, Organization ID)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
# Edit .env with your values

# 3. Run the script
python create_wg_with_pack.py
```

## Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Example environment variables |
| `create_wg_with_pack.py` | Main script |

## Configuration

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `CRIBL_CLIENT_ID` | Cribl Cloud API Client ID |
| `CRIBL_CLIENT_SECRET` | Cribl Cloud API Client Secret |
| `CRIBL_ORGANIZATION_ID` | Cribl Cloud Organization ID |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WORKER_GROUP_ID` | Worker group identifier | `quickstart-wg` |
| `WORKER_GROUP_NAME` | Worker group display name | `Quickstart Worker Group` |
| `WORKER_GROUP_DESCRIPTION` | Worker group description | `Worker group created via Python SDK quickstart` |
| `PACK_ID` | Pack identifier | `cribl-aws-vpcflow-logs` |
| `PACK_SOURCE` | Pack source URL | GitHub URL for AWS VPC Flow Logs |

## Using a .env File

Create a `.env` file in the same directory as the script:

```bash
CRIBL_CLIENT_ID=your-client-id
CRIBL_CLIENT_SECRET=your-client-secret
CRIBL_ORGANIZATION_ID=your-org-id
```

The script uses `python-dotenv` to automatically load these values.

## Using Environment Variables Directly

```bash
export CRIBL_CLIENT_ID="your-client-id"
export CRIBL_CLIENT_SECRET="your-client-secret"
export CRIBL_ORGANIZATION_ID="your-org-id"

python create_wg_with_pack.py
```

## Expected Output

```
============================================================
Cribl as Code Quickstart - Python SDK
============================================================

Connecting to Cribl Cloud...
  Organization: your-org-id

Creating worker group 'Quickstart Worker Group'...
Worker group created successfully!
  ID: quickstart-wg
  Name: Quickstart Worker Group

Installing pack 'cribl-aws-vpcflow-logs' into worker group 'quickstart-wg'...
Pack installed successfully!
  Pack ID: cribl-aws-vpcflow-logs
  Source: https://github.com/criblpacks/cribl-aws-vpcflow-logs

============================================================
SUCCESS!
============================================================

Your new worker group is ready:
  - Worker Group: Quickstart Worker Group (quickstart-wg)
  - Pack Installed: cribl-aws-vpcflow-logs

Next steps:
  1. Log into Cribl Cloud to view your new worker group
  2. Configure the pack's sources and destinations
  3. Deploy workers to the group
```

## Extending the Script

### Creating Multiple Worker Groups

```python
groups = [
    {"id": "dev-wg", "name": "Development"},
    {"id": "prod-wg", "name": "Production"},
]

for group in groups:
    client.groups.create(
        request_body={
            "id": group["id"],
            "name": group["name"],
            "product": "stream",
        }
    )
```

### Installing Multiple Packs

```python
packs = [
    {"id": "pack1", "source": "https://github.com/criblpacks/pack1"},
    {"id": "pack2", "source": "https://github.com/criblpacks/pack2"},
]

for pack in packs:
    client.packs.install(
        group_id=WORKER_GROUP_ID,
        request_body={"source": pack["source"]}
    )
```

## Error Handling

The script includes basic error handling for common scenarios:

- Missing environment variables
- Worker group creation failures
- Pack installation failures

For production use, consider adding:

- Retry logic for transient failures
- Logging to file
- Validation of worker group/pack names

## Resources

- [Cribl Python SDK](https://github.com/criblio/cribl_control_plane_sdk_python)
- [Cribl API Documentation](https://docs.cribl.io/stream/api-reference/)
- [Pack Dispensary](https://packs.cribl.io)
