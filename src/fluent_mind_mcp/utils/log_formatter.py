"""
Credential masking formatter for secure logging.

Provides logging formatter that automatically masks sensitive
credentials (API keys, tokens, passwords) before logging.
"""

import logging
import re


class CredentialMaskingFormatter(logging.Formatter):
    """
    Logging formatter that masks sensitive credentials.

    Automatically masks API keys, Bearer tokens, passwords,
    and sensitive URLs before logging.
    """

    # Regex patterns for credential detection
    PATTERNS = [
        # API keys (common formats)
        (re.compile(r'(api[_-]?key["\s:=]+)([a-zA-Z0-9_\-]{20,})', re.IGNORECASE), r'\1***MASKED***'),
        (re.compile(r'(key["\s:=]+)([a-zA-Z0-9_\-]{20,})', re.IGNORECASE), r'\1***MASKED***'),

        # Bearer tokens (JWT format)
        (re.compile(r'(Bearer\s+)([a-zA-Z0-9_\-\.]+)', re.IGNORECASE), r'\1***MASKED***'),
        (re.compile(r'(token["\s:=]+)([a-zA-Z0-9_\-\.]{20,})', re.IGNORECASE), r'\1***MASKED***'),

        # Passwords
        (re.compile(r'(password["\s:=]+)([^\s"\']+)', re.IGNORECASE), r'\1***MASKED***'),
        (re.compile(r'(passwd["\s:=]+)([^\s"\']+)', re.IGNORECASE), r'\1***MASKED***'),
        (re.compile(r'(pwd["\s:=]+)([^\s"\']+)', re.IGNORECASE), r'\1***MASKED***'),

        # URLs with credentials (e.g., https://user:pass@host)
        (re.compile(r'(https?://)[^:]+:([^@]+)@', re.IGNORECASE), r'\1***MASKED***:***MASKED***@'),

        # Authorization headers
        (re.compile(r'(Authorization["\s:=]+["\']?)([^"\']+)', re.IGNORECASE), r'\1***MASKED***'),

        # Generic secrets
        (re.compile(r'(secret["\s:=]+)([^\s"\']{10,})', re.IGNORECASE), r'\1***MASKED***'),
    ]

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with credential masking.

        Args:
            record: Log record to format

        Returns:
            Formatted and masked log message
        """
        # Format the message first
        formatted = super().format(record)

        # Apply all masking patterns
        masked = formatted
        for pattern, replacement in self.PATTERNS:
            masked = pattern.sub(replacement, masked)

        return masked


def get_logger(
    name: str,
    level: int = logging.INFO,
    mask_credentials: bool = True,
) -> logging.Logger:
    """
    Get configured logger with credential masking.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (default INFO)
        mask_credentials: Enable credential masking (default True)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        if mask_credentials:
            formatter = CredentialMaskingFormatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
            )
        else:
            formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
