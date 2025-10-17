#!/usr/bin/env python3
"""
Create example chatflows using node templates and Flowise connection patterns.

WHY: Demonstrates how to programmatically create valid chatflows using:
- Node templates from node_templates/ directory
- Connection logic from Flowise
- Graph utilities for validation
- Layout algorithms for positioning
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from copy import deepcopy

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fluent_mind_mcp.utils.graph import (
    FlowGraph,
    generate_unique_node_id,
    build_graph_from_flowdata,
)
from fluent_mind_mcp.utils.layout import apply_hierarchical_layout


class FlowBuilder:
    """Build chatflows using node templates and Flowise patterns."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates = self._load_templates()
        self.used_ids = set()

    def _load_templates(self) -> Dict[str, Dict]:
        """Load all node templates from directory."""
        templates = {}
        for template_file in self.templates_dir.glob("*.json"):
            # Skip INDEX.json as it's not a node template
            if template_file.stem == "INDEX":
                continue

            try:
                with open(template_file) as f:
                    data = json.load(f)

                    # Extract node data from template structure
                    if "node" in data:
                        node_template = data["node"]
                        # Use the filename (without .json) as the key
                        name = template_file.stem
                        templates[name] = node_template
                        print(f"✅ Loaded template: {name}")
                    else:
                        print(f"⚠️  Template {template_file.name} missing 'node' field")
            except Exception as e:
                print(f"⚠️  Failed to load {template_file.name}: {e}")
        return templates

    def create_node_from_template(
        self, template_name: str, custom_inputs: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a node instance from a template.

        WHY: Follows Flowise's initNode pattern - creates a complete node
        with unique ID, proper structure, and merged inputs.
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        # Template is already a ReactFlow node structure
        node = deepcopy(self.templates[template_name])

        # Generate unique ID following Flowise pattern: {name}_{counter}
        base_name = node["data"]["name"]
        node_id = generate_unique_node_id(base_name, self.used_ids)
        self.used_ids.add(node_id)

        # Update node ID
        node["id"] = node_id
        node["data"]["id"] = node_id

        # Update IDs in inputParams
        if "inputParams" in node["data"]:
            for param in node["data"]["inputParams"]:
                if "id" in param:
                    # Replace the old ID with new node_id
                    old_id_parts = param["id"].split("-")
                    if len(old_id_parts) >= 3:
                        param["id"] = f"{node_id}-{'-'.join(old_id_parts[1:])}"

        # Update IDs in inputAnchors
        if "inputAnchors" in node["data"]:
            for anchor in node["data"]["inputAnchors"]:
                if "id" in anchor:
                    old_id_parts = anchor["id"].split("-")
                    if len(old_id_parts) >= 3:
                        anchor["id"] = f"{node_id}-{'-'.join(old_id_parts[1:])}"

        # Update IDs in outputAnchors
        if "outputAnchors" in node["data"]:
            for anchor in node["data"]["outputAnchors"]:
                if "id" in anchor:
                    old_id_parts = anchor["id"].split("-")
                    if len(old_id_parts) >= 3:
                        anchor["id"] = f"{node_id}-{'-'.join(old_id_parts[1:])}"

        # Merge custom inputs with template defaults
        if custom_inputs and "inputs" in node["data"]:
            node["data"]["inputs"].update(custom_inputs)

        # Reset position (will be set by layout algorithm)
        node["position"] = {"x": 0, "y": 0}
        node["positionAbsolute"] = {"x": 0, "y": 0}
        node["selected"] = False
        node["dragging"] = False

        return node

    def find_compatible_anchor(
        self,
        source_output_types: str,
        target_input_anchors: List[Dict]
    ) -> int:
        """Find compatible input anchor based on type matching.

        WHY: Different input anchors expect different types (e.g., model vs memory).
             We match the source output type with compatible input anchor type.

        Args:
            source_output_types: Pipe-separated types (e.g., "ChatOpenAI|BaseChatModel")
            target_input_anchors: List of input anchor definitions

        Returns:
            Index of the compatible anchor, or 0 as fallback
        """
        # Parse source types
        source_types = {t.strip() for t in source_output_types.split('|')}

        # Check each target anchor for compatibility
        for i, anchor in enumerate(target_input_anchors):
            anchor_type = anchor.get('type', '')
            target_types = {t.strip() for t in anchor_type.split('|')}

            # Check if any source type matches any target type
            if source_types & target_types:
                return i

        # Fallback to first anchor
        return 0

    def create_edge(
        self,
        source_node: Dict,
        target_node: Dict,
        source_anchor_index: int = 0,
        target_anchor_index: int = None,
    ) -> Dict[str, Any]:
        """Create an edge between two nodes.

        WHY: Follows Flowise's edge creation pattern with proper handle IDs.
             Automatically finds compatible anchor if target_anchor_index not specified.
        """
        source_id = source_node["id"]
        target_id = target_node["id"]

        # Get anchor IDs from nodes
        source_anchors = source_node["data"].get("outputAnchors", [])
        target_anchors = target_node["data"].get("inputAnchors", [])

        # Auto-detect target anchor if not specified
        if target_anchor_index is None and source_anchors and target_anchors:
            source_anchor = source_anchors[source_anchor_index]
            source_types = source_anchor.get('type', '')
            target_anchor_index = self.find_compatible_anchor(source_types, target_anchors)

        # Use 0 as fallback if still not determined
        if target_anchor_index is None:
            target_anchor_index = 0

        if not source_anchors:
            # Fallback: use node ID as handle
            source_handle = f"{source_id}-output-{source_anchor_index}"
        else:
            source_anchor = source_anchors[source_anchor_index]
            source_handle = source_anchor.get("id", f"{source_id}-output-0")

        if not target_anchors:
            # Fallback: use node ID as handle
            target_handle = f"{target_id}-input-{target_anchor_index}"
        else:
            target_anchor = target_anchors[target_anchor_index]
            target_handle = target_anchor.get("id", f"{target_id}-input-0")

        edge = {
            "id": f"{source_id}-{source_handle}-{target_id}-{target_handle}",
            "source": source_id,
            "target": target_id,
            "sourceHandle": source_handle,
            "targetHandle": target_handle,
            "type": "buttonedge",
            "data": {"label": ""},
        }

        return edge

    def build_simple_chat_flow(self) -> Dict[str, Any]:
        """Build a simple chatbot flow: ChatOpenAI → ConversationChain.

        WHY: Demonstrates basic linear flow pattern.
        """
        print("\n🔨 Building Simple Chat Flow...")

        # Create nodes
        llm_node = self.create_node_from_template(
            "chatOpenAI", {"modelName": "gpt-4o-mini", "temperature": 0.7}
        )

        chain_node = self.create_node_from_template("conversationChain")

        nodes = [llm_node, chain_node]

        # Create edge
        edge = self.create_edge(llm_node, chain_node)
        edges = [edge]

        # Validate with graph
        graph = build_graph_from_flowdata(nodes, edges)
        if graph.detect_all_cycles():
            raise ValueError("Flow contains cycles!")

        # Apply layout
        nodes = apply_hierarchical_layout(nodes, edges)

        return {"nodes": nodes, "edges": edges, "viewport": {"x": 0, "y": 0, "zoom": 1}}

    def build_chat_with_memory(self) -> Dict[str, Any]:
        """Build: ChatOpenAI + BufferMemory → ConversationChain.

        WHY: Demonstrates multiple inputs to a single node with automatic type matching.
        """
        print("\n🔨 Building Chat with Memory Flow...")

        # Create nodes
        llm_node = self.create_node_from_template(
            "chatOpenAI", {"modelName": "gpt-4o-mini"}
        )

        memory_node = self.create_node_from_template("bufferMemory")

        chain_node = self.create_node_from_template("conversationChain")

        nodes = [llm_node, memory_node, chain_node]

        # Create edges (automatic type matching finds correct anchors)
        edge1 = self.create_edge(llm_node, chain_node)
        edge2 = self.create_edge(memory_node, chain_node)

        edges = [edge1, edge2]

        # Validate
        graph = build_graph_from_flowdata(nodes, edges)
        cycles = graph.detect_all_cycles()
        if cycles:
            raise ValueError(f"Flow contains cycles: {cycles}")

        topo_order = graph.topological_sort()
        print(f"  ✅ Execution order: {topo_order}")

        # Apply layout
        nodes = apply_hierarchical_layout(nodes, edges)

        return {"nodes": nodes, "edges": edges, "viewport": {"x": 0, "y": 0, "zoom": 1}}

    def build_rag_flow(self) -> Dict[str, Any]:
        """Build RAG flow: ChatOpenAI + DocumentStore → ConversationalRetrievalQAChain.

        WHY: Demonstrates retrieval-augmented generation pattern.
        """
        print("\n🔨 Building RAG Flow...")

        # Create nodes
        llm_node = self.create_node_from_template(
            "chatOpenAI", {"modelName": "gpt-4o-mini"}
        )

        doc_store_node = self.create_node_from_template(
            "documentStore", {"storeId": "my-documents"}
        )

        retrieval_chain_node = self.create_node_from_template(
            "conversationalRetrievalQAChain"
        )

        nodes = [llm_node, doc_store_node, retrieval_chain_node]

        # Create edges
        edge1 = self.create_edge(llm_node, retrieval_chain_node)
        edge2 = self.create_edge(doc_store_node, retrieval_chain_node)

        edges = [edge1, edge2]

        # Validate
        graph = build_graph_from_flowdata(nodes, edges)
        if graph.detect_all_cycles():
            raise ValueError("Flow contains cycles!")

        # Apply layout
        nodes = apply_hierarchical_layout(nodes, edges)

        return {"nodes": nodes, "edges": edges, "viewport": {"x": 0, "y": 0, "zoom": 1}}

    def build_agent_flow(self) -> Dict[str, Any]:
        """Build agent flow with tools: ChatOpenAI + Tools → AgentFlow.

        WHY: Demonstrates agent pattern with multiple tools.
        """
        print("\n🔨 Building Agent Flow...")

        # Create nodes
        llm_node = self.create_node_from_template(
            "chatOpenAI", {"modelName": "gpt-4o-mini"}
        )

        # Add some tool nodes if available
        tool_nodes = []
        if "requestsGet" in self.templates:
            tool_node = self.create_node_from_template("requestsGet")
            tool_nodes.append(tool_node)

        if "currentDateTime" in self.templates:
            datetime_node = self.create_node_from_template("currentDateTime")
            tool_nodes.append(datetime_node)

        # Agent node
        if "agentAgentflow" in self.templates:
            agent_node = self.create_node_from_template("agentAgentflow")
        else:
            # Fallback to conversation chain
            agent_node = self.create_node_from_template("conversationChain")

        nodes = [llm_node] + tool_nodes + [agent_node]

        # Create edges
        edges = []
        edge1 = self.create_edge(llm_node, agent_node)
        edges.append(edge1)

        for tool_node in tool_nodes:
            edge = self.create_edge(tool_node, agent_node)
            edges.append(edge)

        # Validate
        graph = build_graph_from_flowdata(nodes, edges)
        if graph.detect_all_cycles():
            raise ValueError("Flow contains cycles!")

        # Apply layout
        nodes = apply_hierarchical_layout(nodes, edges, spacing_y=200)

        return {"nodes": nodes, "edges": edges, "viewport": {"x": 0, "y": 0, "zoom": 1}}


def main():
    """Create example flows and save to files."""
    # Setup paths
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "node_templates"
    output_dir = script_dir / "generated_flows"
    output_dir.mkdir(exist_ok=True)

    print(f"\n📁 Loading templates from: {templates_dir}")
    print(f"📁 Output directory: {output_dir}")

    # Create builder
    builder = FlowBuilder(templates_dir)

    print(f"\n✅ Loaded {len(builder.templates)} templates")

    # Create flows
    flows = {
        "simple_chat": builder.build_simple_chat_flow(),
        "chat_with_memory": builder.build_chat_with_memory(),
        "rag_flow": builder.build_rag_flow(),
        "agent_flow": builder.build_agent_flow(),
    }

    # Save flows
    print("\n💾 Saving flows...")
    for name, flow_data in flows.items():
        output_file = output_dir / f"{name}.json"

        # Create complete chatflow structure
        chatflow = {
            "name": name.replace("_", " ").title(),
            "deployed": False,
            "isPublic": False,
            "flowData": json.dumps(flow_data),
            "type": "CHATFLOW",
        }

        with open(output_file, "w") as f:
            json.dump(chatflow, f, indent=2)

        print(f"  ✅ {output_file.name}")
        print(f"     Nodes: {len(flow_data['nodes'])}, Edges: {len(flow_data['edges'])}")

    # Also save raw flowData for easier inspection
    print("\n💾 Saving raw flowData...")
    for name, flow_data in flows.items():
        output_file = output_dir / f"{name}_flowdata.json"
        with open(output_file, "w") as f:
            json.dump(flow_data, f, indent=2)
        print(f"  ✅ {output_file.name}")

    print(
        f"\n✨ Successfully created {len(flows)} chatflows in {output_dir}/"
    )
    print("\n📖 Next steps:")
    print("  1. Review the generated flows in generated_flows/")
    print("  2. Use create_chatflow MCP tool to upload them to Flowise")
    print("  3. Or copy the JSON and import via Flowise UI")


if __name__ == "__main__":
    main()
