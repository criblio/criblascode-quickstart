"""
Configuration management for Cribl as Code quickstart.

Loads configuration from environment variables and .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


# Required credentials
CRIBL_CLIENT_ID = os.getenv("CRIBL_CLIENT_ID")
CRIBL_CLIENT_SECRET = os.getenv("CRIBL_CLIENT_SECRET")
CRIBL_ORGANIZATION_ID = os.getenv("CRIBL_ORGANIZATION_ID")

# Optional configuration with defaults
CRIBL_WORKSPACE = os.getenv("CRIBL_WORKSPACE", "main")
CRIBL_DOMAIN = os.getenv(
    "CRIBL_DOMAIN", "cribl.cloud"
)  # Use "cribl-staging.cloud" for staging

# Construct the base URL for Cribl Cloud API
# Format: https://{workspace}-{orgId}.{domain}/api/v1
CRIBL_BASE_URL = (
    f"https://{CRIBL_WORKSPACE}-{CRIBL_ORGANIZATION_ID}.{CRIBL_DOMAIN}/api/v1"
)

# Auth URLs - different for staging vs production
if "staging" in CRIBL_DOMAIN:
    CRIBL_TOKEN_URL = "https://login.cribl-staging.cloud/oauth/token"
    CRIBL_AUDIENCE = "https://api.cribl-staging.cloud"
else:
    CRIBL_TOKEN_URL = "https://login.cribl.cloud/oauth/token"
    CRIBL_AUDIENCE = "https://api.cribl.cloud"


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
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Set these variables in your environment or create a .env file.\n"
            "See .env.example for reference."
        )


def get_config():
    """Return a dictionary of all configuration values."""
    return {
        "client_id": CRIBL_CLIENT_ID,
        "client_secret": CRIBL_CLIENT_SECRET,
        "organization_id": CRIBL_ORGANIZATION_ID,
        "workspace": CRIBL_WORKSPACE,
        "domain": CRIBL_DOMAIN,
        "base_url": CRIBL_BASE_URL,
        "token_url": CRIBL_TOKEN_URL,
        "audience": CRIBL_AUDIENCE,
    }
