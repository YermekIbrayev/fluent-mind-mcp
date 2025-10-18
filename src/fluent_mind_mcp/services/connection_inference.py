"""Connection inference for automatic node chaining.

Implements intelligent connection logic for chatflow nodes based on
type compatibility and topological ordering.

WHY: Separates connection inference algorithm from BuildFlowService
     to maintain file size limits and single responsibility.
"""

from typing import Optional

from fluent_mind_mcp.utils.exceptions import ConnectionInferenceError


class ConnectionInference:
    """Handles automatic connection inference between flow nodes.

    WHY: Encapsulates complex connection logic in dedicated class.
    """

    @staticmethod
    def categorize_nodes(nodes: list[dict]) -> dict[str, list[dict]]:
        """Categorize nodes by type (T038).

        WHY: Groups nodes by role (Input, Processing, Memory, Tools, Output)
             for proper connection ordering.
        """
        categories = {
            "Input": [],
            "Processing": [],
            "Memory": [],
            "Tools": [],
            "Output": []
        }

        for node in nodes:
            base_classes = node.get("base_classes", [])

            if any(cls in base_classes for cls in ["BaseLoader", "Document"]):
                categories["Input"].append(node)
            elif any(cls in base_classes for cls in ["BaseChatModel", "BaseLanguageModel", "Embeddings"]):
                categories["Processing"].append(node)
            elif "BaseMemory" in base_classes:
                categories["Memory"].append(node)
            elif any(cls in base_classes for cls in ["Tool", "BaseTool"]):
                categories["Tools"].append(node)
            elif any(cls in base_classes for cls in ["BaseChain", "BaseAgent", "BaseRetriever", "VectorStore"]):
                categories["Output"].append(node)
            else:
                categories["Processing"].append(node)

        return categories

    @staticmethod
    def topological_sort(categorized_nodes: dict) -> list[dict]:
        """Sort nodes by category order (T039).

        WHY: Ensures proper execution flow: Input → Tools → Processing → Memory → Output
        """
        ordered = []
        for category in ["Input", "Tools", "Processing", "Memory", "Output"]:
            ordered.extend(categorized_nodes.get(category, []))
        return ordered

    @staticmethod
    def match_base_classes(nodes: list[dict]) -> list[tuple[dict, dict]]:
        """Match compatible node pairs (T040).

        WHY: Creates sequential connections between adjacent nodes.
        """
        pairs = []
        for i, node1 in enumerate(nodes[:-1]):
            node2 = nodes[i + 1]
            pairs.append((node1, node2))
        return pairs

    @staticmethod
    def _has_cycle(edge_map: dict, start: str, current: str, visited: set, rec_stack: set) -> bool:
        """Detect cycles in directed graph using Depth-First Search (DFS).

        WHY: Proper cycle detection requires traversing all paths from a node.
        The algorithm uses two sets:
        - visited: Nodes we've seen (prevents re-processing)
        - rec_stack: Nodes in current DFS path (detects back edges)

        A cycle exists if we reach a node that's already in our current path
        (rec_stack), indicating we've looped back.

        Args:
            edge_map: Adjacency list {node_id: [target_ids]}
            start: Starting node (unused but kept for API compatibility)
            current: Current node being explored
            visited: Set of all visited nodes across all DFS trees
            rec_stack: Set of nodes in current DFS recursion path

        Returns:
            True if cycle detected, False otherwise

        Algorithm:
            1. Mark current node as visited and in recursion stack
            2. For each neighbor:
               - If unvisited: recursively check that subtree
               - If in rec_stack: found cycle (back edge)
            3. Remove from rec_stack before returning (backtrack)

        WHY DFS: O(V+E) time complexity, detects all cycles including complex
        multi-node cycles like 1→2→3→1, not just self-loops.
        """
        # WHY: Track visited nodes to avoid re-processing
        visited.add(current)
        # WHY: Track current path to detect back edges (cycles)
        rec_stack.add(current)

        # WHY: Explore all outgoing edges from current node
        for neighbor in edge_map.get(current, []):
            if neighbor not in visited:
                # WHY: Recursively check subtree for cycles
                if ConnectionInference._has_cycle(edge_map, start, neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                # WHY: Back edge detected - neighbor is in our current path
                # This means we've found a cycle (e.g., 1→2→3→1)
                return True

        # WHY: Backtrack - remove from recursion stack as we leave this node
        # Node stays in visited (won't re-process) but not in path anymore
        rec_stack.remove(current)
        return False

    @staticmethod
    def generate_edges(
        node_pairs: list[tuple],
        all_nodes: Optional[list] = None
    ) -> list[dict]:
        """Generate edges from node pairs (T041).

        WHY: Creates edge objects with validation for circular dependencies
             and required inputs.
        """
        edges = []
        edge_map = {}

        for node1, node2 in node_pairs:
            source_id = node1["id"]
            target_id = node2["id"]

            edge = {
                "id": f"edge_{len(edges)}",
                "source": source_id,
                "target": target_id,
                "sourceHandle": source_id,
                "targetHandle": target_id
            }
            edges.append(edge)

            if source_id not in edge_map:
                edge_map[source_id] = []
            edge_map[source_id].append(target_id)

        # WHY: Detect circular dependencies before returning
        # Must check AFTER building all edges to see complete graph structure
        visited = set()
        for node_id in edge_map.keys():
            if node_id not in visited:
                # WHY: Start DFS from each unvisited node to cover disconnected components
                if ConnectionInference._has_cycle(edge_map, node_id, node_id, visited, set()):
                    raise ConnectionInferenceError(
                        message="Circular dependency detected in flow"
                    )

        # WHY: Validate required inputs are satisfied
        # Prevents creating non-functional flows that will fail at runtime
        if all_nodes:
            for node in all_nodes:
                required_inputs = node.get("required_inputs", [])
                if required_inputs:
                    node_id = node["id"]
                    has_input = any(e["target"] == node_id for e in edges)

                    # WHY: Even single-node flows need inputs if marked as required
                    # E.g., Agent needs ChatModel - can't function standalone
                    if not has_input:
                        raise ConnectionInferenceError(
                            message=f"Node {node.get('name', node_id)} missing required inputs"
                        )

        return edges

    @classmethod
    def infer_connections(cls, nodes: list[dict]) -> list[dict]:
        """Infer connections between nodes (T042).

        WHY: Main entry point combining all inference steps.
        """
        if not nodes:
            return []

        categorized = cls.categorize_nodes(nodes)
        sorted_nodes = cls.topological_sort(categorized)
        node_pairs = cls.match_base_classes(sorted_nodes)
        edges = cls.generate_edges(node_pairs, nodes)

        return edges
