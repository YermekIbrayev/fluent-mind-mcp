"""Template service for template retrieval and parameter substitution.

WHY: Extracted from BuildFlowService to maintain file size limits (<200 lines).
     Separates template-specific logic from flow building logic.
"""

import copy
from typing import Any

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.models.flowdata_models import FlowTemplate
from fluent_mind_mcp.utils.exceptions import TemplateNotFoundError, ValidationError


class TemplateService:
    """Handles template retrieval and parameter substitution.

    WHY: Single Responsibility - focused on template operations only.
    """

    # Default viewport configuration
    DEFAULT_VIEWPORT_X = 0
    DEFAULT_VIEWPORT_Y = 0
    DEFAULT_VIEWPORT_ZOOM = 1.0

    def __init__(self, vector_db_client: VectorDatabaseClient) -> None:
        """Initialize template service.

        Args:
            vector_db_client: Client for vector database operations
        """
        self.vector_db = vector_db_client

    async def retrieve_template(self, template_id: str) -> FlowTemplate:
        """Retrieve template from vector DB.

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

            if not template_data or not template_data.get("ids"):
                raise TemplateNotFoundError(template_id=template_id)

            metadata = template_data["metadatas"][0]

            template = FlowTemplate(
                template_id=template_id,
                name=metadata.get("name", template_id),
                flow_data={
                    "nodes": [],
                    "edges": [],
                    "viewport": self._create_default_viewport()
                },
                nodes=[]
            )

            return template

        except TemplateNotFoundError:
            raise
        except (ValueError, KeyError) as e:
            raise TemplateNotFoundError(
                template_id=template_id,
                details={"error": str(e)}
            )

    def substitute_parameters(
        self,
        flow_data: dict[str, Any],
        parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """Substitute template parameters with user-provided values.

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

        result = copy.deepcopy(flow_data)

        for node in result.get("nodes", []):
            node_data = node.get("data", {})
            self._substitute_node_parameters(node_data, parameters)

        return result

    def _substitute_node_parameters(
        self,
        node_data: dict[str, Any],
        parameters: dict[str, Any]
    ) -> None:
        """Substitute parameters in a single node's data.

        WHY: Extract Method refactoring to reduce complexity.

        Args:
            node_data: Node data dictionary (modified in place)
            parameters: User-provided values to substitute

        Raises:
            ValidationError: If parameter type is invalid
        """
        for key, value in node_data.items():
            if not self._is_placeholder(value):
                continue

            param_name = self._extract_param_name(value)
            if param_name in parameters:
                param_value = self._coerce_param_value(
                    param_name,
                    parameters[param_name]
                )
                node_data[key] = param_value

    def _is_placeholder(self, value: Any) -> bool:
        """Check if value is a mustache-style placeholder.

        WHY: Named predicate for clarity.

        Args:
            value: Value to check

        Returns:
            True if value is a placeholder like {{param}}
        """
        return (
            isinstance(value, str)
            and value.startswith("{{")
            and value.endswith("}}")
        )

    def _extract_param_name(self, placeholder: str) -> str:
        """Extract parameter name from placeholder.

        WHY: Single responsibility - isolate string parsing logic.

        Args:
            placeholder: Placeholder string like {{model}}

        Returns:
            Parameter name (e.g., "model")
        """
        return placeholder[2:-2].strip()

    def _coerce_param_value(self, param_name: str, param_value: Any) -> Any:
        """Coerce parameter value to correct type.

        WHY: Type safety - handle common type conversions.

        Args:
            param_name: Name of the parameter
            param_value: Raw parameter value

        Returns:
            Type-coerced value

        Raises:
            ValidationError: If type coercion fails
        """
        if param_name == "temperature" and isinstance(param_value, str):
            try:
                return float(param_value)
            except ValueError:
                raise ValidationError(
                    message=f"Invalid type for {param_name}: expected number"
                )
        return param_value

    def _create_default_viewport(self) -> dict[str, Any]:
        """Create default viewport configuration.

        WHY: Encapsulate default values in a single place.

        Returns:
            Viewport configuration dictionary
        """
        return {
            "x": self.DEFAULT_VIEWPORT_X,
            "y": self.DEFAULT_VIEWPORT_Y,
            "zoom": self.DEFAULT_VIEWPORT_ZOOM
        }
