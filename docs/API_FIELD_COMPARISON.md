# Flowise API Field Comparison

**Date**: 2025-10-17
**Source**: Direct API inspection of Flowise instance at http://192.168.51.32:3000

---

## Summary

This document compares the **documented** Chatflow model fields vs **actual** Flowise API responses.

### Key Issues Found

1. **Field Naming Convention**: Documentation uses `snake_case` but API returns `camelCase`
2. **Missing Fields**: Several optional fields not documented
3. **Field Name Mismatches**: Some fields have incorrect names

---

## Chatflow Entity Comparison

### List Chatflows: `GET /api/v1/chatflows`

**Actual API Response Fields** (from real Flowise instance):

```json
{
  "id": "edfd6c70-1860-4c17-8a02-68617f2d4767",
  "name": "Google Calendar",
  "flowData": "{\"nodes\":[...], \"edges\":[...]}",
  "deployed": false,
  "isPublic": false,
  "apikeyid": null,
  "chatbotConfig": null,
  "apiConfig": null,
  "analytic": null,
  "speechToText": null,
  "textToSpeech": null,
  "followUpPrompts": null,
  "category": null,
  "type": "CHATFLOW",
  "createdDate": "2025-10-12T22:56:27.000Z",
  "updatedDate": "2025-10-14T04:11:03.000Z",
  "workspaceId": "60074b37-ae63-4b66-ac73-e13b79b3a7f7"
}
```

**All Unique Fields Across All Chatflows**:
- `analytic`
- `apiConfig`
- `apikeyid`
- `category`
- `chatbotConfig`
- `createdDate`
- `deployed`
- `flowData`
- `followUpPrompts`
- `id`
- `isPublic`
- `name`
- `speechToText`
- `textToSpeech`
- `type`
- `updatedDate`
- `workspaceId`

---

## Field-by-Field Comparison

| Documented Field | Actual API Field | Status | Notes |
|------------------|------------------|--------|-------|
| `id` | `id` | ✅ Match | - |
| `name` | `name` | ✅ Match | - |
| `type` | `type` | ✅ Match | - |
| `deployed` | `deployed` | ✅ Match | - |
| `is_public` | `isPublic` | ❌ **Wrong Name** | Should be `isPublic` (camelCase) |
| `flow_data` | `flowData` | ❌ **Wrong Name** | Should be `flowData` (camelCase) |
| `chatbot_config` | `chatbotConfig` | ❌ **Wrong Name** | Should be `chatbotConfig` (camelCase) |
| `api_config` | `apiConfig` | ❌ **Wrong Name** | Should be `apiConfig` (camelCase) |
| `created_date` | `createdDate` | ❌ **Wrong Name** | Should be `createdDate` (camelCase) |
| `updated_date` | `updatedDate` | ❌ **Wrong Name** | Should be `updatedDate` (camelCase) |
| - | `apikeyid` | ❌ **Missing** | Not documented |
| - | `analytic` | ❌ **Missing** | Not documented |
| - | `speechToText` | ❌ **Missing** | Not documented |
| - | `textToSpeech` | ❌ **Missing** | Not documented |
| - | `followUpPrompts` | ❌ **Missing** | Not documented |
| - | `category` | ⚠️ **Documented as Optional** | Present in API |
| - | `workspaceId` | ❌ **Missing** | Not documented |

---

## FlowData Structure

**Actual API Response** (parsed from `flowData` JSON string):

```json
{
  "nodes": [
    {
      "id": "toolAgent_0",
      "position": {"x": 1473.43, "y": 175.32},
      "type": "customNode",
      "data": {
        "label": "Tool Agent",
        "name": "toolAgent",
        "version": 2,
        "type": "AgentExecutor",
        "category": "Agents",
        "icon": "/path/to/icon.png",
        "description": "Agent description",
        "baseClasses": ["AgentExecutor", "BaseChain", "Runnable"],
        "inputs": {...},
        "filePath": "/path/to/file.js",
        "inputAnchors": [...],
        "inputParams": [...],
        "outputs": {},
        "outputAnchors": [...]
      },
      "width": 300,
      "height": 492,
      "selected": false,
      "positionAbsolute": {"x": 1473.43, "y": 175.32},
      "dragging": false
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "target": "node-2"
    }
  ],
  "viewport": {
    "x": 0,
    "y": 0,
    "zoom": 1
  }
}
```

**FlowData Additional Fields**:
- `viewport` - Not documented (UI viewport state)

**Node Additional Fields**:
- `width` - Not documented
- `height` - Not documented
- `selected` - Not documented
- `positionAbsolute` - Not documented
- `dragging` - Not documented

---

## Chatflow Types

**Documented**:
```python
class ChatflowType(str, Enum):
    CHATFLOW = "CHATFLOW"
    AGENTFLOW = "AGENTFLOW"
    MULTIAGENT = "MULTIAGENT"
    ASSISTANT = "ASSISTANT"
```

**Actual API Values Found**:
- `CHATFLOW` - ✅ Confirmed (4 instances)
- `AGENTFLOW` - ✅ Confirmed (6 instances)
- `MULTIAGENT` - ⚠️ Not found in test data
- `ASSISTANT` - ⚠️ Not found in test data

**Additional Types Found**:
- None (only CHATFLOW and AGENTFLOW present)

---

## Required Changes

### 1. Update Chatflow Model

**Change snake_case to camelCase for API compatibility**:

```python
class Chatflow(BaseModel):
    """Flowise chatflow model matching actual API responses."""

    # Core fields
    id: str
    name: str
    type: ChatflowType
    deployed: bool

    # Optional fields (camelCase to match API)
    isPublic: Optional[bool] = None  # Changed from is_public
    flowData: Optional[str] = None   # Changed from flow_data
    chatbotConfig: Optional[str] = None  # Changed from chatbot_config
    apiConfig: Optional[str] = None  # Changed from api_config
    createdDate: Optional[datetime] = None  # Changed from created_date
    updatedDate: Optional[datetime] = None  # Changed from updated_date

    # Missing fields (now added)
    apikeyid: Optional[str] = None
    analytic: Optional[str] = None
    speechToText: Optional[str] = None
    textToSpeech: Optional[str] = None
    followUpPrompts: Optional[str] = None
    category: Optional[str] = None
    workspaceId: Optional[str] = None

    class Config:
        populate_by_name = True  # Allow both snake_case and camelCase
```

### 2. Update FlowData Model

```python
class FlowData(BaseModel):
    """Workflow graph structure."""

    nodes: List[Node] = []
    edges: List[Edge] = []
    viewport: Optional[Dict[str, Any]] = None  # Added missing field
```

### 3. Update Node Model

```python
class Node(BaseModel):
    """Workflow component node."""

    id: str
    type: str
    data: Dict[str, Any]
    position: Optional[Dict[str, float]] = None

    # UI-specific fields (added)
    width: Optional[int] = None
    height: Optional[int] = None
    selected: Optional[bool] = None
    positionAbsolute: Optional[Dict[str, float]] = None
    dragging: Optional[bool] = None
```

---

## Testing Evidence

**Total Chatflows Tested**: 20 chatflows
- 4 x CHATFLOW type
- 6 x AGENTFLOW type
- 10 x Other types (not categorized)

**Sample Chatflow Names**:
1. Google Calendar (CHATFLOW)
2. Researcher (AGENTFLOW)
3. Various other flows

**API Endpoints Tested**:
- ✅ `GET /api/v1/chatflows` - List all chatflows
- ✅ `GET /api/v1/chatflows/{id}` - Get specific chatflow

---

## Migration Impact

### Code Changes Required

1. **Models** (`src/fluent_mind_mcp/models/chatflow.py`):
   - Change all field names from snake_case to camelCase
   - Add 7 missing optional fields
   - Add field aliases for backward compatibility

2. **Services** (`src/fluent_mind_mcp/services/`):
   - Update field access from `chatflow.flow_data` to `chatflow.flowData`
   - Update all field references

3. **Tests** (`tests/`):
   - Update test fixtures with correct field names
   - Add tests for new fields

### Breaking Changes

**API Compatibility**:
- Using snake_case field names will break deserialization from Flowise API
- Need to use camelCase or add field aliases

**Backward Compatibility**:
- Use Pydantic's `Field(alias=...)` for both naming conventions
- Allow population by name for flexibility

---

## Recommendations

### Immediate Actions

1. ✅ **Document actual API structure** (this document)
2. ⏳ **Update data-model.md** with correct field names
3. ⏳ **Update Pydantic models** to match API responses
4. ⏳ **Run full test suite** to verify compatibility

### Long-term Actions

1. Add integration tests that verify against live Flowise API
2. Document API version compatibility (currently tested with Flowise v1.x)
3. Add API contract validation tests
4. Consider creating API client wrapper for field name translation

---

## References

- **Data Model Doc**: [data-model.md](../specs/001-flowise-mcp-server/data-model.md)
- **Flowise Instance**: http://192.168.51.32:3000
- **API Version**: v1 (inferred from URL paths)
- **Test Date**: 2025-10-17

---

**Status**: ✅ Analysis Complete - Ready for Model Updates
