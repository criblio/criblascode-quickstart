"""
Worker Group operations for Cribl Cloud.

Provides functions to create, list, and manage worker groups.
"""

from cribl_control_plane.models import ProductsCore

from auth import get_client


def create_worker_group(
    group_id: str,
    name: str,
    description: str = "Worker group created via Python SDK",
):
    """
    Create a new worker group in Cribl Cloud.

    Args:
        group_id: Unique identifier for the worker group (no spaces, lowercase)
        name: Display name for the worker group
        description: Optional description

    Returns:
        The created worker group object

    Raises:
        Exception: If worker group creation fails

    Example:
        group = create_worker_group(
            group_id="my-wg",
            name="My Worker Group",
            description="Handles production logs"
        )
    """
    with get_client() as client:
        result = client.groups.create(
            id=group_id,
            name=name,
            description=description,
            product=ProductsCore.STREAM,
        )
    return result


def list_worker_groups():
    """
    List all worker groups in the organization.

    Returns:
        List of worker group objects

    Example:
        groups = list_worker_groups()
        for group in groups:
            print(group.id, group.name)
    """
    with get_client() as client:
        result = client.groups.list()
    return result


def get_worker_group(group_id: str):
    """
    Get a specific worker group by ID.

    Args:
        group_id: The ID of the worker group

    Returns:
        The worker group object

    Example:
        group = get_worker_group("my-wg")
        print(group.name)
    """
    with get_client() as client:
        result = client.groups.get(id=group_id)
    return result


def delete_worker_group(group_id: str):
    """
    Delete a worker group.

    Args:
        group_id: The ID of the worker group to delete

    Returns:
        Deletion result

    Example:
        delete_worker_group("my-wg")
    """
    with get_client() as client:
        result = client.groups.delete(id=group_id)
    return result
