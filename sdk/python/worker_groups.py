"""
Worker Group operations for Cribl Cloud.

Provides functions to create, list, and manage worker groups.
"""

from typing import Optional

from cribl_control_plane.models import (
    ProductsCore,
    ConfigGroupCloud,
    CloudProvider,
    EstimatedIngestRateOptionsConfigGroup,
)

from auth import get_client


# Ingest rate options (MB/sec)
INGEST_RATES = {
    12: EstimatedIngestRateOptionsConfigGroup.RATE12_MB_PER_SEC,
    24: EstimatedIngestRateOptionsConfigGroup.RATE24_MB_PER_SEC,
    36: EstimatedIngestRateOptionsConfigGroup.RATE36_MB_PER_SEC,
    48: EstimatedIngestRateOptionsConfigGroup.RATE48_MB_PER_SEC,
    60: EstimatedIngestRateOptionsConfigGroup.RATE60_MB_PER_SEC,
    84: EstimatedIngestRateOptionsConfigGroup.RATE84_MB_PER_SEC,
    120: EstimatedIngestRateOptionsConfigGroup.RATE120_MB_PER_SEC,
    156: EstimatedIngestRateOptionsConfigGroup.RATE156_MB_PER_SEC,
    180: EstimatedIngestRateOptionsConfigGroup.RATE180_MB_PER_SEC,
}

# Cloud providers
CLOUD_PROVIDERS = {
    "aws": CloudProvider.AWS,
    "azure": CloudProvider.AZURE,
}


def create_worker_group(
    group_id: str,
    name: str,
    description: str = "Worker group created via Python SDK",
    on_prem: bool = True,
    cloud_provider: Optional[str] = None,
    cloud_region: Optional[str] = None,
    ingest_rate_mb: int = 12,
):
    """
    Create a new worker group in Cribl Cloud.

    Args:
        group_id: Unique identifier for the worker group (lowercase, hyphens allowed)
        name: Display name for the worker group.
              For cloud groups: must be lowercase with hyphens only (e.g., "my-cloud-wg")
              For on-prem groups: can use spaces and mixed case
        description: Optional description
        on_prem: If True, creates an on-prem worker group (default).
                 If False, creates a cloud-managed worker group.
        cloud_provider: Cloud provider ("aws" or "azure"). Required if on_prem=False.
        cloud_region: Cloud region (e.g., "us-east-1"). Required if on_prem=False.
        ingest_rate_mb: Estimated ingest rate in MB/sec for cloud groups.
                        Options: 12, 24, 36, 48, 60, 84, 120, 156, 180

    Returns:
        The created worker group object

    Raises:
        ValueError: If cloud config is missing when on_prem=False
        Exception: If worker group creation fails

    Example (on-prem):
        group = create_worker_group(
            group_id="my-wg",
            name="My Worker Group",
            on_prem=True
        )

    Example (cloud):
        group = create_worker_group(
            group_id="cloud-wg",
            name="Cloud Worker Group",
            on_prem=False,
            cloud_provider="aws",
            cloud_region="us-east-1",
            ingest_rate_mb=24
        )
    """
    # Build kwargs for the API call
    kwargs = {
        "id": group_id,
        "name": name,
        "description": description,
        "product": ProductsCore.STREAM,
        "on_prem": on_prem,
    }

    if not on_prem:
        # Cloud worker group - validate required fields
        if not cloud_provider:
            raise ValueError("cloud_provider is required for cloud worker groups")
        if not cloud_region:
            raise ValueError("cloud_region is required for cloud worker groups")
        if cloud_provider.lower() not in CLOUD_PROVIDERS:
            raise ValueError(
                f"Invalid cloud_provider: {cloud_provider}. "
                f"Must be one of: {list(CLOUD_PROVIDERS.keys())}"
            )
        if ingest_rate_mb not in INGEST_RATES:
            raise ValueError(
                f"Invalid ingest_rate_mb: {ingest_rate_mb}. "
                f"Must be one of: {list(INGEST_RATES.keys())}"
            )

        kwargs["provisioned"] = True
        kwargs["cloud"] = ConfigGroupCloud(
            provider=CLOUD_PROVIDERS[cloud_provider.lower()],
            region=cloud_region,
        )
        kwargs["estimated_ingest_rate"] = INGEST_RATES[ingest_rate_mb]

    with get_client() as client:
        result = client.groups.create(**kwargs)
    return result


def create_onprem_worker_group(
    group_id: str,
    name: str,
    description: str = "On-prem worker group created via Python SDK",
):
    """
    Create an on-prem worker group (convenience function).

    Args:
        group_id: Unique identifier for the worker group
        name: Display name for the worker group
        description: Optional description

    Returns:
        The created worker group object

    Example:
        group = create_onprem_worker_group("datacenter-wg", "Datacenter Workers")
    """
    return create_worker_group(
        group_id=group_id,
        name=name,
        description=description,
        on_prem=True,
    )


def create_cloud_worker_group(
    group_id: str,
    name: str,
    cloud_provider: str,
    cloud_region: str,
    description: str = "Cloud worker group created via Python SDK",
    ingest_rate_mb: int = 12,
):
    """
    Create a cloud-managed worker group (convenience function).

    Args:
        group_id: Unique identifier for the worker group
        name: Display name for the worker group
        cloud_provider: Cloud provider ("aws" or "azure")
        cloud_region: Cloud region (e.g., "us-east-1", "westus2")
        description: Optional description
        ingest_rate_mb: Estimated ingest rate in MB/sec.
                        Options: 12, 24, 36, 48, 60, 84, 120, 156, 180

    Returns:
        The created worker group object

    Example:
        group = create_cloud_worker_group(
            group_id="aws-prod",
            name="AWS Production",
            cloud_provider="aws",
            cloud_region="us-east-1",
            ingest_rate_mb=48
        )
    """
    return create_worker_group(
        group_id=group_id,
        name=name,
        description=description,
        on_prem=False,
        cloud_provider=cloud_provider,
        cloud_region=cloud_region,
        ingest_rate_mb=ingest_rate_mb,
    )


def list_worker_groups(product: str = "stream"):
    """
    List all worker groups in the organization.

    Args:
        product: Product type ("stream" or "edge"). Defaults to "stream".

    Returns:
        List of worker group objects

    Example:
        groups = list_worker_groups()
        for group in groups.items:
            print(group.id, group.name)
    """
    product_enum = ProductsCore.STREAM if product == "stream" else ProductsCore.EDGE
    with get_client() as client:
        result = client.groups.list(product=product_enum)
    return result


def get_worker_group(group_id: str, product: str = "stream"):
    """
    Get a specific worker group by ID.

    Args:
        group_id: The ID of the worker group
        product: Product type ("stream" or "edge"). Defaults to "stream".

    Returns:
        The worker group object

    Example:
        group = get_worker_group("my-wg")
        print(group.name)
    """
    product_enum = ProductsCore.STREAM if product == "stream" else ProductsCore.EDGE
    with get_client() as client:
        result = client.groups.get(product=product_enum, id=group_id)
    return result


def delete_worker_group(group_id: str, product: str = "stream"):
    """
    Delete a worker group.

    Args:
        group_id: The ID of the worker group to delete
        product: Product type ("stream" or "edge"). Defaults to "stream".

    Returns:
        Deletion result

    Example:
        delete_worker_group("my-wg")
    """
    product_enum = ProductsCore.STREAM if product == "stream" else ProductsCore.EDGE
    with get_client() as client:
        result = client.groups.delete(product=product_enum, id=group_id)
    return result
