"""Helper utilities for building chatflows from node templates.

WHY: Simplifies creating Flowise chatflows programmatically using extracted
node templates while following constitution principles.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def update_node_id(node: Dict[str, Any], new_id: str) -> Dict[str, Any]:
    """Update node ID and all related anchor IDs.

    WHY: When changing a node's ID, all anchor IDs must also be updated,
    otherwise edge handles won't match and nodes won't connect.

    Args:
        node: Node dictionary to update
        new_id: New node ID

    Returns:
        Updated node (modifies in place, but also returns for chaining)
    """
    old_id = node['id']
    node['id'] = new_id

    # CRITICAL: Also update data.id (Flowise requires this to match node.id)
    node['data']['id'] = new_id

    # Update output anchors
    for anchor in node['data'].get('outputAnchors', []):
        if 'id' in anchor:
            anchor['id'] = anchor['id'].replace(old_id, new_id, 1)
        # Handle options-type anchors (like cheerioWebScraper, memoryVectorStore)
        if anchor.get('type') == 'options' and 'options' in anchor:
            for option in anchor['options']:
                if 'id' in option:
                    option['id'] = option['id'].replace(old_id, new_id, 1)

    # Update input anchors
    for anchor in node['data'].get('inputAnchors', []):
        if 'id' in anchor:
            anchor['id'] = anchor['id'].replace(old_id, new_id, 1)
        # Handle options-type anchors
        if anchor.get('type') == 'options' and 'options' in anchor:
            for option in anchor['options']:
                if 'id' in option:
                    option['id'] = option['id'].replace(old_id, new_id, 1)

    # Update input params
    for param in node['data'].get('inputParams', []):
        if 'id' in param:
            param['id'] = param['id'].replace(old_id, new_id, 1)

    return node


def get_output_handle(node: Dict[str, Any], anchor_name: str = None) -> str:
    """Get the output handle ID for a node.

    Args:
        node: Node dictionary
        anchor_name: Optional anchor name to find. If None, returns first output.

    Returns:
        Output anchor ID for use in edge sourceHandle

    Raises:
        ValueError: If node has no output anchors or anchor_name not found
    """
    output_anchors = node['data'].get('outputAnchors', [])
    if not output_anchors:
        raise ValueError(f"Node {node['id']} has no output anchors")

    if anchor_name:
        for anchor in output_anchors:
            # Check simple anchors
            if anchor.get('name') == anchor_name:
                return anchor['id']
            # Check options-type anchors (e.g., cheerioWebScraper, memoryVectorStore)
            if anchor.get('type') == 'options' and 'options' in anchor:
                for option in anchor['options']:
                    if option.get('name') == anchor_name:
                        return option['id']
        raise ValueError(f"No output anchor named '{anchor_name}' in node {node['id']}")

    # Return first output anchor
    # For options-type, return the default or first option
    first_anchor = output_anchors[0]
    if first_anchor.get('type') == 'options' and 'options' in first_anchor:
        # Return default option or first option
        default_name = first_anchor.get('default')
        if default_name:
            for option in first_anchor['options']:
                if option.get('name') == default_name:
                    return option['id']
        # Return first option
        return first_anchor['options'][0]['id']

    return first_anchor['id']


def get_input_handle(node: Dict[str, Any], anchor_name: str) -> str:
    """Get the input handle ID for a node.

    Args:
        node: Node dictionary
        anchor_name: Name of input anchor

    Returns:
        Input anchor ID for use in edge targetHandle

    Raises:
        ValueError: If anchor_name not found
    """
    input_anchors = node['data'].get('inputAnchors', [])
    for anchor in input_anchors:
        if anchor.get('name') == anchor_name:
            return anchor['id']
    raise ValueError(f"No input anchor named '{anchor_name}' in node {node['id']}")


class NodeBuilder:
    """Build Flowise chatflows from node templates.

    WHY: Provides a high-level API for creating chatflows programmatically,
    handling node ID updates and edge connections automatically.

    Example:
        >>> builder = NodeBuilder()
        >>> llm = builder.create_node('chatOpenAI', 'llm1', x=100, y=200,
        ...                           modelName='gpt-4o-mini')
        >>> memory = builder.create_node('bufferWindowMemory', 'mem1', x=100, y=400)
        >>> chain = builder.create_node('conversationChain', 'chain1', x=400, y=300)
        >>> # Connect with proper handles
        >>> builder.connect_via_reference('llm1', 'chain1', 'model')
        >>> builder.connect_via_reference('mem1', 'chain1', 'memory')
        >>> flow_data = builder.build()

    Note:
        All node IDs and anchor IDs are automatically updated by create_node(),
        and connect_via_reference() creates edges with correct handles.
    """

    def __init__(self, templates_dir: str = "node_templates"):
        """Initialize node builder.

        Args:
            templates_dir: Directory containing node templates
        """
        self.templates_dir = Path(templates_dir)
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self.edge_counter = 0

    def create_node(
        self,
        template_name: str,
        node_id: str,
        x: int = 100,
        y: int = 100,
        **inputs
    ) -> Dict[str, Any]:
        """Create a node from template.

        Args:
            template_name: Template filename without .json extension
            node_id: Unique identifier for this node instance
            x: X position in canvas
            y: Y position in canvas
            **inputs: Input values to customize

        Returns:
            Node configuration dict

        Raises:
            FileNotFoundError: If template not found
            KeyError: If input key doesn't exist
        """
        # Load template
        template_path = self.templates_dir / f"{template_name}.json"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r') as f:
            template = json.load(f)

        # Get node and customize
        node = json.loads(json.dumps(template['node']))  # Deep copy

        # Update node ID and all anchor IDs
        update_node_id(node, node_id)

        # Set position
        node['position'] = {"x": x, "y": y}

        # Set inputs
        for key, value in inputs.items():
            if key not in node['data']['inputs']:
                raise KeyError(f"Input '{key}' not found in {template_name}")
            node['data']['inputs'][key] = value

        # Add to nodes list
        self.nodes.append(node)

        return node

    def connect(
        self,
        source_id: str,
        target_id: str,
        source_handle: Optional[str] = None,
        target_handle: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an edge between two nodes.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            source_handle: Optional source output handle
            target_handle: Optional target input handle

        Returns:
            Edge configuration dict

        Note:
            Flowise requires edges to have:
            - type: "buttonedge"
            - id: "{source}-{sourceHandle}-{target}-{targetHandle}"
        """
        # Build edge ID in Flowise format
        if source_handle and target_handle:
            edge_id = f"{source_id}-{source_handle}-{target_id}-{target_handle}"
        else:
            edge_id = f"{source_id}-{target_id}-{self.edge_counter}"
            self.edge_counter += 1

        edge = {
            "source": source_id,
            "sourceHandle": source_handle,
            "target": target_id,
            "targetHandle": target_handle,
            "type": "buttonedge",
            "id": edge_id
        }

        self.edges.append(edge)
        return edge

    def connect_with_handles(
        self,
        source_id: str,
        target_id: str,
        source_anchor: str = None,
        target_anchor: str = None
    ) -> Dict[str, Any]:
        """Create an edge with automatically determined handles.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            source_anchor: Source anchor name (uses first if None)
            target_anchor: Target anchor name (required)

        Returns:
            Edge configuration dict
        """
        # Find nodes
        source_node = self.get_node(source_id)
        target_node = self.get_node(target_id)

        if not source_node:
            raise ValueError(f"Source node '{source_id}' not found")
        if not target_node:
            raise ValueError(f"Target node '{target_id}' not found")

        # Get handles
        source_handle = get_output_handle(source_node, source_anchor)
        target_handle = get_input_handle(target_node, target_anchor)

        # Create edge
        return self.connect(source_id, target_id, source_handle, target_handle)

    def connect_via_reference(
        self,
        source_id: str,
        target_id: str,
        input_key: str,
        source_anchor: str = None
    ) -> Dict[str, Any]:
        """Connect nodes via input reference with proper edge handles.

        Args:
            source_id: Source node ID
            target_id: Target node ID that will reference source
            input_key: Input key in target to set reference
            source_anchor: Source output anchor name (uses first if None)

        Returns:
            Edge configuration dict
        """
        # Find nodes
        target = self.get_node(target_id)
        if not target:
            raise ValueError(f"Target node '{target_id}' not found")

        # Set reference
        target['data']['inputs'][input_key] = f"{{{{{source_id}.data.instance}}}}"

        # Create edge with proper handles
        return self.connect_with_handles(source_id, target_id, source_anchor, input_key)

    def build(
        self,
        viewport: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Build final flowData structure.

        Args:
            viewport: Optional viewport config {x, y, zoom}

        Returns:
            Complete flowData dict ready for API
        """
        if viewport is None:
            viewport = {"x": 0, "y": 0, "zoom": 1}

        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "viewport": viewport
        }

    def clear(self) -> None:
        """Clear all nodes and edges."""
        self.nodes = []
        self.edges = []
        self.edge_counter = 0

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get node by ID.

        Args:
            node_id: Node identifier

        Returns:
            Node dict or None if not found
        """
        return next((n for n in self.nodes if n['id'] == node_id), None)

    def list_nodes(self) -> List[str]:
        """Get list of all node IDs.

        Returns:
            List of node identifiers
        """
        return [n['id'] for n in self.nodes]


# Convenience functions

def create_simple_chatbot(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.7,
    memory_size: int = 10
) -> Dict[str, Any]:
    """Create a simple chatbot flowData.

    Args:
        model_name: OpenAI model name
        temperature: Model temperature
        memory_size: Number of messages to remember

    Returns:
        Complete flowData dict
    """
    builder = NodeBuilder()

    # Create nodes
    builder.create_node('chatOpenAI', 'llm', 100, 200,
                        modelName=model_name,
                        temperature=temperature)

    builder.create_node('bufferWindowMemory', 'memory', 100, 400,
                        k=str(memory_size))

    builder.create_node('conversationChain', 'chain', 400, 300)

    # Connect via references
    builder.connect_via_reference('llm', 'chain', 'model')
    builder.connect_via_reference('memory', 'chain', 'memory')

    return builder.build()


def create_rag_chatbot(
    model_name: str = "gpt-4o-mini",
    embedding_model: str = "text-embedding-3-small",
    top_k: int = 5
) -> Dict[str, Any]:
    """Create a RAG (Retrieval-Augmented Generation) chatbot.

    Args:
        model_name: OpenAI model name
        embedding_model: OpenAI embedding model
        top_k: Number of documents to retrieve

    Returns:
        Complete flowData dict
    """
    builder = NodeBuilder()

    # Create nodes
    builder.create_node('openAIEmbeddings', 'embeddings', 100, 100,
                        modelName=embedding_model)

    builder.create_node('faiss', 'vectorstore', 100, 300,
                        topK=str(top_k))

    builder.create_node('chatOpenAI', 'llm', 400, 100,
                        modelName=model_name)

    builder.create_node('conversationalRetrievalQAChain', 'qa_chain', 700, 200)

    # Connect
    builder.connect_via_reference('embeddings', 'vectorstore', 'embeddings')
    builder.connect_via_reference('llm', 'qa_chain', 'model')
    builder.connect_via_reference('vectorstore', 'qa_chain', 'vectorStore')

    return builder.build()


if __name__ == "__main__":
    # Example usage
    print("=== Creating Simple Chatbot ===")
    flow_data = create_simple_chatbot()
    print(f"Nodes: {len(flow_data['nodes'])}")
    print(f"Edges: {len(flow_data['edges'])}")
    print(f"\nFlowData ready to POST to Flowise API")
