"""Clean node templates by removing UI metadata before API submission.

WHY: Node templates extracted from Flowise contain UI state and metadata
that causes errors when submitted back via API. This module strips those fields.
"""

from typing import Any, Dict


def clean_node_for_api(node: Dict[str, Any]) -> Dict[str, Any]:
    """Remove UI metadata from node to make it API-compatible.

    WHY: Flowise UI adds display hints, file paths, and other metadata that
    should not be sent back when creating chatflows via API. These fields
    cause TypeError "Cannot read properties of undefined (reading 'length')".

    Args:
        node: Node dictionary from template

    Returns:
        Cleaned node safe for API submission
    """
    # Create clean copy
    clean = {
        "id": node["id"],
        "type": node["type"],
        "position": node["position"],
        "data": {}
    }

    # Copy essential data fields only
    data = node.get("data", {})
    essential_data_fields = ["id", "label", "name", "category", "baseClasses",
                             "inputs", "outputs"]

    for field in essential_data_fields:
        if field in data:
            clean["data"][field] = data[field]

    # Clean inputParams
    if "inputParams" in data:
        clean["data"]["inputParams"] = []
        for param in data["inputParams"]:
            clean_param = {
                "id": param["id"],
                "name": param["name"],
                "type": param["type"]
            }
            # Keep optional flag if present
            if "optional" in param:
                clean_param["optional"] = param["optional"]
            # Keep required flag if present
            if "required" in param:
                clean_param["required"] = param["required"]
            clean["data"]["inputParams"].append(clean_param)

    # Clean inputAnchors
    if "inputAnchors" in data:
        clean["data"]["inputAnchors"] = []
        for anchor in data["inputAnchors"]:
            clean_anchor = {
                "id": anchor["id"],
                "name": anchor["name"],
                "label": anchor["label"],
                "type": anchor["type"]
            }
            # Keep optional/required flags if present
            if "optional" in anchor:
                clean_anchor["optional"] = anchor["optional"]
            if "required" in anchor:
                clean_anchor["required"] = anchor["required"]
            clean["data"]["inputAnchors"].append(clean_anchor)

    # Clean outputAnchors
    if "outputAnchors" in data:
        clean["data"]["outputAnchors"] = []
        for anchor in data["outputAnchors"]:
            clean_anchor = {
                "id": anchor["id"],
                "name": anchor["name"],
                "label": anchor["label"],
                "type": anchor["type"]
            }
            # Keep description if minimal (working chatflows don't have it)
            # Skip it for now
            clean["data"]["outputAnchors"].append(clean_anchor)

    return clean


def clean_flow_data(flow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean entire flowData structure.

    Args:
        flow_data: FlowData dictionary with nodes and edges

    Returns:
        Cleaned flowData
    """
    return {
        "nodes": [clean_node_for_api(node) for node in flow_data.get("nodes", [])],
        "edges": flow_data.get("edges", []),
        "viewport": flow_data.get("viewport", {"x": 0, "y": 0, "zoom": 1})
    }
