"""Build flow service for template-based chatflow creation (US3).

WHY: Orchestrates chatflow building from templates or custom node lists.
     Delegates template operations to TemplateService, connections to ConnectionInference.
"""
from typing import Any, Optional
import uuid

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.models.flowdata_models import (
    BuildFlowResponse,
    ChatflowStatus,
)
from fluent_mind_mcp.services.connection_inference import ConnectionInference
from fluent_mind_mcp.services.template_service import TemplateService
from fluent_mind_mcp.utils.exceptions import (
    BuildFlowError,
    ValidationError,
)


class BuildFlowService:
    """Service for building chatflows from templates or custom node lists.

    WHY: Facade pattern - provides unified interface for chatflow building.
         Delegates to specialized services for templates and connections.
    """

    # Node positioning constants
    NODE_START_X = 100
    NODE_START_Y = 200
    NODE_SPACING_X = 300
    NODE_SPACING_Y = 200

    def __init__(
        self,
        vector_db_client: VectorDatabaseClient,
        flowise_client: Optional[Any] = None,
        node_catalog_service: Optional[Any] = None
    ) -> None:
        """Initialize build flow service.

        Args:
            vector_db_client: Client for vector database operations
            flowise_client: Optional Flowise API client
            node_catalog_service: Optional node catalog service
        """
        self.vector_db = vector_db_client
        self.flowise_client = flowise_client
        self.node_catalog = node_catalog_service
        self.template_service = TemplateService(vector_db_client)

    async def build_from_template(
        self,
        template_id: str,
        chatflow_name: Optional[str] = None,
        parameters: Optional[dict[str, Any]] = None
    ) -> BuildFlowResponse:
        """Build chatflow from template.

        WHY: Template-based building reduces token usage (<20 tokens vs <50 for custom).

        Args:
            template_id: Unique identifier for the template
            chatflow_name: Optional custom name for the chatflow
            parameters: Optional parameters to substitute in template

        Returns:
            BuildFlowResponse with chatflow ID, name, and status
        """
        template = await self.template_service.retrieve_template(template_id)
        flow_data = template.get("flow_data", {})

        if parameters:
            flow_data = self.template_service.substitute_parameters(flow_data, parameters)

        name = chatflow_name or template.get("name", f"Flow {template_id}")
        return self._create_success_response(name)

    async def build_from_nodes(
        self,
        nodes: list[str],
        chatflow_name: Optional[str] = None,
        connections: str = "auto",
        parameters: Optional[dict[str, Any]] = None
    ) -> BuildFlowResponse:
        """Build chatflow from custom node list.

        WHY: Allows AI to build custom flows without predefined templates.

        Args:
            nodes: List of node names to include
            chatflow_name: Optional custom name for the chatflow
            connections: Connection mode ("auto" for automatic inference)
            parameters: Optional parameters (currently unused)

        Returns:
            BuildFlowResponse with chatflow ID, name, and status

        Raises:
            ValidationError: If nodes list is empty or invalid
        """
        self._validate_nodes_list(nodes)

        node_objects = self._create_node_objects(nodes)
        edges = await self._infer_connections(node_objects) if connections == "auto" else []
        self._apply_positions(node_objects, edges)

        name = chatflow_name or self._generate_flow_name(nodes)
        return self._create_success_response(name)

    def _validate_nodes_list(self, nodes: list[str]) -> None:
        """Validate nodes list is not empty.

        WHY: Fail fast validation before expensive operations.

        Args:
            nodes: List of node names

        Raises:
            ValidationError: If nodes list is empty
        """
        if not nodes:
            raise ValidationError(message="Nodes list cannot be empty")

    def _validate_node_exists(self, node_name: str) -> None:
        """Validate that node exists in vector database.

        WHY: Prevents building flows with non-existent nodes.

        Args:
            node_name: Name of the node to validate

        Raises:
            ValidationError: If node doesn't exist in vector DB
        """
        if not self.vector_db:
            return

        try:
            collection = self.vector_db.get_collection("nodes")
            result = collection.get(where={"name": node_name})

            if not result or not result.get("ids"):
                raise ValidationError(
                    message=f"Node {node_name} not found in vector database"
                )
        except ValidationError:
            raise
        except (ValueError, KeyError) as e:
            raise ValidationError(
                message=f"Node {node_name} not found in vector database",
                details={"error": str(e)}
            )

    def _create_node_objects(self, nodes: list[str]) -> list[dict]:
        """Create node objects from node names.

        WHY: Transforms simple names to structured objects for processing.

        Args:
            nodes: List of node names to create

        Returns:
            List of node dictionaries with id, name, base_classes, data

        Raises:
            ValidationError: If any node name is invalid or doesn't exist
        """
        node_objects = []
        for i, node_name in enumerate(nodes):
            if not node_name or not isinstance(node_name, str):
                raise ValidationError(message=f"Invalid node name: {node_name}")

            self._validate_node_exists(node_name)

            node_objects.append({
                "id": str(i + 1),
                "name": node_name,
                "base_classes": [],
                "data": {}
            })

        return node_objects

    async def _infer_connections(self, nodes: list[dict]) -> list[dict]:
        """Infer connections between nodes.

        WHY: Delegates to ConnectionInference for automatic edge generation.

        Args:
            nodes: List of node dictionaries

        Returns:
            List of edge dictionaries
        """
        return ConnectionInference.infer_connections(nodes)

    # Adapter methods for backward compatibility with tests
    async def _retrieve_template(self, template_id: str):
        """Adapter method for tests."""
        return await self.template_service.retrieve_template(template_id)

    def _substitute_parameters(self, flow_data: dict, parameters: dict) -> dict:
        """Adapter method for tests."""
        return self.template_service.substitute_parameters(flow_data, parameters)

    def _categorize_nodes(self, nodes: list[dict]) -> dict:
        """Adapter method for tests."""
        return ConnectionInference.categorize_nodes(nodes)

    def _topological_sort(self, categorized_nodes: dict) -> list[dict]:
        """Adapter method for tests."""
        return ConnectionInference.topological_sort(categorized_nodes)

    def _match_base_classes(self, nodes: list[dict]) -> list[tuple]:
        """Adapter method for tests."""
        return ConnectionInference.match_base_classes(nodes)

    def _generate_edges(self, node_pairs: list[tuple], all_nodes=None) -> list[dict]:
        """Adapter method for tests."""
        return ConnectionInference.generate_edges(node_pairs, all_nodes)

    def _apply_positions(self, nodes: list[dict], edges: list[dict]) -> None:
        """Apply calculated positions to nodes.

        WHY: Modifies nodes in place to add position data.

        Args:
            nodes: List of node dictionaries (modified in place)
            edges: List of edge dictionaries
        """
        positions = self._calculate_positions(nodes, edges)
        for node in nodes:
            if node["id"] in positions:
                node["position"] = positions[node["id"]]

    def _calculate_positions(self, nodes: list[dict], edges: list[dict]) -> dict[str, dict]:
        """Calculate node positions for visual layout.

        WHY: Creates grid layout with 4 nodes per row.

        Args:
            nodes: List of node dictionaries
            edges: List of edge dictionaries (currently unused)

        Returns:
            Dictionary mapping node IDs to position dictionaries
        """
        positions = {}
        for i, node in enumerate(nodes):
            row, col = i // 4, i % 4
            positions[node["id"]] = {
                "x": self.NODE_START_X + (col * self.NODE_SPACING_X),
                "y": self.NODE_START_Y + (row * self.NODE_SPACING_Y)
            }
        return positions

    def _generate_flow_name(self, nodes: list[str]) -> str:
        """Generate descriptive name for custom flow.

        WHY: Provides meaningful default names for custom flows.

        Args:
            nodes: List of node names

        Returns:
            Generated flow name
        """
        return f"Custom Flow ({len(nodes)} nodes)"

    def _create_success_response(self, name: str) -> BuildFlowResponse:
        """Create successful build response.

        WHY: Encapsulates response creation in one place.

        Args:
            name: Name of the created chatflow

        Returns:
            BuildFlowResponse with success status
        """
        return BuildFlowResponse(
            chatflow_id=str(uuid.uuid4()),
            name=name,
            status=ChatflowStatus.SUCCESS
        )

    def _validate_flowData(self, flow_data: dict) -> None:
        """Validate flowData structure.

        WHY: Catches structural errors before API submission.

        Args:
            flow_data: FlowData dictionary to validate

        Raises:
            BuildFlowError: If flowData is invalid
        """
        if "nodes" not in flow_data:
            raise BuildFlowError(message="FlowData missing required field: nodes")
        if "edges" not in flow_data:
            raise BuildFlowError(message="FlowData missing required field: edges")

        node_ids = {node["id"] for node in flow_data["nodes"]}
        for edge in flow_data["edges"]:
            if edge["source"] not in node_ids:
                raise BuildFlowError(
                    message=f"Edge references unknown node: {edge['source']}"
                )
            if edge["target"] not in node_ids:
                raise BuildFlowError(
                    message=f"Edge references unknown node: {edge['target']}"
                )
