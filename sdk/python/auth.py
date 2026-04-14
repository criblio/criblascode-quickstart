"""
Authentication helpers for Cribl Cloud API.

Provides functions to create authenticated clients for the Cribl Control Plane SDK.
"""

from cribl_control_plane import CriblControlPlane
from cribl_control_plane.models import Security, SchemeClientOauth

from config import (
    CRIBL_CLIENT_ID,
    CRIBL_CLIENT_SECRET,
    CRIBL_BASE_URL,
    CRIBL_TOKEN_URL,
    CRIBL_AUDIENCE,
)


def get_client():
    """
    Create an authenticated Cribl Control Plane client.

    Returns:
        CriblControlPlane: Authenticated client for API operations

    Example:
        with get_client() as client:
            groups = client.groups.list()
    """
    return CriblControlPlane(
        server_url=CRIBL_BASE_URL,
        security=Security(
            client_oauth=SchemeClientOauth(
                client_id=CRIBL_CLIENT_ID,
                client_secret=CRIBL_CLIENT_SECRET,
                audience=CRIBL_AUDIENCE,
                token_url=CRIBL_TOKEN_URL,
            ),
        ),
    )


def get_group_client(group_id: str):
    """
    Create an authenticated client scoped to a specific worker group.

    The Cribl API requires /m/{groupId} path for worker group operations
    like installing packs.

    Args:
        group_id: The ID of the worker group

    Returns:
        CriblControlPlane: Authenticated client for group-specific operations

    Example:
        with get_group_client("my-worker-group") as client:
            client.packs.install(...)
    """
    group_url = f"{CRIBL_BASE_URL}/m/{group_id}"
    return CriblControlPlane(
        server_url=group_url,
        security=Security(
            client_oauth=SchemeClientOauth(
                client_id=CRIBL_CLIENT_ID,
                client_secret=CRIBL_CLIENT_SECRET,
                audience=CRIBL_AUDIENCE,
                token_url=CRIBL_TOKEN_URL,
            ),
        ),
    )
