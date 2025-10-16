# Research: Fluent Mind MCP Server

**Feature**: Fluent Mind MCP Server
**Branch**: `001-flowise-mcp-server`
**Date**: 2025-10-16
**Phase**: Phase 0 - Technical Research

---

## Overview

This document captures research findings and technical decisions for implementing the Fluent Mind MCP Server. All technical context was well-defined from the start, so this phase primarily documents rationale for technology choices and architectural patterns.

---

## Technology Stack Decisions

### 1. MCP Framework: FastMCP

**Decision**: Use FastMCP as the MCP server framework

**Rationale**:
- Modern Python MCP framework with active development
- Built-in async/await support for non-blocking operations
- Simple, declarative tool definition syntax
- Type-safe parameter validation via Pydantic integration
- Well-documented with examples
- Used by other successful MCP servers

**Alternatives Considered**:
- **mcp-python** (official SDK): More low-level, requires more boilerplate
- **Custom implementation**: Too much effort, reinventing wheel

**References**:
- FastMCP documentation: https://github.com/jlowin/fastmcp
- MCP protocol spec: https://modelcontextprotocol.io/

---

### 2. HTTP Client: httpx

**Decision**: Use httpx for async HTTP communication with Flowise API

**Rationale**:
- Native async/await support (required for FR-015)
- Connection pooling out of the box
- Timeout configuration per-request and client-wide
- Well-maintained, widely adopted in Python ecosystem
- Familiar requests-like API
- Excellent performance for concurrent operations

**Alternatives Considered**:
- **aiohttp**: More complex API, less intuitive
- **requests**: Synchronous only, doesn't meet non-blocking requirement

**Configuration**:
```python
httpx.AsyncClient(
    base_url=config.api_url,
    timeout=config.timeout,  # Default 60s
    limits=httpx.Limits(
        max_connections=10,     # NFR-005: 5-10 concurrent
        max_keepalive_connections=5
    )
)
```

**References**:
- httpx documentation: https://www.python-httpx.org/
- Async best practices: https://www.python-httpx.org/async/

---

### 3. Data Validation: Pydantic

**Decision**: Use Pydantic v2 for data modeling and validation

**Rationale**:
- Type-safe data validation with Python type hints
- JSON serialization/deserialization built-in
- Integration with FastMCP for tool parameters
- Excellent error messages for validation failures
- Performance optimized (Rust core in v2)
- Industry standard for Python data validation

**Alternatives Considered**:
- **dataclasses**: No validation, just structure
- **attrs**: Less ecosystem integration
- **marshmallow**: More verbose, less type-safe

**Key Models**:
- `FlowiseConfig`: Environment-based configuration
- `Chatflow`: Domain model for Flowise workflows
- `FlowData`: Workflow graph structure (nodes, edges)
- Custom validators for chatflow IDs, flowData structure

**References**:
- Pydantic v2 documentation: https://docs.pydantic.dev/latest/
- Validation patterns: https://docs.pydantic.dev/latest/concepts/validators/

---

### 4. Testing: pytest + pytest-asyncio

**Decision**: Use pytest with pytest-asyncio plugin for all test types

**Rationale**:
- De facto standard for Python testing
- Excellent async test support via pytest-asyncio
- Rich plugin ecosystem (coverage, mock, fixtures)
- Parametrized tests for multiple scenarios
- Clear, readable test syntax
- Fast test execution (<100ms unit, <5s integration targets)

**Test Structure**:
- **Unit tests**: Mocked dependencies, isolated, <100ms each
- **Integration tests**: Against local Flowise, <5s each
- **Acceptance tests**: Based on spec.md scenarios, end-to-end

**Alternatives Considered**:
- **unittest**: More verbose, less Pythonic
- **nose**: Less actively maintained

**References**:
- pytest documentation: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

---

## Architecture Patterns

### 1. Layered Architecture (4 Layers)

**Decision**: Implement clean 4-layer architecture

**Layers**:
1. **MCP Server Interface** (server.py)
   - MCP protocol handling
   - Tool definitions and schemas
   - Parameter validation
   - Response formatting

2. **Service/Business Logic** (services/)
   - Business rule enforcement
   - Error translation
   - Operation orchestration
   - Logging coordination

3. **Flowise Client** (client/)
   - HTTP communication
   - Request/response formatting
   - Authentication handling
   - Timeout management

4. **Domain Models** (models/)
   - Data structures
   - Validation rules
   - Serialization logic

**Rationale**:
- Clear separation of concerns
- Each layer has single responsibility
- Easy to test (mock one layer, test another)
- No implementation details leak across boundaries
- Business logic independent of MCP or HTTP details

**Pattern References**:
- Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Hexagonal Architecture: https://alistair.cockburn.us/hexagonal-architecture/

---

### 2. Error Handling Strategy

**Decision**: Custom exception hierarchy with translation at service layer

**Exception Hierarchy**:
```
FlowiseClientError (base)
├── ConnectionError (network, timeout)
├── AuthenticationError (invalid API key)
├── ValidationError (malformed data, invalid IDs)
├── NotFoundError (chatflow doesn't exist)
├── RateLimitError (Flowise throttling)
└── UnexpectedError (catch-all)
```

**Translation Flow**:
1. **Client Layer**: Raises specific exceptions with HTTP details
2. **Service Layer**: Catches, logs, translates to user-friendly messages
3. **Server Layer**: Converts to MCP error responses with guidance

**Rationale**:
- AI assistants get actionable error messages (SC-007)
- Internal debugging via detailed logs (NFR-001)
- Consistent error handling across all operations
- Easy to add new error types
- Clear separation between technical errors and user messages

**Pattern References**:
- Exception hierarchy best practices: https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

---

### 3. Async/Await Throughout

**Decision**: Use async/await at all levels for non-blocking operations

**Implementation**:
- All I/O operations async (HTTP requests, file I/O if any)
- Service methods async
- MCP tool handlers async
- No synchronous blocking calls in hot path

**Rationale**:
- Meets FR-015 (non-blocking operations)
- Supports NFR-005 to NFR-007 (5-10 concurrent operations)
- Connection pooling works efficiently with async
- Better resource utilization
- Consistent programming model throughout stack

**Pattern References**:
- Python asyncio: https://docs.python.org/3/library/asyncio.html
- Async patterns: https://realpython.com/async-io-python/

---

### 4. Observability via Structured Logging

**Decision**: Implement OperationLogger with structured logging

**Log Entry Format**:
```json
{
  "timestamp": "2025-10-16T12:34:56Z",
  "level": "INFO",
  "operation": "create_chatflow",
  "chatflow_id": "abc123",
  "duration_ms": 234,
  "status": "success",
  "message": "Created chatflow 'My Flow'"
}
```

**Log Levels** (from Clarifications):
- **ERROR**: All failures with context (NFR-001)
- **INFO**: Key operations (create, update, delete, execute) with IDs (NFR-002)
- **WARNING**: Degraded conditions (slow responses, retries, connection issues) (NFR-004)
- **DEBUG**: Detailed traces (off by default)

**Context Manager for Timing** (NFR-003):
```python
with operation_logger.time_operation("create_chatflow", chatflow_id):
    result = await flowise_client.create(...)
```

**Rationale**:
- Meets all observability NFRs (NFR-001 to NFR-004)
- Structured format parseable by log aggregators
- Easy to search and filter
- Timing automatically captured
- No credential leakage (NFR-012)

**Pattern References**:
- Python logging: https://docs.python.org/3/library/logging.html
- Structured logging: https://www.structlog.org/

---

## Configuration Management

### Decision: Environment Variables via Pydantic Settings

**Implementation**:
```python
class FlowiseConfig(BaseSettings):
    api_url: str                    # FLOWISE_API_URL
    api_key: Optional[str] = None   # FLOWISE_API_KEY
    timeout: int = 60               # FLOWISE_TIMEOUT
    max_connections: int = 10       # FLOWISE_MAX_CONNECTIONS
    log_level: str = "INFO"         # LOG_LEVEL

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

**Rationale**:
- Type-safe configuration with validation
- Environment variables for deployment flexibility
- `.env` file for local development
- Sensible defaults for optional values
- Validation at startup (fail fast)

**References**:
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- 12-Factor App: https://12factor.net/config

---

## Concurrency Strategy

### Decision: Connection Pooling with Async HTTP

**Configuration**:
- Max connections: 10 (matches 5-10 concurrent target from NFR-005)
- Keep-alive connections: 5
- Request timeout: 60s (configurable)
- Connection timeout: 30s

**Rationale**:
- Meets NFR-005 to NFR-007 (5-10 concurrent operations)
- Connection reuse reduces latency
- Timeout prevents hung operations
- No global state (thread-safe)
- Scales within small team deployment constraints

**Pattern References**:
- httpx connection pooling: https://www.python-httpx.org/advanced/#pool-limit-configuration
- Async concurrency patterns: https://docs.python.org/3/library/asyncio-task.html

---

## Data Volume Strategy

### Decision: No Caching, No Pagination

**Implementation**:
- `list_chatflows()` returns all chatflows in single response
- No in-memory caching of chatflow data
- Flowise API is single source of truth

**Rationale**:
- Up to 100 chatflows fits easily in single response (NFR-008)
- Fresh data on every request (no stale cache issues)
- Simpler implementation (no cache invalidation)
- Meets 5s performance target for list operations (NFR-009)
- Reduces complexity and potential bugs

**Future Considerations**:
- If catalog grows >100 chatflows, add pagination
- If performance degrades, add short-lived caching (30s TTL)

---

## Security Decisions

### 1. Authentication Only (No Authorization)

**Decision**: All authenticated users have full permissions (from Clarifications)

**Implementation**:
- API key passed in every request to Flowise
- No user/role management in MCP server
- Flowise handles its own authentication

**Rationale**:
- Small team deployment (5-10 users)
- Trust model: if you have API key, you're trusted
- Simpler implementation
- Can add authorization later if needed

**Security Measures**:
- Credentials never logged (NFR-012)
- API key stored in environment variables (not code)
- HTTPS recommended for Flowise API (not enforced)

---

### 2. Input Validation

**Decision**: Validate all inputs before Flowise API calls

**Validation Points**:
1. **Chatflow IDs**: Format validation (regex or UUID check)
2. **FlowData**: JSON structure validation, size limit (1MB)
3. **Chatflow Type**: Enum validation (CHATFLOW, AGENTFLOW, MULTIAGENT, ASSISTANT)
4. **Required Fields**: Presence checks

**Rationale**:
- Fail fast with clear error messages
- Prevent malformed requests to Flowise
- Security: reject oversized or malicious inputs
- Better user experience (immediate feedback)

**Pattern References**:
- OWASP Input Validation: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

---

## Flowise API Compatibility

### Decision: Target Flowise v1.x Current Stable (from Clarifications)

**Version Strategy**:
- Develop against Flowise v1.x latest release
- No backward compatibility with older v1.x versions
- No v2.x support until released and stable

**Compatibility Checks**:
- Document Flowise version in README
- Add version check at startup (optional)
- Integration tests against specific version

**Future Strategy**:
- When Flowise v2.x releases, evaluate API changes
- Update client layer to handle v2.x endpoints
- Consider version detection and multi-version support

---

## Open Decisions (Deferred to Implementation)

These questions will be answered during implementation:

1. **Logging Format**: JSON structured logs or human-readable?
   - **Proposed**: Start with human-readable, add JSON option later

2. **Retry Strategy**: Auto-retry on transient failures?
   - **Proposed**: Single retry on 409 conflict, no retry on other errors (fail fast)

3. **Rate Limiting**: Client-side rate limiting?
   - **Proposed**: No client-side limiting, respect Flowise rate limit headers

4. **Metrics Export**: Beyond logging?
   - **Proposed**: Logging only initially, metrics can be added later

5. **Connection Keep-Alive Duration**: How long to keep connections open?
   - **Proposed**: Default httpx behavior (likely 5 minutes)

---

## References

### Official Documentation
- **MCP Protocol**: https://modelcontextprotocol.io/
- **FastMCP**: https://github.com/jlowin/fastmcp
- **httpx**: https://www.python-httpx.org/
- **Pydantic**: https://docs.pydantic.dev/
- **pytest**: https://docs.pytest.org/
- **Flowise**: https://github.com/FlowiseAI/Flowise

### Best Practices
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **Python Async**: https://realpython.com/async-io-python/
- **Testing Best Practices**: https://docs.python-guide.org/writing/tests/
- **12-Factor App**: https://12factor.net/

### Project-Specific
- **Feature Spec**: [spec.md](spec.md)
- **Clean Code Plan**: [plan_cc.md](plan_cc.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)

---

**Research Complete**: ✅

All technical decisions documented. Ready to proceed to Phase 1 (Design & Contracts).
