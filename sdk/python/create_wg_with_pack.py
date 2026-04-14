#!/usr/bin/env python3
"""
Cribl as Code Quickstart - Create Worker Group with Pack

This script creates a new worker group in Cribl Cloud and installs
a pack from the Pack Dispensary.

Usage:
    python create_wg_with_pack.py

Environment Variables:
    Required:
        CRIBL_CLIENT_ID       - Your Cribl Cloud API Client ID
        CRIBL_CLIENT_SECRET   - Your Cribl Cloud API Client Secret
        CRIBL_ORGANIZATION_ID - Your Cribl Cloud Organization ID

    Optional:
        CRIBL_WORKSPACE       - Workspace name (default: "main")
        CRIBL_DOMAIN          - Domain (default: "cribl.cloud", use "cribl-staging.cloud" for staging)
        WORKER_GROUP_ID       - Worker group identifier (default: "quickstart-wg")
        WORKER_GROUP_NAME     - Worker group display name (default: "Quickstart Worker Group")
        PACK_ID               - Pack identifier (default: "cribl-aws-vpcflow-logs")
        PACK_SOURCE           - Pack source URL
"""

import os
import sys

from config import (
    validate_config,
    CRIBL_ORGANIZATION_ID,
    CRIBL_WORKSPACE,
    CRIBL_BASE_URL,
)
from worker_groups import create_worker_group
from packs import install_pack


# Worker group configuration (with defaults)
WORKER_GROUP_ID = os.getenv("WORKER_GROUP_ID", "quickstart-wg")
WORKER_GROUP_NAME = os.getenv("WORKER_GROUP_NAME", "Quickstart Worker Group")
WORKER_GROUP_DESCRIPTION = os.getenv(
    "WORKER_GROUP_DESCRIPTION", "Worker group created via Python SDK quickstart"
)

# Pack configuration (defaults to AWS VPC Flow Logs)
PACK_ID = os.getenv("PACK_ID", "cribl-aws-vpcflow-logs")
PACK_SOURCE = os.getenv(
    "PACK_SOURCE", "git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git"
)


def main():
    """Main entry point for the script."""
    print("=" * 60)
    print("Cribl as Code Quickstart - Python SDK")
    print("=" * 60)

    # Validate configuration before proceeding
    try:
        validate_config()
    except ValueError as e:
        print(f"\nConfiguration error: {e}")
        sys.exit(1)

    print("\nConnecting to Cribl Cloud...")
    print(f"  Organization: {CRIBL_ORGANIZATION_ID}")
    print(f"  Workspace: {CRIBL_WORKSPACE}")
    print(f"  API URL: {CRIBL_BASE_URL}")

    # Step 1: Create the worker group
    print(f"\nCreating worker group '{WORKER_GROUP_NAME}'...")
    try:
        create_worker_group(
            group_id=WORKER_GROUP_ID,
            name=WORKER_GROUP_NAME,
            description=WORKER_GROUP_DESCRIPTION,
        )
        print("Worker group created successfully!")
        print(f"  ID: {WORKER_GROUP_ID}")
        print(f"  Name: {WORKER_GROUP_NAME}")
    except Exception as e:
        print(f"\nError creating worker group: {e}")
        sys.exit(1)

    # Step 2: Install the pack into the worker group
    print(f"\nInstalling pack '{PACK_ID}' into worker group '{WORKER_GROUP_ID}'...")
    try:
        install_pack(
            group_id=WORKER_GROUP_ID,
            source=PACK_SOURCE,
            pack_id=PACK_ID,
        )
        print("Pack installed successfully!")
        print(f"  Pack ID: {PACK_ID}")
        print(f"  Source: {PACK_SOURCE}")
    except Exception as e:
        print(f"\nError installing pack: {e}")
        sys.exit(1)

    # Success summary
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print("\nYour new worker group is ready:")
    print(f"  - Worker Group: {WORKER_GROUP_NAME} ({WORKER_GROUP_ID})")
    print(f"  - Pack Installed: {PACK_ID}")
    print("\nNext steps:")
    print("  1. Log into Cribl Cloud to view your new worker group")
    print("  2. Configure the pack's sources and destinations")
    print("  3. Deploy workers to the group")
    print("\nFor more information, visit: https://docs.cribl.io")


if __name__ == "__main__":
    main()
