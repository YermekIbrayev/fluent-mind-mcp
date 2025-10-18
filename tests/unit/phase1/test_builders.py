"""Test data builders for Phase 1 tests.

Provides fluent builders for creating test data structures.

WHY: Builder pattern improves test readability and reduces code duplication.
Instead of manually constructing dictionaries, tests can use expressive builders.
"""

from typing import Any


class NodeBuilder:
    """Builds test node structures with fluent interface.

    Example:
        node = (NodeBuilder()
                .with_id("1")
                .with_name("chatOpenAI")
                .with_base_classes(["BaseChatModel"])
                .build())
    """

    def __init__(self) -> None:
        """Initialize builder with empty node structure."""
        self._node: dict[str, Any] = {}

    def with_id(self, node_id: str) -> "NodeBuilder":
        """Set node ID."""
        self._node["id"] = node_id
        return self

    def with_name(self, name: str) -> "NodeBuilder":
        """Set node name."""
        self._node["name"] = name
        return self

    def with_base_classes(self, base_classes: list[str]) -> "NodeBuilder":
        """Set node base classes for type matching."""
        self._node["base_classes"] = base_classes
        return self

    def with_inputs(self, inputs: list[str]) -> "NodeBuilder":
        """Set node input types."""
        self._node["inputs"] = inputs
        return self

    def with_outputs(self, outputs: list[str]) -> "NodeBuilder":
        """Set node output types."""
        self._node["outputs"] = outputs
        return self

    def with_required_inputs(self, required_inputs: list[str]) -> "NodeBuilder":
        """Set required input types for validation."""
        self._node["required_inputs"] = required_inputs
        return self

    def with_data(self, data: dict[str, Any]) -> "NodeBuilder":
        """Set node data field (for parameter testing)."""
        self._node["data"] = data
        return self

    def build(self) -> dict[str, Any]:
        """Build and return the node dictionary."""
        return self._node.copy()


class EdgeBuilder:
    """Builds test edge structures with fluent interface.

    Example:
        edge = (EdgeBuilder()
                .from_node("1")
                .to_node("2")
                .with_handles("output_0", "input_0")
                .build())
    """

    def __init__(self) -> None:
        """Initialize builder with empty edge structure."""
        self._edge: dict[str, Any] = {}

    def from_node(self, source_id: str) -> "EdgeBuilder":
        """Set source node ID."""
        self._edge["source"] = source_id
        return self

    def to_node(self, target_id: str) -> "EdgeBuilder":
        """Set target node ID."""
        self._edge["target"] = target_id
        return self

    def with_handles(self, source_handle: str, target_handle: str) -> "EdgeBuilder":
        """Set source and target handles."""
        self._edge["sourceHandle"] = source_handle
        self._edge["targetHandle"] = target_handle
        return self

    def with_id(self, edge_id: str) -> "EdgeBuilder":
        """Set edge ID."""
        self._edge["id"] = edge_id
        return self

    def build(self) -> dict[str, Any]:
        """Build and return the edge dictionary."""
        return self._edge.copy()


class FlowDataBuilder:
    """Builds complete flowData structures with fluent interface.

    Example:
        flow_data = (FlowDataBuilder()
                     .add_node(node1)
                     .add_node(node2)
                     .add_edge(edge1)
                     .build())
    """

    def __init__(self) -> None:
        """Initialize builder with empty flowData structure."""
        self._flow_data: dict[str, Any] = {
            "nodes": [],
            "edges": []
        }

    def with_nodes(self, nodes: list[dict[str, Any]]) -> "FlowDataBuilder":
        """Set all nodes at once."""
        self._flow_data["nodes"] = nodes.copy()
        return self

    def with_edges(self, edges: list[dict[str, Any]]) -> "FlowDataBuilder":
        """Set all edges at once."""
        self._flow_data["edges"] = edges.copy()
        return self

    def add_node(self, node: dict[str, Any]) -> "FlowDataBuilder":
        """Add a single node."""
        self._flow_data["nodes"].append(node)
        return self

    def add_edge(self, edge: dict[str, Any]) -> "FlowDataBuilder":
        """Add a single edge."""
        self._flow_data["edges"].append(edge)
        return self

    def build(self) -> dict[str, Any]:
        """Build and return the flowData dictionary."""
        return self._flow_data.copy()
