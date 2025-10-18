# Error Handling & Logging

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: Custom exceptions and credential masking

---

## Custom Exception Hierarchy

```python
# utils/exceptions.py

class FlowiseAutomationError(Exception):
    """Base exception for all automation errors"""
    pass

class CircuitOpenError(FlowiseAutomationError):
    """Raised when circuit breaker is open (<50 tokens per NFR-006)"""
    def __init__(self, dependency: str, retry_after_seconds: int):
        self.message = f"{dependency} unavailable. Retry in {retry_after_seconds}s"
        super().__init__(self.message)

class IncompatibleNodesError(FlowiseAutomationError):
    """Raised when nodes cannot be connected (<50 tokens)"""
    def __init__(self, nodes: List[str], reason: str):
        self.message = f"Cannot connect {nodes}: {reason}"
        super().__init__(self.message)

class TemplateNotFoundError(FlowiseAutomationError):
    """Raised when template_id not found (<50 tokens)"""
    def __init__(self, template_id: str):
        self.message = f"Template '{template_id}' not found. Try search_templates()"
        super().__init__(self.message)

class NodeCatalogStaleError(FlowiseAutomationError):
    """Raised when catalog is stale and refresh failed"""
    def __init__(self, staleness_hours: int):
        self.message = f"Node catalog {staleness_hours}h stale. Flowise server unreachable."
        super().__init__(self.message)
```

---

## Structured Logging with Credential Masking

```python
# utils/logging.py

class CredentialMaskingFormatter(logging.Formatter):
    """
    Mask sensitive data in logs.

    WHY: Security - prevents API keys, tokens from appearing in logs
    PATTERNS: api_key, Bearer tokens, other credentials
    """
    PATTERNS = [
        (r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', 'api_key=***'),
        (r'Bearer\s+([^\s]+)', 'Bearer ***'),
        (r'password["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', 'password=***')
    ]

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        for pattern, replacement in self.PATTERNS:
            msg = re.sub(pattern, replacement, msg, flags=re.IGNORECASE)
        return msg

# Configure logging for observability (NFR-033 to NFR-041)
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(CredentialMaskingFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    # Log all vector searches (NFR-033)
    # Log all build_flow invocations (NFR-034)
    # Log token usage per operation (NFR-035)
    # Track vector search relevance scores (NFR-036)
    # Log node catalog refresh operations (NFR-037)
    # Track circuit breaker state transitions (NFR-084)
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Testing Manual Checklists →](10-testing-manual-checklists.md)
