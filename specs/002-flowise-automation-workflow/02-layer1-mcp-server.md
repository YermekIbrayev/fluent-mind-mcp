# Layer 1: MCP Server Tools

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: 8 MCP tools for token-efficient automation

---

## 8 MCP Tools for Token-Efficient Automation

```python
# src/fluent_mind_mcp/server.py

@mcp.tool()
async def vector_search_nodes(
    query: str,
    category: Optional[str] = None,
    limit: int = 5
) -> List[NodeSummary]:
    """
    Search vector DB for relevant Flowise nodes using natural language.

    WHY: Enables AI to discover nodes without loading full catalog (50 tokens vs. 5000+)
    TOKEN BUDGET: Query <30 tokens, results <150 tokens total
    """
    pass

@mcp.tool()
async def search_templates(
    query: str,
    limit: int = 3
) -> List[TemplateSummary]:
    """
    Search vector DB for pre-built flow templates.

    WHY: Pattern discovery without token overhead for full flowData
    TOKEN BUDGET: Query <30 tokens, results <150 tokens total
    """
    pass

@mcp.tool()
async def build_flow(
    template_id: Optional[str] = None,
    nodes: Optional[List[str]] = None,
    connections: str = "auto",
    **parameters
) -> ChatflowResponse:
    """
    Create chatflow from template or node list.

    WHY: Single function interface minimizes tokens (20-50 tokens vs. 1000+ for manual flowData)
    CONNECTION INFERENCE: Type-compatible chain algorithm when connections="auto"
    NODE POSITIONING: Left-to-right flow pattern (200px vertical, 300px horizontal spacing)
    """
    pass

@mcp.tool()
async def refresh_node_catalog(force: bool = False) -> RefreshResult:
    """
    Update node catalog from Flowise server.

    WHY: Ensures AI works with latest node versions and deprecation status
    TRIGGER: On-demand lazy loading (checks staleness >24h before build_flow)
    """
    pass

@mcp.tool()
async def spec_driven_workflow(user_request: str) -> WorkflowResponse:
    """
    Execute spec-driven workflow for complex chatflow requests.

    WHY: Complex/novel flows need human validation before implementation
    PHASES: specify → clarify (max 5 questions) → plan → tasks → analyze → approve
    """
    pass

# Existing tools from 001-flowise-mcp-server
@mcp.tool()
async def list_chatflows() -> List[ChatflowSummary]:
    """List all chatflows from Flowise server"""
    pass

@mcp.tool()
async def get_chatflow(id: str) -> ChatflowDetail:
    """Get detailed chatflow information"""
    pass

@mcp.tool()
async def run_prediction(id: str, question: str) -> PredictionResult:
    """Execute chatflow with user input"""
    pass
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 2 Vector Search Service →](03-layer2-vector-search-service.md)
