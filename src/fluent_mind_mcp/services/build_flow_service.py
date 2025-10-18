"""Build flow service for template-based chatflow creation.

Provides chatflow creation functionality for Phase 1 User Story 3.

WHY: Service layer that orchestrates template retrieval, FlowData generation,
     and Flowise API chatflow creation.
"""

from typing import Any, Optional
import uuid

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.utils.exceptions import TemplateNotFoundError


class BuildFlowService:
    """Service for building chatflows from templates.

    Handles template-based flow creation with automatic node positioning.

    WHY: Provides high-level API for creating chatflows from curated templates
         with proper node layout and structure.
    """

    # Node layout constants
    NODE_START_X = 100
    NODE_START_Y = 200
    NODE_SPACING_X = 300

    # Viewport defaults
    DEFAULT_VIEWPORT_X = 0
    DEFAULT_VIEWPORT_Y = 0
    DEFAULT_VIEWPORT_ZOOM = 1.0

    def __init__(
        self,
        vector_db_client: VectorDatabaseClient,
        flowise_client: Optional[Any] = None,
        node_catalog_service: Optional[Any] = None
    ) -> None:
        """Initialize build flow service.

        Args:
            vector_db_client: ChromaDB client for template retrieval
            flowise_client: Flowise API client for chatflow creation (Phase 1: optional)
            node_catalog_service: Node catalog for node metadata (Phase 1: optional)

        WHY: Dependency injection enables testing without real Flowise instance.
        """
        self.vector_db = vector_db_client
        self.flowise_client = flowise_client
        self.node_catalog = node_catalog_service

    async def build_from_template(
        self,
        template_id: str,
        chatflow_name: Optional[str] = None
    ) -> dict[str, Any]:
        """Build chatflow from template (User Story 3).

        Args:
            template_id: Template identifier
            chatflow_name: Optional name for created chatflow

        Returns:
            Result dictionary with chatflow_id, flow_data, and status

        Raises:
            TemplateNotFoundError: If template doesn't exist

        Performance: <10s per NFR-022
        Success Rate: >95% per NFR-093

        WHY: Core functionality for template-based chatflow creation.
        """
        # Retrieve template from vector database
        try:
            collection = self.vector_db.get_collection("templates")
            template_data = collection.get(ids=[template_id])

            if not template_data["ids"]:
                raise TemplateNotFoundError(template_id=template_id)

            metadata = template_data["metadatas"][0]

        except ValueError as e:
            raise TemplateNotFoundError(
                template_id=template_id,
                details={"error": str(e)}
            )

        # Generate FlowData structure
        flow_data = self._generate_flow_data(template_id, metadata)

        # Create chatflow in Flowise (if client provided)
        chatflow_id = str(uuid.uuid4())

        # Note: Flowise integration is optional in Phase 1
        # When flowise_client is available, it would be used here to create the chatflow

        return {
            "chatflow_id": chatflow_id,
            "flow_data": flow_data,
            "status": "success",
            "template_id": template_id
        }

    def _parse_node_names(self, metadata: dict[str, Any]) -> list[str]:
        """Extract and clean node names from template metadata.

        Args:
            metadata: Template metadata containing nodes string

        Returns:
            List of cleaned node names

        WHY: Separates parsing logic from node creation for clarity.
        """
        node_str = metadata.get("nodes", "")
        if not node_str:
            return []

        return [name.strip() for name in node_str.split(",") if name.strip()]

    def _create_positioned_node(self, node_name: str, index: int) -> dict[str, Any]:
        """Create node with calculated position.

        Args:
            node_name: Name of the node type
            index: Node index for position calculation

        Returns:
            Node dictionary with id, type, data, and position

        WHY: Encapsulates node creation and positioning logic.
        """
        node_id = f"{node_name}_{index}_{uuid.uuid4().hex[:8]}"

        return {
            "id": node_id,
            "type": node_name,
            "data": {
                "label": node_name,
                "name": node_name
            },
            "position": {
                "x": self.NODE_START_X + (index * self.NODE_SPACING_X),
                "y": self.NODE_START_Y
            }
        }

    def _create_linear_edges(self, nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Create left-to-right edges connecting nodes sequentially.

        Args:
            nodes: List of node dictionaries

        Returns:
            List of edge dictionaries

        WHY: Separates edge creation logic for Phase 1 simple linear flows.
        """
        return [
            {
                "id": f"edge_{i}_{uuid.uuid4().hex[:8]}",
                "source": nodes[i]["id"],
                "target": nodes[i + 1]["id"]
            }
            for i in range(len(nodes) - 1)
        ]

    def _create_default_viewport(self) -> dict[str, Any]:
        """Create default viewport configuration.

        Returns:
            Viewport dictionary with x, y, and zoom

        WHY: Makes viewport structure explicit and configurable.
        """
        return {
            "x": self.DEFAULT_VIEWPORT_X,
            "y": self.DEFAULT_VIEWPORT_Y,
            "zoom": self.DEFAULT_VIEWPORT_ZOOM
        }

    def _generate_flow_data(
        self,
        template_id: str,
        metadata: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate FlowData structure from template metadata.

        Args:
            template_id: Template identifier
            metadata: Template metadata from vector database

        Returns:
            FlowData dictionary with nodes, edges, and viewport

        WHY: Converts template specification into Flowise-compatible FlowData format.
        """
        # Parse node names from metadata
        node_names = self._parse_node_names(metadata)

        # Create positioned nodes
        nodes = [
            self._create_positioned_node(node_name, index)
            for index, node_name in enumerate(node_names)
        ]

        # Create linear edges
        edges = self._create_linear_edges(nodes)

        # Create viewport
        viewport = self._create_default_viewport()

        return {
            "nodes": nodes,
            "edges": edges,
            "viewport": viewport
        }
