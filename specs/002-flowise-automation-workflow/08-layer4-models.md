# Layer 4: Models Layer

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: Pydantic models for type safety

---

## Pydantic Models for Type Safety

```python
# models/node_models.py
class NodeMetadata(BaseModel):
    """Complete metadata for Flowise node type from API"""
    name: str  # e.g., "chatOpenAI"
    label: str  # e.g., "ChatOpenAI"
    version: str
    category: str
    base_classes: List[str]
    description: str
    deprecated: bool = False

class NodeSummary(BaseModel):
    """Compact node summary for AI consumption (<30 tokens)"""
    name: str
    description: str  # One-line
    primary_use_case: str
    relevance_score: float = Field(ge=0.0, le=1.0)

# models/template_models.py
class FlowTemplate(BaseModel):
    """Pre-built chatflow template with full flowData"""
    template_id: str
    name: str
    description: str
    required_nodes: List[str]
    flow_data: Dict  # Complete flowData structure
    created_at: datetime
    metadata: Dict

class TemplateSummary(BaseModel):
    """Compact template summary for AI (<50 tokens)"""
    template_id: str
    name: str
    description: str
    required_nodes: List[str]  # Not full flowData
    relevance_score: float

# models/workflow_models.py
class ComplexityAnalysis(BaseModel):
    """Analysis of request complexity for routing"""
    requires_spec_driven: bool
    confidence_score: float
    reasoning: str

class WorkflowResponse(BaseModel):
    """Response from spec-driven workflow"""
    design: str  # Text-based chatflow design
    awaiting_approval: bool
    token_usage: int

# models/common_models.py
class ChatflowResponse(BaseModel):
    """Response from chatflow creation"""
    chatflow_id: str
    name: str

class Edge(BaseModel):
    """Connection between nodes in flowData"""
    source: str
    target: str
    sourceHandle: str
    targetHandle: str

class RefreshResult(BaseModel):
    """Result of node catalog refresh"""
    refreshed: bool
    reason: Optional[str] = None
    error: Optional[str] = None
    fallback: bool = False
    warning: Optional[str] = None
    changes: Optional[Dict] = None
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Error Handling & Logging →](09-error-logging.md)
