"""
Graph utilities for flow execution and validation.

WHY: Provides core graph operations (cycle detection, topological sort,
dependency management) based on Flowise's node connection patterns.

Based on patterns extracted from FlowiseAI/Flowise repository.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque


@dataclass
class FlowConnection:
    """Represents a connection between two nodes."""

    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class FlowGraph:
    """
    Directed graph for flow execution and validation.

    WHY: Provides graph operations needed for:
    - Validating flow structure (no cycles, valid connections)
    - Determining execution order (topological sort)
    - Managing node dependencies during execution
    - Analyzing flow complexity

    Based on Flowise's graph construction patterns from buildAgentflow.ts
    """

    def __init__(self):
        self.nodes: Dict[str, Any] = {}
        self.edges: List[FlowConnection] = []
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.reverse_adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)

    def add_node(self, node_id: str, data: Any = None) -> None:
        """Add a node to the graph.

        WHY: Nodes represent chatflow components. We track them to build
        adjacency lists and validate connections.
        """
        self.nodes[node_id] = data
        if node_id not in self.adjacency_list:
            self.adjacency_list[node_id] = []
        if node_id not in self.reverse_adjacency_list:
            self.reverse_adjacency_list[node_id] = []
        if node_id not in self.in_degree:
            self.in_degree[node_id] = 0

    def add_edge(
        self, source: str, target: str, validate_cycle: bool = True, **kwargs
    ) -> bool:
        """Add an edge between two nodes with cycle detection.

        WHY: Follows Flowise's isValidConnectionAgentflowV2 pattern which
        prevents cycles in AgentFlow V2 to avoid infinite loops.

        Args:
            source: Source node ID
            target: Target node ID
            validate_cycle: Whether to check for cycles (default: True)
            **kwargs: Additional edge metadata

        Returns:
            bool: True if edge was added, False if it would create a cycle
        """
        # Prevent self-connections (Flowise pattern)
        if source == target:
            return False

        # Check if this would create a cycle
        if validate_cycle and self._would_create_cycle(source, target):
            return False

        connection = FlowConnection(source=source, target=target, metadata=kwargs)
        self.edges.append(connection)
        self.adjacency_list[source].append(target)
        self.reverse_adjacency_list[target].append(source)
        self.in_degree[target] += 1

        return True

    def _would_create_cycle(self, source: str, target: str) -> bool:
        """Check if adding edge source->target would create a cycle.

        WHY: Implements Flowise's cycle detection algorithm from genericHelper.js
        Uses DFS to detect if there's already a path from target to source.

        Algorithm from Flowise wouldCreateCycle function:
        1. Build directed graph from existing edges
        2. Check if there's a path from target to source
        3. If yes, adding source→target will create a cycle
        """
        if source == target:
            return True

        visited = set()

        def has_path(current: str, destination: str) -> bool:
            if current == destination:
                return True
            if current in visited:
                return False

            visited.add(current)

            for neighbor in self.adjacency_list.get(current, []):
                if has_path(neighbor, destination):
                    return True

            return False

        # If there's a path from target to source,
        # adding source → target will create a cycle
        return has_path(target, source)

    def get_starting_nodes(self) -> List[str]:
        """Get all nodes with no incoming edges (starting nodes).

        WHY: Execution begins at nodes with zero dependencies, following
        Flowise's getStartingNode pattern from utils/index.ts
        """
        return [node_id for node_id, degree in self.in_degree.items() if degree == 0]

    def get_children(self, node_id: str) -> List[str]:
        """Get all direct children of a node.

        WHY: Used during execution to determine which nodes to process next
        after a node completes. Follows Flowise's graph[nodeId] pattern.
        """
        return self.adjacency_list.get(node_id, [])

    def get_parents(self, node_id: str) -> List[str]:
        """Get all direct parents of a node.

        WHY: Used to determine dependencies and wait for all inputs before
        executing a node. Follows Flowise's reversedGraph pattern.
        """
        return self.reverse_adjacency_list.get(node_id, [])

    def topological_sort(self) -> Optional[List[str]]:
        """Perform topological sort using Kahn's algorithm.

        WHY: Provides a valid execution order that respects all dependencies.
        If a cycle exists, returns None.

        Algorithm:
        1. Start with nodes that have no dependencies (in_degree = 0)
        2. Process each node and reduce in_degree of children
        3. Add children with in_degree = 0 to queue
        4. If all nodes processed, graph is valid (no cycles)

        Returns:
            List of node IDs in topological order, or None if graph has cycle
        """
        # Create a copy to avoid modifying the original
        in_degree_copy = self.in_degree.copy()
        queue = deque([node for node, degree in in_degree_copy.items() if degree == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.adjacency_list[node]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)

        # If result doesn't contain all nodes, there's a cycle
        if len(result) != len(self.nodes):
            return None

        return result

    def get_node_level(self, node_id: str) -> int:
        """Get the hierarchical level of a node (distance from starting nodes).

        WHY: Used for layout positioning and understanding flow depth.

        Level 0: Starting nodes (no parents)
        Level 1: Nodes with only level 0 parents
        Level 2: Nodes with at least one level 1 parent
        etc.

        Returns:
            int: Level number (0 for starting nodes)
        """
        if self.in_degree[node_id] == 0:
            return 0

        # Work backwards through parents to find max parent level
        max_parent_level = -1
        for parent in self.get_parents(node_id):
            parent_level = self.get_node_level(parent)
            max_parent_level = max(max_parent_level, parent_level)

        return max_parent_level + 1

    def get_all_ancestors(self, node_id: str) -> Set[str]:
        """Get all ancestor nodes (all nodes that can reach this node).

        WHY: Useful for understanding full dependency chain and impact analysis.
        """
        ancestors = set()
        queue = deque(self.get_parents(node_id))

        while queue:
            parent = queue.popleft()
            if parent not in ancestors:
                ancestors.add(parent)
                queue.extend(self.get_parents(parent))

        return ancestors

    def get_all_descendants(self, node_id: str) -> Set[str]:
        """Get all descendant nodes (all nodes reachable from this node).

        WHY: Useful for impact analysis when modifying a node.
        """
        descendants = set()
        queue = deque(self.get_children(node_id))

        while queue:
            child = queue.popleft()
            if child not in descendants:
                descendants.add(child)
                queue.extend(self.get_children(child))

        return descendants

    def detect_all_cycles(self) -> List[List[str]]:
        """Detect all cycles in the graph.

        WHY: Comprehensive cycle detection for validation and debugging.

        Returns:
            List of cycles, where each cycle is a list of node IDs
        """
        cycles = []
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
                    return True

            path.pop()
            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                dfs(node)

        return cycles

    def to_dict(self) -> Dict[str, Any]:
        """Export graph structure as dictionary.

        WHY: Useful for serialization, debugging, and analysis.

        Returns:
            Dictionary with nodes, edges, adjacency list, and dependencies
        """
        return {
            "nodes": list(self.nodes.keys()),
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "sourceHandle": edge.source_handle,
                    "targetHandle": edge.target_handle,
                    **edge.metadata,
                }
                for edge in self.edges
            ],
            "adjacency_list": dict(self.adjacency_list),
            "reverse_adjacency_list": dict(self.reverse_adjacency_list),
            "in_degree": dict(self.in_degree),
        }


def build_graph_from_flowdata(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> FlowGraph:
    """Build FlowGraph from Flowise flowData format.

    WHY: Converts Flowise's JSON flowData structure into our graph representation
    for analysis and execution.

    Args:
        nodes: List of node objects with 'id' key
        edges: List of edge objects with 'source' and 'target' keys

    Returns:
        FlowGraph instance
    """
    graph = FlowGraph()

    # Add all nodes
    for node in nodes:
        node_id = node.get("id")
        if node_id:
            graph.add_node(node_id, data=node.get("data"))

    # Add all edges
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source and target:
            graph.add_edge(
                source,
                target,
                validate_cycle=False,  # Don't validate during batch import
                source_handle=edge.get("sourceHandle"),
                target_handle=edge.get("targetHandle"),
            )

    return graph


def generate_unique_node_id(base_name: str, existing_ids: Set[str]) -> str:
    """Generate a unique ID for a node following Flowise pattern.

    WHY: Follows Flowise's getUniqueNodeId pattern from genericHelper.js
    Format: {nodeName}_{counter}

    Args:
        base_name: Base name for the node (e.g., 'llm', 'chatOpenAI')
        existing_ids: Set of already used IDs

    Returns:
        Unique ID string (e.g., 'llm_0', 'llm_1', 'chatOpenAI_0')
    """
    counter = 0
    node_id = f"{base_name}_{counter}"

    while node_id in existing_ids:
        counter += 1
        node_id = f"{base_name}_{counter}"

    return node_id


def validate_connection_types(
    source_types: List[str], target_types: List[str]
) -> bool:
    """Check if connection is valid based on type compatibility.

    WHY: Implements Flowise's isValidConnection logic from genericHelper.js
    Connections are valid if source output type matches target input type.

    Args:
        source_types: List of output types from source node
        target_types: List of input types accepted by target node

    Returns:
        bool: True if types are compatible
    """
    # Check if any source type matches any target type
    return any(target_type in source_types for target_type in target_types)


# Example usage
if __name__ == "__main__":
    # Create a simple flow graph
    graph = FlowGraph()

    # Add nodes
    graph.add_node("start")
    graph.add_node("llm_1")
    graph.add_node("llm_2")
    graph.add_node("condition")
    graph.add_node("end")

    # Add edges
    print("Adding valid edges:")
    print(f"  start → llm_1: {graph.add_edge('start', 'llm_1')}")
    print(f"  llm_1 → condition: {graph.add_edge('llm_1', 'condition')}")
    print(f"  condition → llm_2: {graph.add_edge('condition', 'llm_2')}")
    print(f"  llm_2 → end: {graph.add_edge('llm_2', 'end')}")

    # Try to add a cycle (should fail)
    print("\nAttempting to add cycle:")
    print(f"  end → llm_1: {graph.add_edge('end', 'llm_1')}")  # Should print False

    # Try self-connection (should fail)
    print(f"  llm_1 → llm_1: {graph.add_edge('llm_1', 'llm_1')}")  # Should print False

    # Get starting nodes
    print(f"\nStarting nodes: {graph.get_starting_nodes()}")

    # Get topological sort
    topo_order = graph.topological_sort()
    print(f"Topological order: {topo_order}")

    # Get node levels
    print("\nNode levels:")
    for node_id in graph.nodes:
        level = graph.get_node_level(node_id)
        print(f"  {node_id}: Level {level}")

    # Test unique ID generation
    print("\nGenerating unique IDs:")
    existing = {"llm_0", "llm_1", "chatOpenAI_0"}
    print(f"  Existing: {existing}")
    print(f"  New llm ID: {generate_unique_node_id('llm', existing)}")
    print(f"  New chatOpenAI ID: {generate_unique_node_id('chatOpenAI', existing)}")

    # Export graph
    print("\nGraph structure:")
    import json
    print(json.dumps(graph.to_dict(), indent=2))
