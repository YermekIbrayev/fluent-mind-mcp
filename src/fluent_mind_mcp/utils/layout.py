"""Layout utilities for positioning Flowise chatflow nodes.

WHY: Provides automatic node positioning algorithms to create beautiful,
non-overlapping diagram layouts when connecting nodes programmatically.
"""

import json
from typing import Any


def apply_hierarchical_layout(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    spacing_x: int = 400,
    spacing_y: int = 250,
    start_x: int = 100,
    start_y: int = 100
) -> list[dict[str, Any]]:
    """Apply hierarchical layout to nodes based on edge connections.

    WHY: Creates left-to-right flow layout where nodes are positioned in
    columns based on their depth in the graph. Prevents node overlap and
    creates clear visual hierarchy.

    Algorithm:
    1. Build adjacency list from edges
    2. Compute depth (column) for each node using BFS from sources
    3. Position nodes in columns with vertical spacing
    4. Set standard node dimensions (300x600 default for Flowise)

    Args:
        nodes: List of node objects with id, position, data
        edges: List of edge objects with source, target
        spacing_x: Horizontal spacing between columns (default: 400px)
        spacing_y: Vertical spacing between nodes (default: 250px)
        start_x: Starting X coordinate (default: 100px)
        start_y: Starting Y coordinate (default: 100px)

    Returns:
        Updated nodes list with new position coordinates
    """
    if not nodes:
        return nodes

    # Build adjacency list for graph traversal
    adjacency: dict[str, list[str]] = {node["id"]: [] for node in nodes}
    in_degree: dict[str, int] = {node["id"]: 0 for node in nodes}

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source and target:
            adjacency[source].append(target)
            in_degree[target] = in_degree.get(target, 0) + 1

    # Find source nodes (nodes with no incoming edges)
    sources = [node_id for node_id, degree in in_degree.items() if degree == 0]

    if not sources:
        # Fallback: if no clear sources (circular graph), use first node
        sources = [nodes[0]["id"]]

    # BFS to assign depth (column) to each node
    node_depths: dict[str, int] = {}
    queue = [(source, 0) for source in sources]
    visited = set()

    while queue:
        node_id, depth = queue.pop(0)
        if node_id in visited:
            continue
        visited.add(node_id)

        # Assign depth (prefer max depth if multiple paths)
        if node_id not in node_depths or depth > node_depths[node_id]:
            node_depths[node_id] = depth

        # Add children to queue
        for child in adjacency.get(node_id, []):
            if child not in visited:
                queue.append((child, depth + 1))

    # Handle disconnected nodes (assign to depth 0)
    for node in nodes:
        if node["id"] not in node_depths:
            node_depths[node["id"]] = 0

    # Group nodes by depth (column)
    columns: dict[int, list[str]] = {}
    for node_id, depth in node_depths.items():
        if depth not in columns:
            columns[depth] = []
        columns[depth].append(node_id)

    # Position nodes in columns
    node_positions: dict[str, dict[str, int]] = {}

    for depth, column_nodes in sorted(columns.items()):
        x = start_x + (depth * spacing_x)

        # Center nodes vertically in column
        num_nodes = len(column_nodes)
        for i, node_id in enumerate(column_nodes):
            y = start_y + (i * spacing_y)
            node_positions[node_id] = {"x": x, "y": y}

    # Update node positions
    for node in nodes:
        if node["id"] in node_positions:
            pos = node_positions[node["id"]]
            node["position"] = pos
            node["positionAbsolute"] = pos  # Flowise uses both

            # Set standard dimensions if not present
            if "width" not in node:
                node["width"] = 300
            if "height" not in node:
                node["height"] = 600

    return nodes


def calculate_node_bounds(nodes: list[dict[str, Any]]) -> dict[str, int]:
    """Calculate the bounding box of all nodes.

    WHY: Useful for centering layouts or checking if nodes fit in viewport.

    Args:
        nodes: List of node objects with position

    Returns:
        Dictionary with min_x, max_x, min_y, max_y, width, height
    """
    if not nodes:
        return {
            "min_x": 0, "max_x": 0,
            "min_y": 0, "max_y": 0,
            "width": 0, "height": 0
        }

    positions = [node.get("position", {}) for node in nodes]
    widths = [node.get("width", 300) for node in nodes]
    heights = [node.get("height", 600) for node in nodes]

    min_x = min(p.get("x", 0) for p in positions)
    max_x = max(p.get("x", 0) + w for p, w in zip(positions, widths))
    min_y = min(p.get("y", 0) for p in positions)
    max_y = max(p.get("y", 0) + h for p, h in zip(positions, heights))

    return {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "width": max_x - min_x,
        "height": max_y - min_y
    }


def format_flowdata_for_display(flow_data: str, indent: int = 2) -> str:
    """Pretty-print flowData JSON for human readability.

    WHY: Makes generated flowData easier to inspect and debug.

    Args:
        flow_data: JSON string of flowData
        indent: Number of spaces for indentation (default: 2)

    Returns:
        Formatted JSON string
    """
    try:
        parsed = json.loads(flow_data)
        return json.dumps(parsed, indent=indent)
    except json.JSONDecodeError:
        return flow_data  # Return as-is if invalid JSON
