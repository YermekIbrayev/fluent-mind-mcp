"""Business logic layer for chatflow operations.

This module orchestrates chatflow operations by coordinating between
the FlowiseClient and providing structured logging, validation, and
user-friendly error translation.
"""

from typing import List

from fluent_mind_mcp.client.exceptions import ValidationError
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.models import Chatflow, PredictionResponse
from fluent_mind_mcp.utils.validators import validate_chatflow_id


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

    async def list_chatflows(self) -> List[Chatflow]:
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
        # Strip whitespace from input
        chatflow_id = chatflow_id.strip()

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
        # Strip whitespace from inputs
        chatflow_id = chatflow_id.strip()
        question = question.strip()

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
