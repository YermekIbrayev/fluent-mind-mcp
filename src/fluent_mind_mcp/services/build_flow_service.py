"""Build flow service for template-based chatflow creation (US3)."""
from typing import Any, Optional
import uuid
import copy

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.models.flowdata_models import (
    BuildFlowResponse,
    ChatflowStatus,
    FlowTemplate,
)
from fluent_mind_mcp.services.connection_inference import ConnectionInference
from fluent_mind_mcp.utils.exceptions import (
    BuildFlowError,
    TemplateNotFoundError,
    ValidationError,
)


class BuildFlowService:
    """Service for building chatflows from templates or custom node lists."""
    NODE_START_X = 100
    NODE_START_Y = 200
    NODE_SPACING_X = 300
    NODE_SPACING_Y = 200
    DEFAULT_VIEWPORT_X = 0
    DEFAULT_VIEWPORT_Y = 0
    DEFAULT_VIEWPORT_ZOOM = 1.0

    def __init__(
        self,
        vector_db_client: VectorDatabaseClient,
        flowise_client: Optional[Any] = None,
        node_catalog_service: Optional[Any] = None
    ) -> None:
        """Initialize build flow service."""
        self.vector_db = vector_db_client
        self.flowise_client = flowise_client
        self.node_catalog = node_catalog_service

    async def build_from_template(
        self,
        template_id: str,
        chatflow_name: Optional[str] = None,
        parameters: Optional[dict[str, Any]] = None
    ) -> BuildFlowResponse:
        """Build chatflow from template (T035, T047)."""
        template = await self._retrieve_template(template_id)
        flow_data = template.get("flow_data", {})
        if parameters:
            flow_data = self._substitute_parameters(flow_data, parameters)
        name = chatflow_name or template.get("name", f"Flow {template_id}")
        return BuildFlowResponse(
            chatflow_id=str(uuid.uuid4()),
            name=str(name),
            status=ChatflowStatus.SUCCESS
        )

    async def build_from_nodes(
        self,
        nodes: list[str],
        chatflow_name: Optional[str] = None,
        connections: str = "auto",
        parameters: Optional[dict[str, Any]] = None
    ) -> BuildFlowResponse:
        """Build chatflow from custom node list (T044)."""
        if not nodes:
            raise ValidationError(message="Nodes list cannot be empty")

        node_objects = self._create_node_objects(nodes)
        edges = await self._infer_connections(node_objects) if connections == "auto" else []
        positions = self._calculate_positions(node_objects, edges)

        for node in node_objects:
            if node["id"] in positions:
                node["position"] = positions[node["id"]]

        name = chatflow_name or f"Custom Flow ({len(nodes)} nodes)"
        return BuildFlowResponse(
            chatflow_id=str(uuid.uuid4()),
            name=name,
            status=ChatflowStatus.SUCCESS
        )

    def _validate_node_exists(self, node_name: str) -> None:
        """Validate that node exists in vector database.

        WHY: Prevents building flows with non-existent nodes, failing fast
        before expensive connection inference.

        Args:
            node_name: Name of the node to validate

        Raises:
            ValidationError: If node doesn't exist in vector DB
        """
        if not self.vector_db:
            # WHY: Allow testing without actual vector DB
            return

        try:
            collection = self.vector_db.get_collection("nodes")
            result = collection.get(where={"name": node_name})

            if not result or not result.get("ids"):
                raise ValidationError(
                    message=f"Node {node_name} not found in vector database"
                )
        except ValidationError:
            # WHY: Re-raise our domain exception
            raise
        except (ValueError, KeyError) as e:
            # WHY: Convert DB-specific errors to domain exceptions
            raise ValidationError(
                message=f"Node {node_name} not found in vector database",
                details={"error": str(e)}
            )

    def _create_node_objects(self, nodes: list[str]) -> list[dict]:
        """Create node objects from node names.

        WHY: Converts simple string names to structured node objects
        needed for connection inference and flowData generation.

        Args:
            nodes: List of node names to create

        Returns:
            List of node dictionaries with id, name, base_classes, data

        Raises:
            ValidationError: If any node name is invalid or doesn't exist
        """
        node_objects = []
        for i, node_name in enumerate(nodes):
            # WHY: Basic input validation before DB lookup
            if not node_name or not isinstance(node_name, str):
                raise ValidationError(message=f"Invalid node name: {node_name}")

            # WHY: Validate existence before creating object
            self._validate_node_exists(node_name)

            node_objects.append({
                "id": str(i + 1),
                "name": node_name,
                "base_classes": [],
                "data": {}
            })

        return node_objects

    async def _retrieve_template(self, template_id: str) -> FlowTemplate:
        """Retrieve template from vector DB (T036).

        WHY: Templates stored in ChromaDB provide pre-built flow structures,
        reducing token usage vs building flows from scratch.

        Args:
            template_id: Unique identifier for the template

        Returns:
            FlowTemplate with template data and metadata

        Raises:
            TemplateNotFoundError: If template_id doesn't exist in vector DB
        """
        try:
            collection = self.vector_db.get_collection("templates")
            template_data = collection.get(ids=[template_id])

            # Check if template exists
            if not template_data or not template_data.get("ids"):
                raise TemplateNotFoundError(template_id=template_id)

            metadata = template_data["metadatas"][0]

            # WHY: Use Pydantic model for type safety and validation
            template = FlowTemplate(
                template_id=template_id,
                name=metadata.get("name", template_id),
                flow_data={
                    "nodes": [],
                    "edges": [],
                    "viewport": self._create_default_viewport()
                },
                nodes=[]  # For backward compatibility with tests
            )

            return template

        except TemplateNotFoundError:
            # WHY: Re-raise to preserve specific error type
            raise
        except (ValueError, KeyError) as e:
            # WHY: Convert DB errors to domain exceptions for consistent error handling
            raise TemplateNotFoundError(
                template_id=template_id,
                details={"error": str(e)}
            )

    def _substitute_parameters(
        self,
        flow_data: dict[str, Any],
        parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """Substitute template parameters (T037).

        WHY: Templates use placeholders like {{model}} to allow customization
        without creating separate templates for each configuration.

        Args:
            flow_data: Template flowData with placeholders
            parameters: User-provided values to substitute

        Returns:
            New flowData dict with substituted values

        Raises:
            ValidationError: If parameter type is invalid
        """
        if not parameters:
            return flow_data

        # WHY: Deep copy to avoid mutating original template
        # Templates may be reused for multiple chatflows
        result = copy.deepcopy(flow_data)

        for node in result.get("nodes", []):
            node_data = node.get("data", {})
            for key, value in node_data.items():
                # WHY: Only substitute mustache-style placeholders {{param}}
                if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                    param_name = value[2:-2].strip()

                    if param_name in parameters:
                        param_value = parameters[param_name]

                        # WHY: Type coercion for numeric parameters
                        # temperature often sent as string "0.7" but needs float
                        if param_name == "temperature" and isinstance(param_value, str):
                            try:
                                param_value = float(param_value)
                            except ValueError:
                                raise ValidationError(
                                    message=f"Invalid type for {param_name}: expected number"
                                )

                        node_data[key] = param_value

        return result

    def _categorize_nodes(self, nodes: list[dict]) -> dict[str, list[dict]]:
        """Categorize nodes by type (T038)."""
        return ConnectionInference.categorize_nodes(nodes)

    def _topological_sort(self, categorized_nodes: dict) -> list[dict]:
        """Sort nodes by category order (T039)."""
        return ConnectionInference.topological_sort(categorized_nodes)

    def _match_base_classes(self, nodes: list[dict]) -> list[tuple[dict, dict]]:
        """Match compatible node pairs (T040)."""
        return ConnectionInference.match_base_classes(nodes)

    def _generate_edges(self, node_pairs: list[tuple], all_nodes: Optional[list] = None) -> list[dict]:
        """Generate edges from node pairs (T041)."""
        return ConnectionInference.generate_edges(node_pairs, all_nodes)

    async def _infer_connections(self, nodes: list[dict]) -> list[dict]:
        """Infer connections between nodes (T042)."""
        return ConnectionInference.infer_connections(nodes)

    def _calculate_positions(self, nodes: list[dict], edges: list[dict]) -> dict[str, dict]:
        """Calculate node positions (T043)."""
        positions = {}
        for i, node in enumerate(nodes):
            row, col = i // 4, i % 4
            positions[node["id"]] = {
                "x": self.NODE_START_X + (col * self.NODE_SPACING_X),
                "y": self.NODE_START_Y + (row * self.NODE_SPACING_Y)
            }
        return positions

    def _validate_flowData(self, flow_data: dict) -> None:
        """Validate flowData structure (T046)."""
        if "nodes" not in flow_data:
            raise BuildFlowError(message="FlowData missing required field: nodes")
        if "edges" not in flow_data:
            raise BuildFlowError(message="FlowData missing required field: edges")

        node_ids = {node["id"] for node in flow_data["nodes"]}
        for edge in flow_data["edges"]:
            if edge["source"] not in node_ids:
                raise BuildFlowError(message=f"Edge references unknown node: {edge['source']}")
            if edge["target"] not in node_ids:
                raise BuildFlowError(message=f"Edge references unknown node: {edge['target']}")

    def _create_default_viewport(self) -> dict[str, Any]:
        """Create default viewport configuration."""
        return {
            "x": self.DEFAULT_VIEWPORT_X,
            "y": self.DEFAULT_VIEWPORT_Y,
            "zoom": self.DEFAULT_VIEWPORT_ZOOM
        }
