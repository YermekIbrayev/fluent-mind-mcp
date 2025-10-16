# Implementation Plan: Fluent Mind MCP Server

**Feature Branch**: `001-flowise-mcp-server`
**Created**: 2025-10-16
**Planning Method**: Clean Code MCP
**Based on**: [spec.md](spec.md)

---

## Executive Summary

This plan outlines the implementation of a Model Context Protocol (MCP) server that provides complete lifecycle management for Flowise chatflows. The system enables AI assistants to programmatically create, read, update, delete, and execute Flowise workflows through 8 MCP tools.

**Key Targets:**
- Support 5-10 concurrent AI assistants
- Handle up to 100 chatflows
- Response times: 5s (list/get/execute), 10s (create), 60s (full lifecycle)
- Flowise v1.x compatibility
- Standard operational logging

---

## Architecture Overview

### System Layers

The architecture follows clean separation of concerns with four distinct layers:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: MCP Server Interface                          │
│  - Exposes 8 MCP tools to AI assistants                │
│  - Parameter validation and format conversion          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Service/Business Logic                        │
│  - ChatflowService orchestrates operations              │
│  - Business rule validation                             │
│  - Error translation and logging                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Flowise Client                                │
│  - HTTP communication with Flowise REST API             │
│  - Authentication and timeout management                │
│  - Async/non-blocking operations                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 4: Domain Models                                 │
│  - Type-safe data structures (Pydantic)                 │
│  - Serialization/deserialization                        │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

**Request Flow:**
1. AI Assistant → MCP Tool Call
2. MCP Server → Validates parameters, creates domain models
3. Service Layer → Applies business rules, logs operation start
4. Flowise Client → HTTP request to Flowise API
5. Flowise API → Processes request, returns response

**Response Flow:**
1. Flowise API → JSON response
2. Flowise Client → Parses response, handles errors
3. Service Layer → Translates to domain models, logs completion
4. MCP Server → Formats as MCP response
5. AI Assistant → Receives structured result

---

## Module Organization

Following clean code principles with single responsibility per module:

```
src/fluent_mind_mcp/
├── server.py                    # MCP server entry point, tool definitions
├── services/
│   ├── __init__.py
│   └── chatflow_service.py      # Business logic orchestration
├── client/
│   ├── __init__.py
│   ├── flowise_client.py        # HTTP client implementation
│   └── exceptions.py            # Custom exception hierarchy
├── models/
│   ├── __init__.py
│   ├── chatflow.py              # Chatflow, FlowData domain models
│   ├── config.py                # Configuration model
│   └── responses.py             # API response models
├── logging/
│   ├── __init__.py
│   └── operation_logger.py      # Structured logging (NFR-001 to NFR-004)
└── utils/
    ├── __init__.py
    └── validators.py            # Input validation helpers
```

### Module Responsibilities

**server.py**
- Purpose: MCP protocol handling only
- Responsibilities:
  - Define 8 MCP tools with schemas
  - Validate MCP-level parameters
  - Convert between MCP format and domain models
  - Handle MCP error responses
- Dependencies: FastMCP, services, models

**services/chatflow_service.py**
- Purpose: Business logic orchestration
- Responsibilities:
  - Implement 8 chatflow operations
  - Validate business rules (identifiers, required fields)
  - Translate Flowise errors to user-friendly messages
  - Coordinate logging via OperationLogger
- Dependencies: client, models, logging
- No HTTP details leak into this layer

**client/flowise_client.py**
- Purpose: HTTP communication with Flowise
- Responsibilities:
  - Manage HTTP connections (async, pooling)
  - Format requests to Flowise API endpoints
  - Parse API responses to domain models
  - Handle authentication (API key)
  - Implement timeout configuration
  - Raise specific exceptions for failures
- Dependencies: httpx, models
- No business logic in this layer

**client/exceptions.py**
- Purpose: Custom exception hierarchy
- Exceptions:
  - `FlowiseClientError` (base)
  - `ConnectionError` (network, timeout)
  - `AuthenticationError` (invalid API key)
  - `ValidationError` (malformed data, invalid IDs)
  - `NotFoundError` (chatflow doesn't exist)
  - `RateLimitError` (Flowise throttling)

**models/chatflow.py**
- Purpose: Domain model definitions
- Models:
  - `Chatflow`: id, name, type, deployed, flowData
  - `FlowData`: nodes, edges structures
  - Type validation via Pydantic
  - Serialization methods (to/from JSON)

**models/config.py**
- Purpose: Configuration management
- Model:
  ```python
  class FlowiseConfig:
      api_url: str              # FLOWISE_API_URL env var
      api_key: Optional[str]    # FLOWISE_API_KEY env var
      timeout: int = 60         # Request timeout (FR-014)
      max_connections: int = 10 # Connection pool size
      log_level: str = "INFO"   # Logging level
      flowise_version: str = "v1.x"  # Compatibility target

      @classmethod
      def from_env(cls):
          # Load from environment with validation
  ```

**logging/operation_logger.py**
- Purpose: Structured logging for observability (NFR-001 to NFR-004)
- Responsibilities:
  - Log all errors with context (operation, parameters, error details)
  - Log key operations (create, update, delete, execute)
  - Log operation timing (start, duration, completion)
  - Log warnings (slow responses, retries, connection issues)
  - Protect credentials from logs (NFR-012)
- Format: timestamp, level, operation, chatflow_id, duration, status, message
- Context manager for timing:
  ```python
  with operation_logger.time_operation("create_chatflow", chatflow_id):
      result = await flowise_client.create(...)
  ```

**utils/validators.py**
- Purpose: Reusable input validation
- Functions:
  - `validate_chatflow_id(id: str)` - Check identifier format
  - `validate_flow_data(data: str)` - Parse and validate JSON structure
  - `validate_chatflow_type(type: str)` - Check against allowed types
  - `sanitize_error_message(msg: str)` - Remove sensitive data

---

## Error Handling Strategy

### Exception Hierarchy

```
FlowiseClientError (base)
├── ConnectionError
│   ├── TimeoutError
│   └── NetworkError
├── AuthenticationError
├── ValidationError
│   ├── InvalidIdentifierError
│   └── MalformedDataError
├── NotFoundError
├── RateLimitError
└── UnexpectedError
```

### Error Translation Flow

**Client Layer:**
- Raises specific exceptions with HTTP details
- Example: `raise AuthenticationError(f"Invalid API key: {status_code}")`

**Service Layer:**
- Catches client exceptions
- Logs error with context
- Translates to user-friendly message
- Example: "Authentication failed. Please verify your FLOWISE_API_KEY is correct."

**Server Layer:**
- Converts to MCP error response
- Includes corrective guidance
- Example: Include link to configuration docs

### Error Scenarios (from Edge Cases)

1. **Flowise API unreachable** → ConnectionError → "Cannot connect to Flowise at {url}. Verify the service is running."
2. **Invalid API key** → AuthenticationError → "Authentication failed. Check FLOWISE_API_KEY configuration."
3. **Malformed flowData** → ValidationError → "Invalid workflow structure: {specific_issue}"
4. **Very large flowData (>1MB)** → ValidationError → "Workflow structure exceeds size limit (1MB)"
5. **Chatflow being updated** → Retry once, then error → "Chatflow is currently busy. Try again."
6. **Rate limiting** → RateLimitError with retry-after → "Rate limit exceeded. Retry in {seconds}s."
7. **Execution timeout** → TimeoutError → "Chatflow execution exceeded timeout ({timeout}s)"
8. **Concurrent operations** → Allow (no locks), Flowise handles conflicts

---

## Concurrency and Performance

### Async/Await Strategy (FR-015, NFR-005 to NFR-007)

**Non-blocking Operations:**
- All I/O operations use async/await
- FlowiseClient methods are async
- Service layer methods are async
- MCP tools use async handlers

**Connection Pooling:**
```python
# FlowiseClient initialization
self.http_client = httpx.AsyncClient(
    base_url=config.api_url,
    timeout=config.timeout,
    limits=httpx.Limits(
        max_connections=10,      # NFR-005: Support 5-10 concurrent
        max_keepalive_connections=5
    )
)
```

**Concurrency Targets:**
- 5-10 concurrent AI assistant connections (NFR-005)
- 5-10 simultaneous operations (NFR-006)
- Maintain performance targets under concurrent load (NFR-007)

**No Global State:**
- Each request is independent
- No shared mutable state between operations
- Thread-safe logging via queue handler

---

## Configuration Management

### Environment Variables (FR-009)

Required:
- `FLOWISE_API_URL` - Flowise instance URL (e.g., http://localhost:3000)

Optional:
- `FLOWISE_API_KEY` - API key for secured instances (NFR-010)
- `FLOWISE_TIMEOUT` - Request timeout in seconds (default: 60)
- `FLOWISE_MAX_CONNECTIONS` - Connection pool size (default: 10)
- `LOG_LEVEL` - Logging level (default: INFO)

### Configuration Validation

```python
config = FlowiseConfig.from_env()
# Validates:
# - api_url is valid URL format
# - timeout is positive integer
# - max_connections is positive integer
# - Flowise version compatibility (v1.x check)
```

---

## Data Volume Handling

### Chatflow Catalog (NFR-008, NFR-009)

**Scale:** Up to 100 chatflows

**list_chatflows Operation:**
- Returns all chatflows in single response
- No pagination needed for ≤100 items
- Must complete within 5 seconds (SC-002)

**No Caching Required:**
- Flowise API is source of truth
- Fresh data on every request
- Simpler implementation, no cache invalidation

**Large flowData Handling:**
- Validate size before accepting (reject >1MB)
- Stream large responses if needed
- No in-memory accumulation of all chatflows at once

---

## Implementation Phases

### Phase 1: Foundation (P1 - Query and Execute Chatflows)

**Goal:** Enable AI assistants to list, retrieve, and execute existing chatflows

**Tasks:**
1. Project setup
   - Create pyproject.toml with dependencies (fastmcp, httpx, pydantic)
   - Setup src/fluent_mind_mcp/ structure
   - Create .env.example

2. Configuration and models
   - Implement FlowiseConfig in models/config.py
   - Implement Chatflow and FlowData models in models/chatflow.py
   - Add validation rules

3. Flowise client - Read operations
   - Implement FlowiseClient class in client/flowise_client.py
   - Add async HTTP client with connection pooling
   - Implement GET /api/v1/chatflows (list_chatflows)
   - Implement GET /api/v1/chatflows/{id} (get_chatflow)
   - Implement POST /api/v1/prediction/{id} (run_prediction)
   - Add authentication header handling

4. Exception handling
   - Create exception hierarchy in client/exceptions.py
   - Add error parsing from Flowise API responses

5. Observability
   - Implement OperationLogger in logging/operation_logger.py
   - Add structured logging format
   - Implement timing context manager

6. Service layer
   - Implement ChatflowService in services/chatflow_service.py
   - Add list_chatflows operation with logging
   - Add get_chatflow operation with logging
   - Add run_prediction operation with logging
   - Implement error translation

7. MCP server
   - Implement server.py with FastMCP
   - Define list_chatflows MCP tool with schema
   - Define get_chatflow MCP tool with schema
   - Define run_prediction MCP tool with schema
   - Wire up to service layer

8. Testing
   - Unit tests for models (validation)
   - Unit tests for FlowiseClient (mocked httpx)
   - Unit tests for ChatflowService (mocked client)
   - Integration test: List chatflows from local Flowise
   - Integration test: Get chatflow details
   - Integration test: Execute chatflow with question
   - Acceptance test: All P1 scenarios from spec.md

**Deliverable:** AI assistants can discover and execute existing Flowise chatflows

---

### Phase 2: Creation (P2 - Create New Chatflows)

**Goal:** Enable AI assistants to create new chatflows from scratch

**Tasks:**
1. Flowise client - Create operation
   - Implement POST /api/v1/chatflows in FlowiseClient
   - Add request body formatting (name, type, flowData, deployed)
   - Add response parsing for created chatflow

2. Input validation
   - Implement validate_flow_data in utils/validators.py
   - Check JSON structure (nodes, edges arrays)
   - Validate required fields present
   - Check flowData size limit (1MB)

3. Service layer
   - Add create_chatflow operation to ChatflowService
   - Validate inputs before API call
   - Log creation with chatflow details
   - Handle creation errors

4. MCP server
   - Define create_chatflow MCP tool with schema
   - Document parameters: name (required), type (default CHATFLOW), flowData (required), deployed (default false)
   - Wire up to service layer

5. Testing
   - Unit test: Validate flowData structure
   - Integration test: Create chatflow and verify in Flowise UI
   - Integration test: Create with invalid flowData (expect error)
   - Integration test: Create when Flowise unavailable (expect error)
   - Acceptance test: All P2 scenarios from spec.md

**Deliverable:** AI assistants can create new chatflows dynamically

---

### Phase 3: Modification (P3 - Update and Deploy Chatflows)

**Goal:** Enable AI assistants to modify and deploy chatflows

**Tasks:**
1. Flowise client - Update operations
   - Implement PUT /api/v1/chatflows/{id} in FlowiseClient
   - Support partial updates (only provided fields)
   - Add request body formatting
   - Add response parsing for updated chatflow

2. Service layer
   - Add update_chatflow operation to ChatflowService
   - Support optional parameters (name, flowData, deployed)
   - Validate only provided fields
   - Log updates with changed fields
   - Add deploy_chatflow operation (convenience wrapper for update with deployed flag)

3. MCP server
   - Define update_chatflow MCP tool with schema
   - All parameters optional except chatflow_id
   - Define deploy_chatflow MCP tool with schema
   - Parameters: chatflow_id (required), deployed (required boolean)

4. Testing
   - Integration test: Update chatflow name
   - Integration test: Update flowData
   - Integration test: Toggle deployment status (false → true → false)
   - Integration test: Partial update (only name)
   - Acceptance test: All P3 scenarios from spec.md

**Deliverable:** AI assistants can iterate on chatflows without recreation

---

### Phase 4: Deletion (P4 - Delete Chatflows)

**Goal:** Enable AI assistants to remove chatflows

**Tasks:**
1. Flowise client - Delete operation
   - Implement DELETE /api/v1/chatflows/{id} in FlowiseClient
   - Handle 404 responses gracefully
   - Parse success confirmation

2. Service layer
   - Add delete_chatflow operation to ChatflowService
   - Log deletion with chatflow_id
   - Handle "already deleted" gracefully

3. MCP server
   - Define delete_chatflow MCP tool with schema
   - Single parameter: chatflow_id (required)
   - Return confirmation message

4. Testing
   - Integration test: Create, then delete chatflow
   - Integration test: Verify deleted chatflow not in list
   - Integration test: Delete non-existent chatflow (expect error)
   - Integration test: Get deleted chatflow (expect not found)
   - Acceptance test: All P4 scenarios from spec.md

**Deliverable:** AI assistants can clean up unused chatflows

---

### Phase 5: Generation (P5 - Generate AgentFlow V2)

**Goal:** Enable AI assistants to generate agent workflows from descriptions

**Tasks:**
1. Flowise client - Generation operation
   - Implement POST /api/v1/agentflowv2-generator/generate in FlowiseClient
   - Request body: {description: string}
   - Parse response: {flowData: string, name: string, description: string}

2. Service layer
   - Add generate_agentflow_v2 operation to ChatflowService
   - Validate description provided
   - Log generation request and result
   - Optionally combine with create_chatflow

3. MCP server
   - Define generate_agentflow_v2 MCP tool with schema
   - Parameter: description (required string)
   - Return generated flowData, name, description

4. Testing
   - Integration test: Generate from description "research agent"
   - Integration test: Generate and create chatflow
   - Integration test: Vague description (verify sensible defaults)
   - Acceptance test: All P5 scenarios from spec.md

**Deliverable:** AI assistants can create complex agents from natural language

---

## Testing Strategy

### Unit Tests

**Purpose:** Test each module in isolation with mocked dependencies

**Coverage:**
- models/chatflow.py: Validation rules, serialization
- utils/validators.py: Input validation edge cases
- client/flowise_client.py: Request formatting, response parsing (mock httpx)
- services/chatflow_service.py: Business logic, error translation (mock client)
- logging/operation_logger.py: Log format, timing accuracy

**Example:**
```python
# Test FlowiseClient.list_chatflows with mocked httpx
@pytest.mark.asyncio
async def test_list_chatflows_success():
    mock_response = [
        {"id": "123", "name": "Test", "type": "CHATFLOW", "deployed": true}
    ]
    with mock_httpx_response(200, mock_response):
        client = FlowiseClient(config)
        result = await client.list_chatflows()
        assert len(result) == 1
        assert result[0].id == "123"
```

### Integration Tests

**Purpose:** Test against real Flowise instance

**Prerequisites:**
- Local Flowise running at http://localhost:3000
- Test API key configured
- Clean test database

**Coverage:**
- Full lifecycle: create → update → execute → delete
- Error scenarios: invalid IDs, malformed data, connection failures
- Concurrency: 5-10 simultaneous operations
- Performance: Verify timing targets met

**Example:**
```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_lifecycle():
    service = ChatflowService(client, logger)

    # Create
    chatflow = await service.create_chatflow(
        name="Test Flow",
        flow_data=VALID_FLOW_DATA
    )
    assert chatflow.id is not None

    # Update
    updated = await service.update_chatflow(
        chatflow.id,
        name="Updated Flow"
    )
    assert updated.name == "Updated Flow"

    # Execute
    result = await service.run_prediction(
        chatflow.id,
        question="test question"
    )
    assert result.text is not None

    # Delete
    await service.delete_chatflow(chatflow.id)

    # Verify deleted
    with pytest.raises(NotFoundError):
        await service.get_chatflow(chatflow.id)
```

### Acceptance Tests

**Purpose:** Verify spec requirements met

**Coverage:** All 18 acceptance scenarios from spec.md user stories

**Format:** Given-When-Then scenarios as executable tests

**Example:**
```python
@pytest.mark.acceptance
@pytest.mark.asyncio
async def test_us1_scenario1():
    """
    User Story 1, Scenario 1:
    Given a Flowise instance with 3 chatflows,
    When AI assistant calls list_chatflows,
    Then all 3 chatflows are returned with names, IDs, types, deployment status
    """
    # Setup: Ensure exactly 3 chatflows exist
    await setup_test_chatflows(count=3)

    # Execute
    chatflows = await service.list_chatflows()

    # Assert
    assert len(chatflows) == 3
    for chatflow in chatflows:
        assert chatflow.id is not None
        assert chatflow.name is not None
        assert chatflow.type in ["CHATFLOW", "AGENTFLOW", "MULTIAGENT", "ASSISTANT"]
        assert isinstance(chatflow.deployed, bool)
```

### Performance Tests

**Purpose:** Verify NFR-006 timing targets

**Tests:**
1. List 100 chatflows completes in <5s (NFR-009)
2. Get single chatflow completes in <5s (SC-002)
3. Execute chatflow completes in <5s (SC-002)
4. Create chatflow completes in <10s (SC-003)
5. Full lifecycle completes in <60s (SC-006)
6. 5-10 concurrent operations meet targets (NFR-006)

**Example:**
```python
@pytest.mark.performance
@pytest.mark.asyncio
async def test_list_performance():
    # Setup: 100 chatflows in Flowise
    await setup_test_chatflows(count=100)

    # Execute with timing
    start = time.time()
    chatflows = await service.list_chatflows()
    duration = time.time() - start

    # Assert
    assert len(chatflows) == 100
    assert duration < 5.0, f"List took {duration}s, expected <5s"
```

---

## Documentation Strategy

### Code Documentation Principles

**Module Docstrings:**
```python
"""
Flowise HTTP client for REST API communication.

This module provides async HTTP client for interacting with Flowise API endpoints.
Handles authentication, request formatting, response parsing, and error handling.

Dependencies:
- httpx for async HTTP operations
- models for domain objects
- exceptions for error hierarchy

Example:
    config = FlowiseConfig.from_env()
    async with FlowiseClient(config) as client:
        chatflows = await client.list_chatflows()
"""
```

**Class Docstrings:**
```python
class ChatflowService:
    """
    Orchestrates chatflow operations with business logic and logging.

    This service layer sits between the MCP server and Flowise client,
    implementing business rules, error translation, and observability.

    Responsibilities:
    - Validate business rules before API calls
    - Translate Flowise errors to user-friendly messages
    - Log operations for observability (NFR-001 to NFR-004)
    - Coordinate domain model conversions

    Example:
        service = ChatflowService(flowise_client, operation_logger)
        chatflow = await service.create_chatflow(name="My Flow", flow_data=data)
    """
```

**Method Docstrings:**
```python
async def create_chatflow(
    self,
    name: str,
    flow_data: str,
    chatflow_type: str = "CHATFLOW",
    deployed: bool = False
) -> Chatflow:
    """
    Create a new chatflow in Flowise.

    Validates inputs, calls Flowise API, and logs the operation.
    The flowData must be a valid JSON string representing the workflow structure.

    Args:
        name: Human-readable chatflow name
        flow_data: JSON string with nodes and edges structure
        chatflow_type: One of CHATFLOW, AGENTFLOW, MULTIAGENT, ASSISTANT
        deployed: Whether chatflow should be immediately deployed

    Returns:
        Created Chatflow object with generated ID

    Raises:
        ValidationError: If flow_data is malformed or exceeds 1MB
        ConnectionError: If Flowise API is unreachable
        AuthenticationError: If API key is invalid

    Example:
        flow_data = json.dumps({"nodes": [...], "edges": [...]})
        chatflow = await service.create_chatflow("My Flow", flow_data)
        print(f"Created chatflow {chatflow.id}")
    """
```

**Inline Comments - Explain WHY:**
```python
# Good: Explains business reason
# Flowise requires flowData as JSON string, not dict object
# This is a quirk of their API design for handling complex nested structures
flow_data_str = json.dumps(flow_data)

# Bad: Restates code
# Convert dict to JSON string
flow_data_str = json.dumps(flow_data)
```

```python
# Good: Explains non-obvious decision
# Retry once on conflict - Flowise may be processing concurrent update
# After one retry, fail fast to avoid blocking AI assistant
if error.status_code == 409:
    await asyncio.sleep(0.5)
    return await self._retry_request(request)

# Bad: Obvious from code
# Sleep for 0.5 seconds and retry
await asyncio.sleep(0.5)
```

### Type Hints Throughout

```python
from typing import Optional, List

async def list_chatflows(self) -> List[Chatflow]:
    """Fetch all chatflows from Flowise."""

async def get_chatflow(self, chatflow_id: str) -> Optional[Chatflow]:
    """Get chatflow by ID, returns None if not found."""

async def create_chatflow(
    self,
    name: str,
    flow_data: str,
    chatflow_type: str = "CHATFLOW",
    deployed: bool = False
) -> Chatflow:
    """Create new chatflow."""
```

---

## Deployment Checklist

### Prerequisites

1. **Python Environment**
   - Python 3.12+ installed
   - pip or poetry for dependency management

2. **Flowise Instance**
   - Flowise v1.x running and accessible
   - API URL reachable from deployment environment
   - API key generated (if instance is secured)

### Installation Steps

1. **Clone and Install**
   ```bash
   cd ~/work/ai/fluent-mind-mcp
   pip install -e .
   ```

2. **Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your values:
   # FLOWISE_API_URL=http://localhost:3000
   # FLOWISE_API_KEY=your_api_key_here
   ```

3. **Verify Flowise Connection**
   ```bash
   python -m fluent_mind_mcp.client.flowise_client --test
   # Should connect and list chatflows
   ```

4. **Claude Desktop Integration**

   Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "fluent-mind": {
         "command": "python",
         "args": ["-m", "fluent_mind_mcp.server"],
         "env": {
           "FLOWISE_API_URL": "http://localhost:3000",
           "FLOWISE_API_KEY": "your_api_key_here"
         }
       }
     }
   }
   ```

5. **Restart Claude Desktop**
   - Quit Claude Desktop completely
   - Relaunch to load new MCP server

### Verification

1. **Health Check**
   - In Claude, ask: "List my Flowise chatflows"
   - Verify chatflows are returned

2. **Performance Validation**
   - List 100 chatflows: Should complete in <5s
   - Create chatflow: Should complete in <10s
   - Execute chatflow: Should complete in <5s

3. **Concurrency Test**
   - Open 5-10 Claude conversations
   - Execute chatflow operations simultaneously
   - Verify all complete without errors

4. **Logging Check**
   - Check logs contain operation entries
   - Verify timing information present
   - Confirm no credentials in logs

### Monitoring

**Log Location:** (Configure in environment)
- Default: stdout/stderr captured by Claude Desktop
- Production: Configure file handler in operation_logger.py

**Key Metrics to Monitor:**
- Operation latency (95th percentile should meet targets)
- Error rate (should be <1% for valid operations)
- Concurrent connections (should stay ≤10)

**Health Indicators:**
- Can connect to Flowise (test list_chatflows)
- Authentication succeeds
- Response times within targets

---

## Success Criteria Mapping

This plan ensures all success criteria from spec.md are met:

| Success Criteria | Implementation |
|------------------|----------------|
| SC-001: AI assistant can discover all 8 operations | server.py defines 8 MCP tools with schemas |
| SC-002: List/get/execute within 5s | Async operations, connection pooling, performance tests |
| SC-003: Create within 10s | Async create operation, performance test |
| SC-004: 100% error handling | Exception hierarchy, validation, error tests |
| SC-005: Maintain connection across operations | HTTP keep-alive, connection pooling |
| SC-006: Full lifecycle within 60s | End-to-end integration test, performance validation |
| SC-007: Clear error messages | Error translation in service layer, user-friendly messages |
| SC-008: Generate and create AgentFlow V2 | Phase 5 implementation, acceptance test |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Flowise API changes | Pin to v1.x, document version compatibility, add version check |
| Performance degradation under load | Connection pooling, async operations, performance tests in CI |
| Authentication leaks in logs | Credential sanitization in logger, security review |
| Malformed flowData crashes system | Input validation before API call, size limits, error handling |
| Concurrent operations conflict | Let Flowise handle conflicts, retry on 409, test concurrency |
| Timeout during long chatflow execution | Configurable timeouts, clear timeout messages, retry guidance |

---

## Open Questions (Deferred to Implementation)

These questions will be answered during implementation based on practical constraints:

1. **Logging Format:** JSON structured logs or human-readable format?
   - Decision: Start with human-readable, add JSON option later if needed

2. **Retry Strategy:** Should we auto-retry on transient failures?
   - Decision: Single retry on 409 conflict, no retry on other errors (fail fast)

3. **Caching:** Should we cache list_chatflows results?
   - Decision: No caching initially (always fresh), add if needed

4. **Rate Limiting:** Should we implement client-side rate limiting?
   - Decision: No client-side limiting, respect Flowise rate limit headers

5. **Metrics:** Should we export metrics beyond logging?
   - Decision: Logging only initially, metrics can be added later

---

## Maintenance Plan

### Version Updates

**When to update Flowise compatibility:**
- When Flowise v2.x is released (breaking changes expected)
- When v1.x API endpoints change
- Test compatibility before updating

**How to update:**
1. Run integration tests against new Flowise version
2. Document any API changes found
3. Update client to handle new/changed endpoints
4. Update version compatibility in config

### Code Quality

**Linting:**
- Run `ruff` on all Python files
- Enforce type hints with `mypy --strict`

**Testing:**
- Run unit tests on every commit
- Run integration tests before release
- Maintain >80% code coverage

**Documentation:**
- Update docstrings when behavior changes
- Keep plan.md in sync with implementation
- Document any deviations from plan

---

## Appendix: API Endpoint Mapping

| MCP Tool | HTTP Method | Flowise Endpoint | Response Time Target |
|----------|-------------|------------------|----------------------|
| list_chatflows | GET | /api/v1/chatflows | 5s |
| get_chatflow | GET | /api/v1/chatflows/{id} | 5s |
| create_chatflow | POST | /api/v1/chatflows | 10s |
| update_chatflow | PUT | /api/v1/chatflows/{id} | 10s |
| delete_chatflow | DELETE | /api/v1/chatflows/{id} | 5s |
| run_prediction | POST | /api/v1/prediction/{id} | 5s |
| deploy_chatflow | PUT | /api/v1/chatflows/{id} | 10s |
| generate_agentflow_v2 | POST | /api/v1/agentflowv2-generator/generate | 10s |

---

**Plan Complete** ✅

This plan provides comprehensive guidance for implementing the Fluent Mind MCP Server following clean code principles. All decisions are traceable to spec requirements and clarifications.
