"""
Structured logging helper functions.

Provides helper functions for operation tracking, error logging,
performance monitoring, and token usage tracking.
"""

import logging
import time
from typing import Any


def log_operation_start(
    logger: logging.Logger,
    operation: str,
    **context: Any,
) -> float:
    """
    Log the start of an operation with context.

    Args:
        logger: Logger instance
        operation: Operation name
        **context: Additional context fields

    Returns:
        Start timestamp for timing
    """
    start_time = time.time()

    context_str = " | ".join(f"{k}={v}" for k, v in context.items()) if context else ""
    message = f"START {operation}"
    if context_str:
        message += f" | {context_str}"

    logger.info(message)
    return start_time


def log_operation_end(
    logger: logging.Logger,
    operation: str,
    start_time: float,
    success: bool = True,
    **context: Any,
) -> None:
    """
    Log the end of an operation with timing.

    Args:
        logger: Logger instance
        operation: Operation name
        start_time: Start timestamp from log_operation_start
        success: Whether operation succeeded
        **context: Additional context fields
    """
    duration = time.time() - start_time

    status = "SUCCESS" if success else "FAILED"
    context_str = " | ".join(f"{k}={v}" for k, v in context.items()) if context else ""

    message = f"END {operation} | {status} | duration={duration:.3f}s"
    if context_str:
        message += f" | {context_str}"

    if success:
        logger.info(message)
    else:
        logger.warning(message)


def log_error(
    logger: logging.Logger,
    operation: str,
    error: Exception,
    **context: Any,
) -> None:
    """
    Log an error with context and exception details.

    Args:
        logger: Logger instance
        operation: Operation that failed
        error: Exception that occurred
        **context: Additional context fields
    """
    error_type = type(error).__name__
    error_message = str(error)

    context_str = " | ".join(f"{k}={v}" for k, v in context.items()) if context else ""

    message = f"ERROR {operation} | {error_type}: {error_message}"
    if context_str:
        message += f" | {context_str}"

    logger.error(message, exc_info=True)


def log_performance(
    logger: logging.Logger,
    operation: str,
    duration: float,
    threshold: float,
    **context: Any,
) -> None:
    """
    Log performance metrics and warn if threshold exceeded.

    Args:
        logger: Logger instance
        operation: Operation name
        duration: Operation duration in seconds
        threshold: Warning threshold in seconds
        **context: Additional context fields
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items()) if context else ""

    message = f"PERFORMANCE {operation} | duration={duration:.3f}s | threshold={threshold:.3f}s"
    if context_str:
        message += f" | {context_str}"

    if duration > threshold:
        logger.warning(message)
    else:
        logger.debug(message)


def log_token_usage(
    logger: logging.Logger,
    operation: str,
    token_count: int,
    budget: int,
    **context: Any,
) -> None:
    """
    Log token usage and warn if budget exceeded.

    Args:
        logger: Logger instance
        operation: Operation name
        token_count: Actual token count
        budget: Token budget
        **context: Additional context fields
    """
    percentage = (token_count / budget * 100) if budget > 0 else 0
    context_str = " | ".join(f"{k}={v}" for k, v in context.items()) if context else ""

    message = f"TOKENS {operation} | used={token_count} | budget={budget} | {percentage:.1f}%"
    if context_str:
        message += f" | {context_str}"

    if token_count > budget:
        logger.warning(message)
    else:
        logger.debug(message)
