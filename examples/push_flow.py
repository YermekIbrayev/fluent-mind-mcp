#!/usr/bin/env python3
"""
Reusable script to push chatflows to Flowise with automatic 2-phase deployment.

WHY: Handles all complexity of creating and fixing node references automatically.
     You just describe what you want, and the script does the rest.

USAGE:
    python3 push_flow.py --config my_flow.yaml
    python3 push_flow.py --name "My Flow" --nodes llm,memory,chain
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fluent_mind_mcp.services.chatflow_service import ChatflowService
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.models import FlowiseConfig
from fluent_mind_mcp.models.chatflow import ChatflowType
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.utils.graph import build_graph_from_flowdata, generate_unique_node_id
from fluent_mind_mcp.utils.layout import apply_hierarchical_layout

# Import FlowBuilder
sys.path.insert(0, str(Path(__file__).parent))
from create_example_flows import FlowBuilder


class FlowPusher:
    """Push chatflows to Flowise with automatic 2-phase deployment."""

    def __init__(self):
        """Initialize with Flowise connection."""
        self.config = FlowiseConfig.from_env()
        self.client = FlowiseClient(self.config)
        self.logger = OperationLogger(name="flow_pusher", level=self.config.log_level)
        self.service = ChatflowService(self.client, self.logger)

        # Initialize template builder
        templates_dir = Path(__file__).parent / "node_templates"
        self.builder = FlowBuilder(templates_dir)
        print(f"✅ Loaded {len(self.builder.templates)} node templates")

    async def close(self):
        """Close connections."""
        await self.client.close()

    def build_flow_from_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Build flow from specification.

        Args:
            spec: Flow specification with format:
                {
                    "nodes": [
                        {"template": "chatOpenAI", "inputs": {"modelName": "gpt-4o-mini"}},
                        {"template": "bufferMemory", "inputs": {}},
                        {"template": "conversationChain", "inputs": {}}
                    ],
                    "edges": [
                        {"from": 0, "to": 2},  # chatOpenAI -> conversationChain
                        {"from": 1, "to": 2}   # bufferMemory -> conversationChain
                    ]
                }

        Returns:
            FlowData dict with nodes and edges
        """
        # Create nodes
        nodes = []
        for node_spec in spec["nodes"]:
            node = self.builder.create_node_from_template(
                node_spec["template"],
                node_spec.get("inputs", {})
            )
            nodes.append(node)

        # Create edges
        edges = []
        for edge_spec in spec["edges"]:
            source_node = nodes[edge_spec["from"]]
            target_node = nodes[edge_spec["to"]]

            # Use automatic type matching if target_anchor not specified
            edge = self.builder.create_edge(
                source_node,
                target_node,
                source_anchor_index=edge_spec.get("source_anchor", 0),
                target_anchor_index=edge_spec.get("target_anchor")  # None = auto-detect
            )
            edges.append(edge)

        # Validate (no cycles)
        graph = build_graph_from_flowdata(nodes, edges)
        if graph.detect_all_cycles():
            raise ValueError("Flow contains cycles!")

        # Apply layout
        nodes = apply_hierarchical_layout(nodes, edges)

        return {
            "nodes": nodes,
            "edges": edges,
            "viewport": {"x": 0, "y": 0, "zoom": 1}
        }

    def fix_node_references(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix variable references in node inputs based on edges.

        WHY: Node templates have hardcoded references. We update them to
             reference the actual nodes connected via edges.

        Args:
            flow_data: FlowData dict with nodes and edges

        Returns:
            Updated flow_data with fixed references
        """
        # Build edge mapping: {target_node: {input_name: source_node}}
        edge_mapping = {}

        for edge in flow_data['edges']:
            source_id = edge['source']
            target_id = edge['target']
            target_handle = edge['targetHandle']

            # Extract input name from targetHandle
            # Format: "conversationChain_1-input-model-BaseChatModel"
            parts = target_handle.split('-input-')
            if len(parts) == 2:
                input_name = parts[1].rsplit('-', 1)[0]

                if target_id not in edge_mapping:
                    edge_mapping[target_id] = {}
                edge_mapping[target_id][input_name] = source_id

        # Get all node IDs
        node_ids = {node['id'] for node in flow_data['nodes']}

        # Update node inputs
        for node in flow_data['nodes']:
            node_id = node['id']

            if 'inputs' in node['data']:
                inputs_to_remove = []
                for key, value in node['data']['inputs'].items():
                    # If it's a reference {{something.data.instance}}
                    if isinstance(value, str) and '{{' in value and '.data.instance' in value:
                        # Check if we have an edge connection
                        if node_id in edge_mapping and key in edge_mapping[node_id]:
                            correct_source = edge_mapping[node_id][key]
                            correct_ref = f"{{{{{correct_source}.data.instance}}}}"
                            node['data']['inputs'][key] = correct_ref
                        else:
                            # No edge = optional input, remove it entirely
                            inputs_to_remove.append(key)

                # Remove unused optional inputs
                for key in inputs_to_remove:
                    del node['data']['inputs'][key]

        return flow_data

    async def push(
        self,
        name: str,
        spec: Dict[str, Any],
        deployed: bool = False
    ) -> str:
        """Push chatflow to Flowise with 2-phase deployment.

        Args:
            name: Chatflow name
            spec: Flow specification (see build_flow_from_spec)
            deployed: Whether to deploy immediately

        Returns:
            Created chatflow ID
        """
        print(f"\n🔨 Building flow: {name}")

        # Build flow from spec
        flow_data = self.build_flow_from_spec(spec)
        print(f"   ✅ Built: {len(flow_data['nodes'])} nodes, {len(flow_data['edges'])} edges")

        # Phase 1: Create chatflow
        print(f"\n📤 Phase 1: Creating chatflow...")
        flow_data_str = json.dumps(flow_data)

        chatflow = await self.service.create_chatflow(
            name=name,
            flow_data=flow_data_str,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        print(f"   ✅ Created: {chatflow.id}")

        # Phase 2: Fix references
        print(f"\n🔧 Phase 2: Fixing node references...")

        # Get current chatflow
        current = await self.service.get_chatflow(chatflow.id)
        current_flow = json.loads(current.flow_data)

        # Fix references
        fixed_flow = self.fix_node_references(current_flow)

        # Count fixes
        fixes = 0
        for node in fixed_flow['nodes']:
            if 'inputs' in node['data']:
                for key, value in node['data']['inputs'].items():
                    if isinstance(value, str) and '{{' in value:
                        fixes += 1

        print(f"   ✅ Fixed {fixes} node references")

        # Update chatflow
        updated = await self.service.update_chatflow(
            chatflow_id=chatflow.id,
            flow_data=json.dumps(fixed_flow)
        )

        # Deploy if requested
        if deployed:
            print(f"\n🚀 Deploying chatflow...")
            await self.service.deploy_chatflow(chatflow.id, deployed=True)
            print(f"   ✅ Deployed")

        print(f"\n✅ Success! Chatflow ID: {chatflow.id}")

        return chatflow.id


async def push_from_config(config_file: Path) -> str:
    """Push chatflow from YAML/JSON config file."""
    import yaml

    with open(config_file) as f:
        if config_file.suffix == '.json':
            config = json.load(f)
        else:
            config = yaml.safe_load(f)

    pusher = FlowPusher()
    try:
        return await pusher.push(
            name=config["name"],
            spec=config["spec"],
            deployed=config.get("deployed", False)
        )
    finally:
        await pusher.close()


async def push_from_args(args) -> str:
    """Push chatflow from command line arguments."""
    # Build simple spec from args
    spec = {
        "nodes": [],
        "edges": []
    }

    # Parse nodes (e.g., "llm:chatOpenAI,memory:bufferMemory,chain:conversationChain")
    if args.nodes:
        for i, node_def in enumerate(args.nodes.split(',')):
            if ':' in node_def:
                alias, template = node_def.split(':', 1)
            else:
                alias = node_def
                template = node_def

            spec["nodes"].append({
                "template": template,
                "inputs": {}
            })

    # Parse edges (e.g., "0-2,1-2" means node 0->2 and node 1->2)
    if args.edges:
        for edge_def in args.edges.split(','):
            from_idx, to_idx = edge_def.split('-')
            spec["edges"].append({
                "from": int(from_idx),
                "to": int(to_idx)
            })

    pusher = FlowPusher()
    try:
        return await pusher.push(
            name=args.name,
            spec=spec,
            deployed=args.deploy
        )
    finally:
        await pusher.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Push chatflows to Flowise with automatic 2-phase deployment"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Config file (YAML or JSON) with flow specification"
    )

    parser.add_argument(
        "--name",
        type=str,
        help="Chatflow name (for CLI mode)"
    )

    parser.add_argument(
        "--nodes",
        type=str,
        help="Comma-separated node templates (e.g., 'chatOpenAI,bufferMemory,conversationChain')"
    )

    parser.add_argument(
        "--edges",
        type=str,
        help="Comma-separated edges (e.g., '0-2,1-2' means node 0->2 and 1->2)"
    )

    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Deploy chatflow immediately after creation"
    )

    args = parser.parse_args()

    # Validate args
    if args.config:
        if not args.config.exists():
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
        chatflow_id = asyncio.run(push_from_config(args.config))
    elif args.name and args.nodes:
        chatflow_id = asyncio.run(push_from_args(args))
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # From config file")
        print("  python3 push_flow.py --config my_flow.yaml")
        print()
        print("  # From command line")
        print("  python3 push_flow.py --name 'Simple Chat' --nodes 'chatOpenAI,conversationChain' --edges '0-1'")
        print()
        print("  # Chat with memory")
        print("  python3 push_flow.py --name 'Chat With Memory' --nodes 'chatOpenAI,bufferMemory,conversationChain' --edges '0-2,1-2'")
        sys.exit(1)

    print(f"\n🎉 Done! Chatflow ID: {chatflow_id}")


if __name__ == "__main__":
    main()
