# Architecture Overview

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: Architecture overview, design principles, project structure

---

## Architecture Overview

### 4-Layer Clean Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: MCP Server (server.py)                             │
│ - 8 MCP Tools for AI assistant interaction                  │
│ - Token-efficient interfaces (<150 tokens per workflow)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Service Layer (services/)                          │
│ - Business logic with validation                            │
│ - Circuit breaker integration                               │
│ - Structured logging with credential masking                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Client Layer (client/)                             │
│ - FlowiseApiClient (HTTP with connection pooling)           │
│ - VectorDatabaseClient (ChromaDB operations)                │
│ - EmbeddingClient (sentence-transformers wrapper)           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Models Layer (models/)                             │
│ - Pydantic models for type safety                           │
│ - Request/response validation                               │
│ - Clear contracts between layers                            │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles Applied

- **Single Responsibility**: Each service handles one domain
- **Dependency Injection**: Services receive dependencies via constructor
- **Interface Segregation**: Services expose minimal, focused interfaces
- **Open/Closed**: Services open for extension via composition
- **Clean Code**: WHY-focused comments, readable structure, testable logic

---

## Project Structure

```
src/fluent_mind_mcp/
├── server.py                       # MCP Server with 8 tools
├── models/
│   ├── node_models.py             # NodeMetadata, NodeSummary
│   ├── template_models.py         # FlowTemplate, TemplateSummary
│   ├── workflow_models.py         # ComplexityAnalysis, WorkflowResponse
│   └── common_models.py           # ChatflowResponse, Edge, RefreshResult
├── services/
│   ├── vector_service.py          # Vector search for nodes/templates
│   ├── build_flow_service.py      # Chatflow creation logic
│   ├── node_catalog_service.py    # Dynamic node catalog refresh
│   ├── workflow_service.py        # Spec-driven workflow orchestration
│   └── circuit_breaker_service.py # Failure resilience
├── client/
│   ├── flowise_client.py          # Flowise API integration
│   ├── vector_db_client.py        # ChromaDB operations
│   └── embedding_client.py        # Sentence-transformers wrapper
└── utils/
    ├── logging.py                 # Credential masking formatter
    └── exceptions.py              # Custom exception hierarchy

tests/
├── checklists/                    # Manual test checklists (7 stories)
│   ├── user_story_1_checklist.md
│   ├── user_story_2_checklist.md
│   └── ...
├── critical_paths/                # Automated critical path tests
│   ├── test_vector_search_accuracy.py
│   ├── test_build_flow_creation.py
│   └── test_circuit_breaker_transitions.py
├── utilities/                     # Test data generators and utilities
│   ├── test_data_generator.py
│   └── test_utilities.py
└── integration/                   # End-to-end integration tests
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 1 MCP Server →](02-layer1-mcp-server.md)
