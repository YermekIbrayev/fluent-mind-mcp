"""Structured logging with credential masking for MCP operations.

This module provides the OperationLogger class for logging operations with
timing, structured data, and automatic credential masking for security.
"""

import logging
import re
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Dict, Optional, Generator


# Patterns for credential masking (case-insensitive)
CREDENTIAL_PATTERNS = [
    (re.compile(r'(api_key|apikey)=([^\s]+)', re.IGNORECASE), r'\1=***'),
    (re.compile(r'(password|passwd|pwd)=([^\s]+)', re.IGNORECASE), r'\1=***'),
    (re.compile(r'(token|bearer)=([^\s]+)', re.IGNORECASE), r'\1=***'),
    (re.compile(r'(secret|auth)=([^\s]+)', re.IGNORECASE), r'\1=***'),
]

# Keys that should have their values masked
SENSITIVE_KEYS = {'api_key', 'apikey', 'password', 'passwd', 'pwd', 'token', 'secret', 'auth', 'bearer'}


class OperationLogger:
    """Structured logger with timing and credential masking.

    Provides logging with automatic credential masking, operation timing,
    and structured data output for better observability.

    Attributes:
        name: Logger name for identification
        logger: Underlying Python logger instance
    """

    def __init__(self, name: str, level: str = "INFO") -> None:
        """Initialize OperationLogger.

        Args:
            name: Logger name for identification
            level: Log level (DEBUG, INFO, WARNING, ERROR)
        """
        self.name = name
        self.logger = logging.getLogger(name)

        # Always set logger to minimum level for flexibility
        # WHY: Allows test frameworks (caplog) and handlers to control filtering
        # The actual filtering happens at the handler level
        self.logger.setLevel(logging.DEBUG if level == "INFO" else getattr(logging, level.upper()))

        # Add handler only if none exists
        # WHY: pytest caplog provides its own handler via propagation
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(getattr(logging, level.upper()))
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _mask_credentials(self, message: str) -> str:
        """Mask credentials in log message.

        WHY: Security requirement - never log sensitive credentials.

        Args:
            message: Original log message

        Returns:
            Message with credentials masked
        """
        masked = message
        for pattern, replacement in CREDENTIAL_PATTERNS:
            masked = pattern.sub(replacement, masked)
        return masked

    def _mask_dict_credentials(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask credentials in dictionary values.

        WHY: Security requirement for structured logging data.

        Args:
            data: Dictionary that may contain credentials

        Returns:
            Dictionary with credential values masked
        """
        masked = {}
        for key, value in data.items():
            if key.lower() in SENSITIVE_KEYS:
                masked[key] = "***"
            else:
                masked[key] = value
        return masked

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with credential masking."""
        masked_message = self._mask_credentials(message)
        self.logger.debug(masked_message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with credential masking."""
        masked_message = self._mask_credentials(message)
        self.logger.info(masked_message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with credential masking."""
        masked_message = self._mask_credentials(message)
        self.logger.warning(masked_message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with credential masking."""
        masked_message = self._mask_credentials(message)
        self.logger.error(masked_message, **kwargs)

    def _log_operation_message(
        self,
        operation: str,
        duration: float,
        status: str,
        **context: Any
    ) -> None:
        """Log operation with structured data (internal helper).

        WHY: Provides consistent structured logging for operations.

        Args:
            operation: Operation name (e.g., "list_chatflows")
            duration: Operation duration in seconds
            status: Operation status ("success" or "failure")
            **context: Additional structured data
        """
        # Mask credentials in context
        masked_context = self._mask_dict_credentials(context)

        # Build structured log message
        context_str = ", ".join(f"{k}={v}" for k, v in masked_context.items())
        message = f"operation={operation}, status={status}, duration={duration:.3f}s"
        if context_str:
            message += f", {context_str}"

        # Log at appropriate level
        if status == "failure":
            self.logger.error(message)
        else:
            self.logger.info(message)

    @contextmanager
    def time_operation(self, operation: str, **context: Any) -> Generator[None, None, None]:
        """Context manager for timing operations.

        WHY: Automatically captures operation duration and logs completion.

        Args:
            operation: Operation name
            **context: Additional context to log

        Yields:
            None

        Example:
            with logger.time_operation("fetch_chatflow", chatflow_id="123"):
                # Do work
                pass
        """
        start_time = time.time()
        exception_occurred = False

        try:
            yield
        except Exception:
            exception_occurred = True
            raise
        finally:
            duration = time.time() - start_time
            status = "failure" if exception_occurred else "success"
            self._log_operation_message(operation, duration, status, **context)

    @asynccontextmanager
    async def log_operation(
        self, operation: str, initial_context: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Async context manager for logging operations with timing.

        WHY: Provides automatic operation timing and logging for async operations.
        Returns a mutable context dict that can be updated during the operation.

        Args:
            operation: Operation name
            initial_context: Initial context to log

        Yields:
            Mutable context dictionary that will be logged

        Example:
            async with logger.log_operation("fetch_chatflow", {"id": "123"}) as ctx:
                result = await fetch()
                ctx["result_count"] = len(result)
        """
        start_time = time.time()
        context = dict(initial_context)  # Copy to avoid mutation
        exception_occurred = False

        try:
            yield context
        except Exception:
            exception_occurred = True
            raise
        finally:
            duration = time.time() - start_time
            status = "failure" if exception_occurred else "success"

            # Mask credentials in context
            masked_context = self._mask_dict_credentials(context)

            # Build structured log message
            context_str = ", ".join(f"{k}={v}" for k, v in masked_context.items())
            message = f"operation={operation}, status={status}, duration={duration:.3f}s"
            if context_str:
                message += f", {context_str}"

            # Log at appropriate level
            if status == "failure":
                self.logger.error(message)
            else:
                self.logger.info(message)

    def log_error(
        self,
        operation: str,
        exception: Optional[Exception] = None,
        include_traceback: bool = False,
        **context: Any
    ) -> None:
        """Log error with exception details and context.

        WHY: Provides consistent error logging with context.

        Args:
            operation: Operation that failed
            exception: Optional exception object
            include_traceback: Whether to include full traceback
            **context: Additional error context
        """
        # Mask credentials in context
        masked_context = self._mask_dict_credentials(context)

        # Build error message
        context_str = ", ".join(f"{k}={v}" for k, v in masked_context.items())
        message = f"operation={operation} failed"
        if context_str:
            message += f", {context_str}"

        if exception:
            message += f", exception={exception.__class__.__name__}: {str(exception)}"

        self.logger.error(message, exc_info=include_traceback)
