"""Business logic layer for chatflow operations.

This module orchestrates chatflow operations by coordinating between
the FlowiseClient and providing structured logging, validation, and
user-friendly error translation.
"""


from fluent_mind_mcp.client.exceptions import ValidationError
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.models import Chatflow, PredictionResponse
from fluent_mind_mcp.models.chatflow import ChatflowType
from fluent_mind_mcp.utils.validators import (
    sanitize_inputs,
    sanitize_string,
    validate_chatflow_id,
    validate_flow_data,
)


class ChatflowService:
    """Service layer for chatflow business logic.

    Coordinates between FlowiseClient and provides:
    - Structured logging of all operations
    - Input validation before API calls
    - User-friendly error translation
    - Operation timing and metrics

    Attributes:
        client: FlowiseClient for API communication
        logger: OperationLogger for structured logging
    """

    def __init__(self, client: FlowiseClient, logger: OperationLogger) -> None:
        """Initialize ChatflowService with dependencies.

        Args:
            client: FlowiseClient for API operations
            logger: OperationLogger for operation logging
        """
        self.client = client
        self.logger = logger

    async def list_chatflows(self) -> list[Chatflow]:
        """List all chatflows with logging.

        WHY: Provides discovery of available chatflows with operation timing.

        Returns:
            List of Chatflow objects

        Raises:
            FlowiseClientError: On API errors (already user-friendly from client)
        """
        async with self.logger.log_operation("list_chatflows", {}) as log_ctx:
            try:
                chatflows = await self.client.list_chatflows()
                log_ctx["chatflow_count"] = len(chatflows)
                log_ctx["chatflow_ids"] = [cf.id for cf in chatflows]
                return chatflows
            except Exception as e:
                log_ctx["error"] = str(e)
                log_ctx["error_type"] = type(e).__name__
                self.logger.log_error("list_chatflows", exception=e)
                raise

    async def get_chatflow(self, chatflow_id: str) -> Chatflow:
        """Get chatflow by ID with logging and validation.

        WHY: Retrieves complete chatflow details with input validation.

        Args:
            chatflow_id: Unique chatflow identifier

        Returns:
            Chatflow object with complete details

        Raises:
            ValidationError: Invalid chatflow_id format
            FlowiseClientError: On API errors
        """
        # Sanitize input
        inputs = sanitize_inputs(chatflow_id=chatflow_id)
        chatflow_id = inputs['chatflow_id']

        # Validate input before API call
        if not validate_chatflow_id(chatflow_id):
            raise ValidationError(f"Invalid chatflow_id: '{chatflow_id}' (must be non-empty)")

        async with self.logger.log_operation(
            "get_chatflow", {"chatflow_id": chatflow_id}
        ) as log_ctx:
            try:
                chatflow = await self.client.get_chatflow(chatflow_id)
                log_ctx["chatflow_name"] = chatflow.name
                log_ctx["chatflow_type"] = chatflow.type
                log_ctx["deployed"] = chatflow.deployed
                return chatflow
            except Exception as e:
                log_ctx["error"] = str(e)
                log_ctx["error_type"] = type(e).__name__
                self.logger.log_error("get_chatflow", exception=e, chatflow_id=chatflow_id)
                raise

    async def run_prediction(
        self, chatflow_id: str, question: str
    ) -> PredictionResponse:
        """Execute chatflow with logging.

        WHY: Runs chatflow and logs execution timing and results.

        Args:
            chatflow_id: Chatflow to execute
            question: User input question

        Returns:
            PredictionResponse with chatflow output

        Raises:
            ValidationError: Invalid inputs
            FlowiseClientError: On API errors
        """
        # Sanitize inputs with robust security checks
        try:
            chatflow_id = sanitize_string(chatflow_id)
            question = sanitize_string(question, max_length=10000)  # Reasonable limit for questions
        except ValueError as e:
            raise ValidationError(f"Invalid input: {e}")

        # Validate inputs before API call
        if not validate_chatflow_id(chatflow_id):
            raise ValidationError(f"Invalid chatflow_id: '{chatflow_id}' (must be non-empty)")
        if not question:
            raise ValidationError("Question cannot be empty")

        async with self.logger.log_operation(
            "run_prediction",
            {"chatflow_id": chatflow_id, "question_length": len(question)},
        ) as log_ctx:
            try:
                response = await self.client.run_prediction(chatflow_id=chatflow_id, question=question)
                log_ctx["response_length"] = len(response.text)
                log_ctx["has_session_id"] = response.session_id is not None
                return response
            except Exception as e:
                log_ctx["error"] = str(e)
                log_ctx["error_type"] = type(e).__name__
                self.logger.log_error(
                    "run_prediction",
                    exception=e,
                    chatflow_id=chatflow_id,
                    question_length=len(question)
                )
                raise

    async def create_chatflow(
        self,
        name: str,
        flow_data: str,
        type: ChatflowType = ChatflowType.CHATFLOW,
        deployed: bool = False
    ) -> Chatflow:
        """Create new chatflow with validation and logging.

        WHY: Orchestrates chatflow creation with proper validation,
             logging, and error translation.

        Args:
            name: Chatflow display name
            flow_data: JSON string containing nodes and edges
            type: Chatflow type (defaults to CHATFLOW)
            deployed: Whether to deploy chatflow (defaults to False)

        Returns:
            Chatflow object with assigned ID

        Raises:
            ValidationError: Invalid name or flowData structure
            FlowiseClientError: On API errors
        """
        # Sanitize inputs with robust security checks
        try:
            name = sanitize_string(name, max_length=255)
        except ValueError as e:
            raise ValidationError(f"Invalid chatflow name: {e}")

        # Validate name
        if not name:
            raise ValidationError("Chatflow name cannot be empty")

        # Validate flow_data structure and size (<1MB)
        is_valid, error_message = validate_flow_data(flow_data)
        if not is_valid:
            raise ValidationError(f"Invalid flow_data: {error_message}")

        async with self.logger.log_operation(
            "create_chatflow",
            {"name": name, "chatflow_type": type.value, "deployed": deployed, "flow_data_size": len(flow_data)},
        ) as log_ctx:
            try:
                chatflow = await self.client.create_chatflow(
                    name=name,
                    flow_data=flow_data,
                    type=type,
                    deployed=deployed
                )
                log_ctx["chatflow_id"] = chatflow.id
                log_ctx["chatflow_name"] = chatflow.name
                return chatflow
            except Exception as e:
                log_ctx["error"] = str(e)
                # Use __class__.__name__ to avoid shadowing 'type' builtin
                error_type = e.__class__.__name__
                log_ctx["error_type"] = error_type
                self.logger.log_error(
                    "create_chatflow",
                    exception=e,
                    name=name,
                    chatflow_type=type.value
                )
                raise

    async def update_chatflow(
        self,
        chatflow_id: str,
        name: str | None = None,
        flow_data: str | None = None,
        deployed: bool | None = None
    ) -> Chatflow:
        """Update chatflow with validation and logging.

        WHY: Orchestrates chatflow updates with proper validation,
             logging, and error translation. Ensures at least one field
             is provided for update.

        Args:
            chatflow_id: Chatflow to update (required)
            name: New chatflow name (optional)
            flow_data: New JSON string containing nodes and edges (optional)
            deployed: New deployment status (optional)

        Returns:
            Chatflow object with updated fields

        Raises:
            ValidationError: Invalid chatflow_id, no fields provided, or invalid field values
            NotFoundError: Chatflow doesn't exist
            FlowiseClientError: On API errors
        """
        # Sanitize inputs
        inputs = sanitize_inputs(chatflow_id=chatflow_id, name=name)
        chatflow_id = inputs['chatflow_id']
        if name is not None:
            name = inputs['name']

        # Validate chatflow_id
        if not validate_chatflow_id(chatflow_id):
            raise ValidationError(f"Invalid chatflow_id: '{chatflow_id}' (must be non-empty)")

        # Validate at least one field is provided
        if name is None and flow_data is None and deployed is None:
            raise ValidationError("At least one field must be provided for update (name, flow_data, or deployed)")

        # Validate name if provided
        if name is not None and not name:
            raise ValidationError("Chatflow name cannot be empty")

        # Validate flow_data if provided
        if flow_data is not None:
            is_valid, error_message = validate_flow_data(flow_data)
            if not is_valid:
                raise ValidationError(f"Invalid flow_data: {error_message}")

        # Prepare log context with provided fields
        log_context: dict[str, object] = {"chatflow_id": chatflow_id}
        if name is not None:
            log_context["new_name"] = name
        if flow_data is not None:
            log_context["flow_data_size"] = len(flow_data)
        if deployed is not None:
            log_context["new_deployed_status"] = deployed

        async with self.logger.log_operation("update_chatflow", log_context) as log_ctx:
            try:
                chatflow = await self.client.update_chatflow(
                    chatflow_id=chatflow_id,
                    name=name,
                    flow_data=flow_data,
                    deployed=deployed
                )
                log_ctx["chatflow_name"] = chatflow.name
                log_ctx["chatflow_type"] = chatflow.type
                log_ctx["deployed"] = chatflow.deployed
                return chatflow
            except Exception as e:
                log_ctx["error"] = str(e)
                log_ctx["error_type"] = type(e).__name__
                self.logger.log_error(
                    "update_chatflow",
                    exception=e,
                    chatflow_id=chatflow_id
                )
                raise

    async def deploy_chatflow(self, chatflow_id: str, deployed: bool) -> Chatflow:
        """Toggle chatflow deployment status (convenience wrapper).

        WHY: Provides a convenient method for specifically toggling deployment
             status without needing to specify other fields. Wraps update_chatflow
             with only the deployed field.

        Args:
            chatflow_id: Chatflow to deploy/undeploy (required)
            deployed: True to deploy, False to undeploy

        Returns:
            Chatflow object with updated deployment status

        Raises:
            ValidationError: Invalid chatflow_id
            NotFoundError: Chatflow doesn't exist
            FlowiseClientError: On API errors
        """
        # Delegate to update_chatflow with only deployed field
        return await self.update_chatflow(
            chatflow_id=chatflow_id,
            deployed=deployed
        )

    async def delete_chatflow(self, chatflow_id: str) -> None:
        """Delete chatflow permanently with validation and logging.

        WHY: Orchestrates chatflow deletion with proper validation,
             logging, and error translation. Enables AI assistants to
             maintain clean workspace and manage resource usage.

        Args:
            chatflow_id: Chatflow to delete (required)

        Returns:
            None on successful deletion

        Raises:
            ValidationError: Invalid chatflow_id
            NotFoundError: Chatflow doesn't exist
            FlowiseClientError: On API errors
        """
        # Sanitize input
        inputs = sanitize_inputs(chatflow_id=chatflow_id)
        chatflow_id = inputs['chatflow_id']

        # Validate chatflow_id
        if not validate_chatflow_id(chatflow_id):
            raise ValidationError(f"Invalid chatflow_id: '{chatflow_id}' (must be non-empty)")

        async with self.logger.log_operation(
            "delete_chatflow", {"chatflow_id": chatflow_id}
        ) as log_ctx:
            try:
                await self.client.delete_chatflow(chatflow_id)
                log_ctx["deleted"] = True
                return None
            except Exception as e:
                log_ctx["error"] = str(e)
                log_ctx["error_type"] = type(e).__name__
                self.logger.log_error(
                    "delete_chatflow",
                    exception=e,
                    chatflow_id=chatflow_id
                )
                raise

    async def generate_agentflow_v2(self, description: str) -> dict[str, object]:
        """Generate AgentFlow V2 structure from natural language description.

        WHY: Enables AI assistants to create complex agent workflows from natural
             language, significantly lowering the technical barrier to agent creation.
             Orchestrates generation with validation, logging, and error translation.

        Args:
            description: Natural language description of desired agent (min 10 chars)

        Returns:
            Dictionary containing:
                - flowData: JSON string with generated nodes and edges structure
                - name: Generated chatflow name
                - description: Generated chatflow description (optional)

        Raises:
            ValidationError: Description too short (<10 chars) or invalid
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
            RateLimitError: Too many requests
        """
        # Sanitize input
        inputs = sanitize_inputs(description=description)
        description = inputs['description']

        # Validate description (minimum 10 characters)
        if len(description) < 10:
            raise ValidationError(
                f"Description too short: '{description}' (minimum 10 characters required)"
            )

        async with self.logger.log_operation(
            "generate_agentflow_v2",
            {"description_length": len(description), "description_preview": description[:50]}
        ) as log_ctx:
            try:
                result = await self.client.generate_agentflow_v2(description=description)
                log_ctx["generated_name"] = result.get("name")
                log_ctx["has_flowData"] = "flowData" in result
                if "flowData" in result:
                    flow_data = result["flowData"]
                    if isinstance(flow_data, str):
                        log_ctx["flow_data_size"] = len(flow_data)
                return result
            except Exception as e:
                log_ctx["error"] = str(e)
                log_ctx["error_type"] = type(e).__name__
                self.logger.log_error(
                    "generate_agentflow_v2",
                    exception=e,
                    description_length=len(description)
                )
                raise
