"""
Pack operations for Cribl Cloud.

Provides functions to install, list, and manage packs in worker groups.
"""

from typing import Optional

from cribl_control_plane.models import PackRequestBody2

from auth import get_group_client


def install_pack(
    group_id: str,
    source: str,
    pack_id: Optional[str] = None,
):
    """
    Install a pack into a worker group.

    Args:
        group_id: The ID of the worker group to install the pack into
        source: Pack source URL. Can be:
            - GitHub: "git+https://github.com/criblpacks/pack-name.git"
            - Pack Dispensary: "https://packs.cribl.io/dl/pack-name/version/pack-name-version.crbl"
        pack_id: Optional pack identifier (defaults to pack name from source)

    Returns:
        Pack installation result

    Example:
        # Install from GitHub
        install_pack(
            group_id="my-wg",
            source="git+https://github.com/criblpacks/cribl-aws-vpcflow-logs.git",
            pack_id="cribl-aws-vpcflow-logs"
        )

        # Install from Pack Dispensary
        install_pack(
            group_id="my-wg",
            source="https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/"
                   "cribl-aws-bedrock-io-2.0.0.crbl"
        )
    """
    with get_group_client(group_id) as client:
        request = PackRequestBody2(source=source)
        if pack_id:
            request = PackRequestBody2(source=source, id=pack_id)
        result = client.packs.install(request=request)
    return result


def list_packs(group_id: str):
    """
    List all packs installed in a worker group.

    Args:
        group_id: The ID of the worker group

    Returns:
        List of installed packs

    Example:
        packs = list_packs("my-wg")
        for pack in packs:
            print(pack.id)
    """
    with get_group_client(group_id) as client:
        result = client.packs.list()
    return result


def get_pack(group_id: str, pack_id: str):
    """
    Get details of a specific pack.

    Args:
        group_id: The ID of the worker group
        pack_id: The ID of the pack

    Returns:
        Pack details

    Example:
        pack = get_pack("my-wg", "cribl-aws-vpcflow-logs")
    """
    with get_group_client(group_id) as client:
        result = client.packs.get(id=pack_id)
    return result


def delete_pack(group_id: str, pack_id: str):
    """
    Uninstall a pack from a worker group.

    Args:
        group_id: The ID of the worker group
        pack_id: The ID of the pack to uninstall

    Returns:
        Deletion result

    Example:
        delete_pack("my-wg", "cribl-aws-vpcflow-logs")
    """
    with get_group_client(group_id) as client:
        result = client.packs.delete(id=pack_id)
    return result
