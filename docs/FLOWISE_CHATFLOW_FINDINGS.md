# Flowise Chatflow Creation - Critical Findings

**Date**: 2025-10-17
**Context**: Building AI Web Assistant and discovering why programmatically created chatflows fail

---

## The Problem

When creating Flowise chatflows programmatically, they would be created successfully but fail at runtime with:

```
Error: predictionsServices.buildChatflow - Expected a Runnable, function or object.
Instead got an unsupported type.
```

## Root Causes Discovered

### 1. **CRITICAL: `node.id` Must Match `node.data.id`**

**The Bug:**
```python
node['id'] = 'my_custom_id'  # Changed
node['data']['id'] = 'template_0'  # NOT changed - still has template ID
```

**Result:** Flowise can't resolve node references, chatflow fails.

**The Fix:**
```python
def update_node_id(node, new_id):
    node['id'] = new_id
    node['data']['id'] = new_id  # CRITICAL: Must match!
```

**Verification:**
```python
# Working flow (copied from Flowise):
node.id: chatOpenAI_0 | data.id: chatOpenAI_0 ✓

# My broken flow:
node.id: llm | data.id: chatOpenAI_0 ✗ MISMATCH!
```

---

### 2. Edge Format Requirements

**Working Edge Structure:**
```json
{
  "source": "chatOpenAI_0",
  "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|...",
  "target": "conversationChain_0",
  "targetHandle": "conversationChain_0-input-model-BaseChatModel",
  "type": "buttonedge",
  "id": "chatOpenAI_0-chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|...-conversationChain_0-conversationChain_0-input-model-BaseChatModel"
}
```

**Requirements:**
1. `type`: Must be `"buttonedge"`
2. `id`: Format is `{source}-{sourceHandle}-{target}-{targetHandle}`
3. `sourceHandle`: Must exactly match an anchor ID from source node's `outputAnchors`
4. `targetHandle`: Must exactly match an anchor ID from target node's `inputAnchors`

---

### 3. Options-Type Anchors

Some nodes (e.g., `cheerioWebScraper`, `memoryVectorStore`) have special "options" type output anchors:

```json
{
  "outputAnchors": [{
    "name": "output",
    "type": "options",
    "options": [
      {
        "id": "nodeId-output-document-Document|json",
        "name": "document"
      },
      {
        "id": "nodeId-output-text-string|json",
        "name": "text"
      }
    ]
  }]
}
```

**Issue:** When updating node ID, the option IDs must also be updated:

```python
# Update output anchors
for anchor in node['data'].get('outputAnchors', []):
    if 'id' in anchor:
        anchor['id'] = anchor['id'].replace(old_id, new_id, 1)

    # Handle options-type anchors
    if anchor.get('type') == 'options' and 'options' in anchor:
        for option in anchor['options']:
            if 'id' in option:
                option['id'] = option['id'].replace(old_id, new_id, 1)
```

---

### 4. Node Input References

Nodes reference other nodes via `{{nodeId.data.instance}}` format:

```json
{
  "data": {
    "inputs": {
      "model": "{{chatOpenAI_0.data.instance}}",
      "vectorStoreRetriever": "{{memoryVectorStore_0.data.instance}}"
    }
  }
}
```

**Issue:** References must use the actual node ID, not template ID.

**Wrong:**
```json
{
  "id": "my_llm",
  "data": {
    "inputs": {
      "model": "{{chatOpenAI_0.data.instance}}"  // ✗ Wrong reference!
    }
  }
}
```

**Correct:**
```json
{
  "id": "my_llm",
  "data": {
    "inputs": {
      "model": "{{my_llm.data.instance}}"  // ✓ Matches node ID
    }
  }
}
```

---

### 5. Document Input Arrays

Vector stores expect document inputs as arrays:

```json
{
  "inputs": {
    "document": ["{{cheerioWebScraper_0.data.instance}}"],  // Note: array!
    "embeddings": "{{openAIEmbeddings_0.data.instance}}"     // Not array
  }
}
```

---

## Complete Node Update Checklist

When changing a node's ID from template to custom:

- [ ] Update `node.id`
- [ ] Update `node.data.id` (CRITICAL!)
- [ ] Update all `outputAnchors[].id`
- [ ] Update all `outputAnchors[].options[].id` (for options-type)
- [ ] Update all `inputAnchors[].id`
- [ ] Update all `inputAnchors[].options[].id` (for options-type)
- [ ] Update all `inputParams[].id`
- [ ] Update all input references in dependent nodes

---

## Verification Method

**The ONLY reliable verification is runtime testing:**

```python
# Create chatflow
response = httpx.post(f'{api_url}/api/v1/chatflows', json=chatflow_data)
chatflow_id = response.json()['id']

# TEST IT!
response = httpx.post(
    f'{api_url}/api/v1/prediction/{chatflow_id}',
    json={"question": "Hello"}
)

if response.status_code == 200:
    print("✓ Chatflow works!")
else:
    print(f"✗ Failed: {response.text}")
```

**Don't trust:**
- ✗ Edge handle verification (can pass but chatflow still fails)
- ✗ Anchor ID matching (can pass but chatflow still fails)
- ✗ Flowise UI showing connections (visual can be misleading)

**Only trust:**
- ✓ Actual chat prediction succeeding

---

## Working Example

Copy a working flow and modify it:

```python
# Load working flow
with open('working_flow.json') as f:
    working = json.load(f)

# Create as new chatflow
working['name'] = "My Copy"
del working['id']  # Remove to create new

# Post to API
response = httpx.post(f'{api_url}/api/v1/chatflows', json=working)
new_id = response.json()['id']

# Test
response = httpx.post(
    f'{api_url}/api/v1/prediction/{new_id}',
    json={"question": "Test"}
)
# ✓ Works because structure is exactly like working flow
```

---

## Helper Function (Fixed)

```python
def update_node_id(node: Dict[str, Any], new_id: str) -> Dict[str, Any]:
    """Update node ID and ALL related IDs."""
    old_id = node['id']

    # Update node IDs
    node['id'] = new_id
    node['data']['id'] = new_id  # CRITICAL!

    # Update output anchors
    for anchor in node['data'].get('outputAnchors', []):
        if 'id' in anchor:
            anchor['id'] = anchor['id'].replace(old_id, new_id, 1)
        # Handle options-type anchors
        if anchor.get('type') == 'options' and 'options' in anchor:
            for option in anchor['options']:
                if 'id' in option:
                    option['id'] = option['id'].replace(old_id, new_id, 1)

    # Update input anchors
    for anchor in node['data'].get('inputAnchors', []):
        if 'id' in anchor:
            anchor['id'] = anchor['id'].replace(old_id, new_id, 1)
        if anchor.get('type') == 'options' and 'options' in anchor:
            for option in anchor['options']:
                if 'id' in option:
                    option['id'] = option['id'].replace(old_id, new_id, 1)

    # Update input params
    for param in node['data'].get('inputParams', []):
        if 'id' in param:
            param['id'] = param['id'].replace(old_id, new_id, 1)

    return node
```

---

## Lessons Learned

1. **Visual verification is NOT enough** - edges can look connected in UI but fail at runtime
2. **Flowise requires exact ID consistency** - `node.id` must match `node.data.id`
3. **Always test with actual predictions** - it's the only reliable verification
4. **Options-type anchors are tricky** - they have nested IDs that must be updated
5. **Copy working flows when possible** - safest approach for complex chatflows

---

## Files Updated

- `examples/node_templates/node_builder.py` - Fixed `update_node_id()` to update `data.id`
- `docs/PORT_CONNECTIONS_GUIDE.md` - Complete guide on port connections
- `examples/working_flows/*.json` - 15 real working flows for reference

---

## Next Steps

1. ✓ Fix `update_node_id()` to update `data.id`
2. ✓ Update helper functions to support options-type anchors
3. ⏳ Recreate AI Web Assistant with all fixes
4. ⏳ Test with actual chat predictions
5. ⏳ Document working solution

---

**Status**: Root cause identified - `node.id` vs `node.data.id` mismatch
**Priority**: CRITICAL - This breaks ALL programmatically created chatflows
