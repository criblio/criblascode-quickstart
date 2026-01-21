#!/usr/bin/env python3
"""
Cribl as Code Quickstart - Python SDK Example

This script creates a new worker group in Cribl Cloud and installs
the AWS VPC Flow Logs pack from the Pack Dispensary.

Prerequisites:
    - Cribl Cloud account with API credentials
    - Python 3.9+
    - Dependencies installed: pip install -r requirements.txt

Environment Variables:
    CRIBL_CLIENT_ID      - Your Cribl Cloud API Client ID
    CRIBL_CLIENT_SECRET  - Your Cribl Cloud API Client Secret
    CRIBL_ORGANIZATION_ID - Your Cribl Cloud Organization ID

Optional Environment Variables:
    WORKER_GROUP_ID      - Worker group identifier (default: quickstart-wg)
    WORKER_GROUP_NAME    - Worker group display name (default: Quickstart Worker Group)
    PACK_SOURCE          - Pack source URL (default: AWS VPC Flow Logs pack)
"""

import os
import sys
from dotenv import load_dotenv

from cribl_control_plane import CriblControlPlane, models
from cribl_control_plane.models import Security

# Load environment variables from .env file if present
load_dotenv()

# Configuration from environment variables
CRIBL_CLIENT_ID = os.getenv("CRIBL_CLIENT_ID")
CRIBL_CLIENT_SECRET = os.getenv("CRIBL_CLIENT_SECRET")
CRIBL_ORGANIZATION_ID = os.getenv("CRIBL_ORGANIZATION_ID")

# Worker group configuration (with defaults)
WORKER_GROUP_ID = os.getenv("WORKER_GROUP_ID", "quickstart-wg")
WORKER_GROUP_NAME = os.getenv("WORKER_GROUP_NAME", "Quickstart Worker Group")
WORKER_GROUP_DESCRIPTION = os.getenv(
    "WORKER_GROUP_DESCRIPTION",
    "Worker group created via Python SDK quickstart"
)

# Pack configuration (defaults to AWS VPC Flow Logs)
PACK_ID = os.getenv("PACK_ID", "cribl-aws-vpcflow-logs")
PACK_SOURCE = os.getenv(
    "PACK_SOURCE",
    "https://github.com/criblpacks/cribl-aws-vpcflow-logs"
)


def validate_config():
    """Validate that required environment variables are set."""
    missing = []
    if not CRIBL_CLIENT_ID:
        missing.append("CRIBL_CLIENT_ID")
    if not CRIBL_CLIENT_SECRET:
        missing.append("CRIBL_CLIENT_SECRET")
    if not CRIBL_ORGANIZATION_ID:
        missing.append("CRIBL_ORGANIZATION_ID")

    if missing:
        print("Error: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nSet these variables in your environment or create a .env file.")
        print("See .env.example for reference.")
        sys.exit(1)


def create_worker_group(client):
    """
    Create a new worker group in Cribl Cloud.

    Args:
        client: Authenticated CriblControlPlane client

    Returns:
        The created worker group object
    """
    print(f"\nCreating worker group '{WORKER_GROUP_NAME}'...")

    # Create the worker group using the groups API
    # The group is created as a Stream worker group (product="stream")
    result = client.groups.create(
        request_body={
            "id": WORKER_GROUP_ID,
            "name": WORKER_GROUP_NAME,
            "description": WORKER_GROUP_DESCRIPTION,
            "product": "stream",
        }
    )

    print(f"Worker group created successfully!")
    print(f"  ID: {WORKER_GROUP_ID}")
    print(f"  Name: {WORKER_GROUP_NAME}")

    return result


def install_pack(client, group_id):
    """
    Install a pack from Pack Dispensary into the worker group.

    Args:
        client: Authenticated CriblControlPlane client
        group_id: The ID of the worker group to install the pack into

    Returns:
        The pack installation result
    """
    print(f"\nInstalling pack '{PACK_ID}' into worker group '{group_id}'...")

    # Install the pack from the Pack Dispensary source URL
    # The source URL points to the GitHub repository for the pack
    result = client.packs.install(
        group_id=group_id,
        request_body={
            "source": PACK_SOURCE,
        }
    )

    print(f"Pack installed successfully!")
    print(f"  Pack ID: {PACK_ID}")
    print(f"  Source: {PACK_SOURCE}")

    return result


def main():
    """Main entry point for the script."""
    print("=" * 60)
    print("Cribl as Code Quickstart - Python SDK")
    print("=" * 60)

    # Validate configuration before proceeding
    validate_config()

    print(f"\nConnecting to Cribl Cloud...")
    print(f"  Organization: {CRIBL_ORGANIZATION_ID}")

    # Initialize the Cribl Control Plane client with OAuth credentials
    # This uses client credentials flow for authentication
    with CriblControlPlane(
        server_url=f"https://api.cribl.cloud/{CRIBL_ORGANIZATION_ID}",
        security=Security(
            client_id=CRIBL_CLIENT_ID,
            client_secret=CRIBL_CLIENT_SECRET,
        ),
    ) as client:

        # Step 1: Create the worker group
        try:
            create_worker_group(client)
        except Exception as e:
            print(f"\nError creating worker group: {e}")
            sys.exit(1)

        # Step 2: Install the pack into the worker group
        try:
            install_pack(client, WORKER_GROUP_ID)
        except Exception as e:
            print(f"\nError installing pack: {e}")
            sys.exit(1)

    # Success summary
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print(f"\nYour new worker group is ready:")
    print(f"  - Worker Group: {WORKER_GROUP_NAME} ({WORKER_GROUP_ID})")
    print(f"  - Pack Installed: {PACK_ID}")
    print(f"\nNext steps:")
    print("  1. Log into Cribl Cloud to view your new worker group")
    print("  2. Configure the pack's sources and destinations")
    print("  3. Deploy workers to the group")
    print("\nFor more information, visit: https://docs.cribl.io")


if __name__ == "__main__":
    main()
