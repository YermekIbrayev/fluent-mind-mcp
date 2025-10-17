# How to Connect Nodes in Flowise - Complete Guide

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

A practical guide for AI assistants and developers on creating valid connections between Flowise nodes programmatically.

---

## Table of Contents

1. [Understanding Node Anatomy](#understanding-node-anatomy)
2. [Connection Fundamentals](#connection-fundamentals)
3. [Type Compatibility System](#type-compatibility-system)
4. [Step-by-Step Connection Process](#step-by-step-connection-process)
5. [Common Connection Patterns](#common-connection-patterns)
6. [Edge Cases and Validation](#edge-cases-and-validation)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Complete Working Example](#complete-working-example)

---

## Understanding Node Anatomy

### Node Structure Overview

Every Flowise node has three key connection-related components:

```python
node = {
    "id": "chatOpenAI_0",  # Unique node identifier
    "data": {
        # Connection Points
        "inputAnchors": [],   # Where data flows IN
        "outputAnchors": [],  # Where data flows OUT

        # Configuration
        "inputParams": [],    # UI parameters (not connections)
        "inputs": {}          # Actual parameter values
    }
}
```

### Anchors vs Parameters

**Anchors** (Connection Points):
- Handle data flow between nodes
- Have types like `BaseLanguageModel`, `BaseMemory`, `Tool`
- Appear as connection ports in Flowise UI
- Created from node template inputs with non-UI types

**Parameters** (UI Inputs):
- Handle configuration values
- Have types like `string`, `number`, `boolean`, `options`
- Appear as form fields in Flowise UI
- Cannot be connected to other nodes

### Anchor Structure

```python
# Input Anchor (where data comes FROM another node)
{
    "id": "conversationChain_0-input-model-BaseLanguageModel",
    "name": "model",
    "label": "Language Model",
    "type": "BaseLanguageModel",
    "list": False  # If True, accepts multiple connections
}

# Output Anchor (where data goes TO another node)
{
    "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
    "name": "chatOpenAI",
    "label": "ChatOpenAI",
    "type": "ChatOpenAI | BaseChatModel | BaseLanguageModel"
}
```

### Handle ID Format (CRITICAL)

Handle IDs MUST follow this exact format:

```
Output: {nodeId}-output-{paramName}-{types}
Input:  {nodeId}-input-{paramName}-{types}

Examples:
✅ "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel"
✅ "conversationChain_0-input-model-BaseLanguageModel"
✅ "bufferMemory_0-output-bufferMemory-BufferMemory|BaseMemory"

❌ "chatOpenAI_0-output"  (missing param name and types)
❌ "model-input-BaseLanguageModel"  (missing node ID)
```

**WHY**: Flowise uses this format to:
- Identify which node the connection belongs to
- Determine which parameter is being connected
- Validate type compatibility

---

## Connection Fundamentals

### Edge (Connection) Structure

```python
edge = {
    "id": "chatOpenAI_0-conversationChain_0",  # source-target
    "source": "chatOpenAI_0",                  # Source node ID
    "target": "conversationChain_0",           # Target node ID
    "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
    "targetHandle": "conversationChain_0-input-model-BaseLanguageModel",
    "type": "buttonedge"  # Edge type (always "buttonedge" for Flowise)
}
```

### Connection Rules

1. **Source must be an outputAnchor** on the source node
2. **Target must be an inputAnchor** on the target node
3. **Types must be compatible** (see Type Compatibility section)
4. **Single connection limit**: If `list: False`, input can only accept ONE connection
5. **No self-connections**: A node cannot connect to itself
6. **No cycles** (in most flow types, except AgentFlow)

### Connection Direction

```
SOURCE (Output) ──────> TARGET (Input)

Example:
chatOpenAI_0 (output: ChatOpenAI) ──> conversationChain_0 (input: BaseLanguageModel)
```

**Data flows from left to right** in the diagram, from output to input.

---

## Type Compatibility System

### Type Hierarchy

Flowise uses a hierarchical type system where child types can connect to parent types:

```
BaseLanguageModel (PARENT)
├── BaseChatModel (CHILD)
│   ├── ChatOpenAI (GRANDCHILD)
│   ├── ChatAnthropic
│   └── ChatGoogleGenerativeAI
└── BaseLLM (CHILD)
    ├── OpenAI
    └── HuggingFace

BaseMemory (PARENT)
├── BufferMemory (CHILD)
├── BufferWindowMemory (CHILD)
└── ConversationSummaryMemory (CHILD)

Tool (PARENT)
├── Calculator (CHILD)
├── Serper (CHILD)
└── WebBrowser (CHILD)
```

### Compatibility Rules

```python
def are_types_compatible(source_types: str, target_types: str) -> bool:
    """
    Check if source output can connect to target input.

    Source types: "ChatOpenAI|BaseChatModel|BaseLanguageModel"
    Target types: "BaseLanguageModel"

    Result: True (BaseLanguageModel is in source types)
    """
    source_list = source_types.split('|')
    target_list = target_types.split('|')

    # Compatible if ANY target type matches ANY source type
    return any(target_type.strip() in source_list for target_type in target_list)
```

### Compatibility Examples

| Source Type | Target Type | Compatible? | Reason |
|-------------|-------------|-------------|--------|
| `ChatOpenAI\|BaseChatModel\|BaseLanguageModel` | `BaseLanguageModel` | ✅ Yes | BaseLanguageModel in source |
| `BufferMemory\|BaseMemory` | `BaseMemory` | ✅ Yes | BaseMemory in source |
| `Calculator\|Tool` | `Tool` | ✅ Yes | Tool in source |
| `ChatOpenAI\|BaseChatModel` | `BaseMemory` | ❌ No | No overlap |
| `OpenAIEmbeddings\|Embeddings` | `BaseLanguageModel` | ❌ No | Different hierarchies |

### Multi-Type Inputs

Some inputs accept multiple types:

```python
# Input that accepts EITHER Document OR BaseRetriever
{
    "name": "vectorStoreRetriever",
    "type": "Document | BaseRetriever"
}

# Compatible sources:
✅ "Document"
✅ "BaseRetriever"
✅ "Pinecone|VectorStore|BaseRetriever"  (has BaseRetriever)
❌ "OpenAIEmbeddings|Embeddings"  (no match)
```

---

## Step-by-Step Connection Process

### Step 1: Identify Connection Need

Ask yourself:
1. What data does my target node need?
2. Which input anchor requires this data?
3. What type does this input accept?

**Example**: ConversationChain needs a Language Model
- Target node: `conversationChain_0`
- Input anchor: `model` (type: `BaseLanguageModel`)

### Step 2: Find Compatible Source

Look for a node that:
1. Has the required data as output
2. Output type is compatible with input type

**Example**: ChatOpenAI provides a Language Model
- Source node: `chatOpenAI_0`
- Output anchor: `chatOpenAI` (type: `ChatOpenAI|BaseChatModel|BaseLanguageModel`)
- ✅ Compatible: `BaseLanguageModel` is in the output types

### Step 3: Extract Anchor IDs

Get the exact handle IDs from the node structures:

```python
# From source node
source_node = {
    "id": "chatOpenAI_0",
    "data": {
        "outputAnchors": [
            {
                "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
                "name": "chatOpenAI",
                "type": "ChatOpenAI | BaseChatModel | BaseLanguageModel"
            }
        ]
    }
}
source_handle = source_node["data"]["outputAnchors"][0]["id"]

# From target node
target_node = {
    "id": "conversationChain_0",
    "data": {
        "inputAnchors": [
            {
                "id": "conversationChain_0-input-model-BaseLanguageModel",
                "name": "model",
                "type": "BaseLanguageModel"
            }
        ]
    }
}
target_handle = target_node["data"]["inputAnchors"][0]["id"]
```

### Step 4: Validate Type Compatibility

```python
# Extract types from handles
source_types = "ChatOpenAI|BaseChatModel|BaseLanguageModel"
target_types = "BaseLanguageModel"

# Check compatibility
if not are_types_compatible(source_types, target_types):
    raise ValueError(f"Type mismatch: {source_types} -> {target_types}")
```

### Step 5: Create Edge Object

```python
edge = {
    "id": f"{source_node['id']}-{target_node['id']}",
    "source": source_node["id"],
    "target": target_node["id"],
    "sourceHandle": source_handle,
    "targetHandle": target_handle,
    "type": "buttonedge"
}
```

### Step 6: Validate Connection Rules

```python
# Check 1: Source and target nodes exist
assert source_node["id"] in [n["id"] for n in nodes]
assert target_node["id"] in [n["id"] for n in nodes]

# Check 2: No self-connection
assert source_node["id"] != target_node["id"]

# Check 3: Single connection limit (if list: False)
target_anchor = next(a for a in target_node["data"]["inputAnchors"] if a["id"] == target_handle)
if not target_anchor.get("list", False):
    # Check no existing connection to this input
    existing = [e for e in edges if e["targetHandle"] == target_handle]
    assert len(existing) == 0, f"Input {target_anchor['name']} already connected"
```

### Step 7: Add to Edges Array

```python
edges.append(edge)
```

---

## Common Connection Patterns

### Pattern 1: LLM → Chain (Simple Chat)

**Goal**: Connect a language model to a conversation chain

```python
# Nodes
chatOpenAI = {
    "id": "chatOpenAI_0",
    "data": {
        "outputAnchors": [
            {"id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
             "name": "chatOpenAI", "type": "ChatOpenAI | BaseChatModel | BaseLanguageModel"}
        ]
    }
}

conversationChain = {
    "id": "conversationChain_0",
    "data": {
        "inputAnchors": [
            {"id": "conversationChain_0-input-model-BaseLanguageModel",
             "name": "model", "type": "BaseLanguageModel"}
        ]
    }
}

# Connection
edge = {
    "id": "chatOpenAI_0-conversationChain_0",
    "source": "chatOpenAI_0",
    "target": "conversationChain_0",
    "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
    "targetHandle": "conversationChain_0-input-model-BaseLanguageModel",
    "type": "buttonedge"
}
```

**Type Flow**: `ChatOpenAI` → `BaseLanguageModel` ✅

### Pattern 2: Memory → Chain (Add Memory)

**Goal**: Connect memory to maintain conversation history

```python
# Nodes
bufferMemory = {
    "id": "bufferMemory_0",
    "data": {
        "outputAnchors": [
            {"id": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseMemory",
             "name": "bufferMemory", "type": "BufferMemory | BaseMemory"}
        ]
    }
}

conversationChain = {
    "id": "conversationChain_0",
    "data": {
        "inputAnchors": [
            {"id": "conversationChain_0-input-memory-BaseMemory",
             "name": "memory", "type": "BaseMemory"}
        ]
    }
}

# Connection
edge = {
    "id": "bufferMemory_0-conversationChain_0",
    "source": "bufferMemory_0",
    "target": "conversationChain_0",
    "sourceHandle": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseMemory",
    "targetHandle": "conversationChain_0-input-memory-BaseMemory",
    "type": "buttonedge"
}
```

**Type Flow**: `BufferMemory` → `BaseMemory` ✅

### Pattern 3: Multiple Tools → Agent

**Goal**: Connect multiple tools to an agent (list input)

```python
# Nodes
calculator = {
    "id": "calculator_0",
    "data": {
        "outputAnchors": [
            {"id": "calculator_0-output-calculator-Calculator|Tool",
             "name": "calculator", "type": "Calculator | Tool"}
        ]
    }
}

serper = {
    "id": "serper_0",
    "data": {
        "outputAnchors": [
            {"id": "serper_0-output-serper-Serper|Tool",
             "name": "serper", "type": "Serper | Tool"}
        ]
    }
}

agent = {
    "id": "openAIFunctionAgent_0",
    "data": {
        "inputAnchors": [
            {"id": "openAIFunctionAgent_0-input-tools-Tool",
             "name": "tools", "type": "Tool", "list": True}  # Accepts multiple
        ]
    }
}

# Connections (both tools can connect because list: True)
edges = [
    {
        "id": "calculator_0-openAIFunctionAgent_0",
        "source": "calculator_0",
        "target": "openAIFunctionAgent_0",
        "sourceHandle": "calculator_0-output-calculator-Calculator|Tool",
        "targetHandle": "openAIFunctionAgent_0-input-tools-Tool",
        "type": "buttonedge"
    },
    {
        "id": "serper_0-openAIFunctionAgent_0",
        "source": "serper_0",
        "target": "openAIFunctionAgent_0",
        "sourceHandle": "serper_0-output-serper-Serper|Tool",
        "targetHandle": "openAIFunctionAgent_0-input-tools-Tool",
        "type": "buttonedge"
    }
]
```

**Type Flow**: `Calculator|Tool` → `Tool` ✅, `Serper|Tool` → `Tool` ✅

### Pattern 4: Document Processing Pipeline

**Goal**: Connect document loader → splitter → embeddings → vector store

```python
# Node 1: PDF Loader
pdfFile = {
    "id": "pdfFile_0",
    "data": {
        "outputAnchors": [
            {"id": "pdfFile_0-output-pdfFile-Document",
             "name": "pdfFile", "type": "Document"}
        ]
    }
}

# Node 2: Text Splitter
splitter = {
    "id": "recursiveCharacterTextSplitter_0",
    "data": {
        "inputAnchors": [
            {"id": "recursiveCharacterTextSplitter_0-input-document-Document",
             "name": "document", "type": "Document"}
        ],
        "outputAnchors": [
            {"id": "recursiveCharacterTextSplitter_0-output-recursiveCharacterTextSplitter-Document",
             "name": "recursiveCharacterTextSplitter", "type": "Document"}
        ]
    }
}

# Node 3: Embeddings
embeddings = {
    "id": "openAIEmbeddings_0",
    "data": {
        "outputAnchors": [
            {"id": "openAIEmbeddings_0-output-openAIEmbeddings-OpenAIEmbeddings|Embeddings",
             "name": "openAIEmbeddings", "type": "OpenAIEmbeddings | Embeddings"}
        ]
    }
}

# Node 4: Vector Store
pinecone = {
    "id": "pinecone_0",
    "data": {
        "inputAnchors": [
            {"id": "pinecone_0-input-document-Document",
             "name": "document", "type": "Document", "list": True},
            {"id": "pinecone_0-input-embeddings-Embeddings",
             "name": "embeddings", "type": "Embeddings"}
        ]
    }
}

# Connections
edges = [
    # PDF → Splitter
    {
        "id": "pdfFile_0-recursiveCharacterTextSplitter_0",
        "source": "pdfFile_0",
        "target": "recursiveCharacterTextSplitter_0",
        "sourceHandle": "pdfFile_0-output-pdfFile-Document",
        "targetHandle": "recursiveCharacterTextSplitter_0-input-document-Document",
        "type": "buttonedge"
    },
    # Splitter → Vector Store
    {
        "id": "recursiveCharacterTextSplitter_0-pinecone_0",
        "source": "recursiveCharacterTextSplitter_0",
        "target": "pinecone_0",
        "sourceHandle": "recursiveCharacterTextSplitter_0-output-recursiveCharacterTextSplitter-Document",
        "targetHandle": "pinecone_0-input-document-Document",
        "type": "buttonedge"
    },
    # Embeddings → Vector Store
    {
        "id": "openAIEmbeddings_0-pinecone_0",
        "source": "openAIEmbeddings_0",
        "target": "pinecone_0",
        "sourceHandle": "openAIEmbeddings_0-output-openAIEmbeddings-OpenAIEmbeddings|Embeddings",
        "targetHandle": "pinecone_0-input-embeddings-Embeddings",
        "type": "buttonedge"
    }
]
```

**Type Flows**:
- `Document` → `Document` ✅
- `Document` → `Document` ✅
- `OpenAIEmbeddings|Embeddings` → `Embeddings` ✅

---

## Edge Cases and Validation

### Edge Case 1: Single vs Multiple Connections

```python
# Single connection input (list: False or undefined)
input_anchor = {
    "name": "model",
    "type": "BaseLanguageModel",
    "list": False  # Can only accept ONE connection
}

# Attempting second connection to same input
existing_edges = [
    {"targetHandle": "chain_0-input-model-BaseLanguageModel"}
]

# ❌ This will fail validation
new_edge = {
    "targetHandle": "chain_0-input-model-BaseLanguageModel"
}

# ✅ Solution: Remove existing connection first, or connect to different input
```

### Edge Case 2: Optional vs Required Inputs

```python
# Optional input (can be empty)
optional_input = {
    "name": "memory",
    "type": "BaseMemory",
    "optional": True  # Not required for execution
}

# Required input (must be connected or have value)
required_input = {
    "name": "model",
    "type": "BaseLanguageModel",
    "required": True  # Must be connected for execution
}

# Validation: Required inputs MUST have connection OR default value
def validate_required_inputs(node, edges):
    for anchor in node["data"]["inputAnchors"]:
        if anchor.get("required", False):
            # Check if connected
            is_connected = any(e["targetHandle"] == anchor["id"] for e in edges)
            # Check if has default value
            has_default = anchor["name"] in node["data"]["inputs"]

            if not (is_connected or has_default):
                raise ValueError(f"Required input '{anchor['name']}' not satisfied")
```

### Edge Case 3: Conditional Types

Some nodes accept different types based on configuration:

```python
# Vector store can accept EITHER documents OR existing index
vector_store_input = {
    "name": "documents",
    "type": "Document | BaseRetriever"  # Accepts either type
}

# ✅ Connect documents
edge1 = {
    "sourceHandle": "pdfFile_0-output-pdfFile-Document",
    "targetHandle": "pinecone_0-input-documents-Document|BaseRetriever"
}

# ✅ OR connect retriever
edge2 = {
    "sourceHandle": "existingRetriever_0-output-retriever-BaseRetriever",
    "targetHandle": "pinecone_0-input-documents-Document|BaseRetriever"
}
```

### Edge Case 4: Disconnected Nodes

```python
# Valid: Single node with no connections
nodes = [
    {"id": "chatOpenAI_0", "data": {...}}
]
edges = []  # No connections needed for single node

# Invalid: Multiple nodes with disconnected nodes
nodes = [
    {"id": "chatOpenAI_0", "data": {...}},
    {"id": "conversationChain_0", "data": {...}},
    {"id": "bufferMemory_0", "data": {...}}  # ❌ Not connected to anything
]
edges = [
    {"source": "chatOpenAI_0", "target": "conversationChain_0"}
]

# ✅ Validation should catch this
def validate_no_orphans(nodes, edges):
    if len(nodes) <= 1:
        return  # Single node is OK

    connected = set()
    for edge in edges:
        connected.add(edge["source"])
        connected.add(edge["target"])

    for node in nodes:
        if node["id"] not in connected:
            raise ValueError(f"Node {node['id']} is disconnected")
```

---

## Troubleshooting Guide

### Problem 1: "Invalid handle format"

**Symptoms**: Connection rejected, error about handle format

**Causes**:
- Manually constructed handle ID instead of using anchor ID
- Missing parts in handle ID (nodeId, param name, or types)
- Wrong delimiter (should be `-`)

**Solutions**:
```python
# ❌ WRONG: Manual construction
wrong_handle = f"{node_id}-output-{param_name}"

# ✅ CORRECT: Use anchor ID from node
correct_handle = node["data"]["outputAnchors"][0]["id"]
```

### Problem 2: "Type mismatch"

**Symptoms**: Connection rejected, incompatible types error

**Causes**:
- Source output type doesn't match target input type
- No overlap in type hierarchies

**Solutions**:
```python
# Debug: Print types
print(f"Source: {source_types}")
print(f"Target: {target_types}")

# Check each type
source_list = source_types.split('|')
target_list = target_types.split('|')

print("Checking compatibility:")
for target_type in target_list:
    if target_type.strip() in source_list:
        print(f"  ✅ {target_type} found in source")
    else:
        print(f"  ❌ {target_type} NOT in source")

# If no matches, check type hierarchy documentation
# May need different node type or intermediate conversion
```

### Problem 3: "Input already connected"

**Symptoms**: Cannot add connection, input limit reached

**Causes**:
- Input anchor has `list: False` (single connection only)
- Existing connection already using this input

**Solutions**:
```python
# Check if input accepts multiple connections
input_anchor = next(a for a in node["data"]["inputAnchors"]
                   if a["name"] == "model")

if input_anchor.get("list", False):
    print("✅ Accepts multiple connections")
else:
    print("❌ Single connection only")
    # Remove existing connection first
    edges = [e for e in edges if e["targetHandle"] != input_anchor["id"]]
```

### Problem 4: "Node not found"

**Symptoms**: Edge references non-existent node

**Causes**:
- Edge created before node added to nodes array
- Typo in node ID
- Wrong order of operations

**Solutions**:
```python
# ✅ CORRECT ORDER:
# 1. Create all nodes first
nodes = []
nodes.append(create_node("chatOpenAI", ...))
nodes.append(create_node("conversationChain", ...))

# 2. Then create edges
edges = []
edges.append(create_edge(nodes[0], nodes[1], ...))

# 3. Validate
assert edge["source"] in [n["id"] for n in nodes]
assert edge["target"] in [n["id"] for n in nodes]
```

### Problem 5: "Ending node required"

**Symptoms**: Flow validation fails, no output

**Causes**:
- No Chain, Agent, or End node in flow
- Only intermediate nodes (LLMs, Tools, Memory)

**Solutions**:
```python
# Check for ending node
ending_categories = ["Chains", "Agents", "Multi Agents", "Sequential Agents"]
has_ending = any(
    n["data"]["category"] in ending_categories
    for n in nodes
)

if not has_ending:
    # ❌ Missing ending node
    # ✅ Add a Chain or Agent node
    chain = create_node("conversationChain", ...)
    nodes.append(chain)
    # Connect LLM to chain
    edges.append(create_edge(llm_node, chain, ...))
```

### Problem 6: "Required input missing"

**Symptoms**: Node execution fails, missing required data

**Causes**:
- Required input anchor not connected
- Required parameter not set

**Solutions**:
```python
# Check all required inputs
for node in nodes:
    for anchor in node["data"]["inputAnchors"]:
        if anchor.get("required", False):
            # Check connection
            connected = any(e["targetHandle"] == anchor["id"] for e in edges)

            # Check default value
            has_value = anchor["name"] in node["data"]["inputs"]

            if not (connected or has_value):
                print(f"❌ {node['id']}.{anchor['name']} is required but not connected")
                print(f"   Type needed: {anchor['type']}")
                print(f"   Find a node that outputs: {anchor['type']}")
```

---

## Complete Working Example

Here's the full code for the 3-node conversation flow with detailed comments:

```python
#!/usr/bin/env python3
"""
Complete example: Create a 3-node conversation flow in Flowise.

This demonstrates all concepts from the connection guide:
- Proper node structure with anchors
- Type-compatible connections
- Edge validation
- Full flow deployment
"""

import json
import asyncio
import os
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.models import FlowiseConfig


async def create_conversation_flow():
    # Initialize client
    config = FlowiseConfig(
        api_url=os.getenv("FLOWISE_API_URL", "http://localhost:3000"),
        api_key=os.getenv("FLOWISE_API_KEY")
    )

    async with FlowiseClient(config=config) as client:
        # =================================================================
        # STEP 1: Define Nodes with Anchors
        # =================================================================

        nodes = []

        # Node 1: ChatOpenAI (LLM)
        # Output: ChatOpenAI|BaseChatModel|BaseLanguageModel
        chatOpenAI = {
            "id": "chatOpenAI_0",
            "type": "customNode",
            "position": {"x": 250, "y": 100},
            "data": {
                "id": "chatOpenAI_0",
                "label": "ChatOpenAI",
                "name": "chatOpenAI",
                "category": "Chat Models",
                "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel"],

                # UI Parameters (not connections)
                "inputParams": [
                    {
                        "id": "chatOpenAI_0-input-modelName-options",
                        "name": "modelName",
                        "type": "options",
                        "default": "gpt-3.5-turbo"
                    },
                    {
                        "id": "chatOpenAI_0-input-temperature-number",
                        "name": "temperature",
                        "type": "number",
                        "default": 0.7
                    }
                ],
                "inputs": {
                    "temperature": 0.7,
                    "modelName": "gpt-3.5-turbo"
                },

                # Connection points
                "inputAnchors": [],  # No inputs needed
                "outputAnchors": [
                    {
                        "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
                        "name": "chatOpenAI",
                        "label": "ChatOpenAI",
                        "type": "ChatOpenAI | BaseChatModel | BaseLanguageModel"
                    }
                ],
                "outputs": {}
            }
        }
        nodes.append(chatOpenAI)

        # Node 2: BufferMemory (Memory)
        # Output: BufferMemory|BaseMemory
        bufferMemory = {
            "id": "bufferMemory_0",
            "type": "customNode",
            "position": {"x": 250, "y": 300},
            "data": {
                "id": "bufferMemory_0",
                "label": "Buffer Memory",
                "name": "bufferMemory",
                "category": "Memory",
                "baseClasses": ["BufferMemory", "BaseMemory"],

                "inputParams": [
                    {
                        "id": "bufferMemory_0-input-memoryKey-string",
                        "name": "memoryKey",
                        "type": "string",
                        "default": "chat_history"
                    }
                ],
                "inputs": {
                    "memoryKey": "chat_history"
                },

                "inputAnchors": [],
                "outputAnchors": [
                    {
                        "id": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseMemory",
                        "name": "bufferMemory",
                        "label": "BufferMemory",
                        "type": "BufferMemory | BaseMemory"
                    }
                ],
                "outputs": {}
            }
        }
        nodes.append(bufferMemory)

        # Node 3: ConversationChain (Chain - Ending Node)
        # Inputs: model (BaseLanguageModel), memory (BaseMemory)
        conversationChain = {
            "id": "conversationChain_0",
            "type": "customNode",
            "position": {"x": 550, "y": 200},
            "data": {
                "id": "conversationChain_0",
                "label": "Conversation Chain",
                "name": "conversationChain",
                "category": "Chains",  # Ending node category
                "baseClasses": ["ConversationChain", "LLMChain", "BaseChain"],

                "inputParams": [
                    {
                        "id": "conversationChain_0-input-systemMessage-string",
                        "name": "systemMessage",
                        "type": "string",
                        "optional": True
                    }
                ],
                "inputs": {
                    "systemMessage": "You are a helpful AI assistant."
                },

                # Connection points (REQUIRED for chain to work)
                "inputAnchors": [
                    {
                        "id": "conversationChain_0-input-model-BaseLanguageModel",
                        "name": "model",
                        "label": "Language Model",
                        "type": "BaseLanguageModel",
                        "required": True  # MUST be connected
                    },
                    {
                        "id": "conversationChain_0-input-memory-BaseMemory",
                        "name": "memory",
                        "label": "Memory",
                        "type": "BaseMemory",
                        "optional": True  # Optional
                    }
                ],
                "outputAnchors": [
                    {
                        "id": "conversationChain_0-output-conversationChain-ConversationChain|LLMChain|BaseChain",
                        "name": "conversationChain",
                        "label": "ConversationChain",
                        "type": "ConversationChain | LLMChain | BaseChain"
                    }
                ],
                "outputs": {}
            }
        }
        nodes.append(conversationChain)

        # =================================================================
        # STEP 2: Create Connections (Edges)
        # =================================================================

        edges = []

        # Connection 1: ChatOpenAI → ConversationChain (model input)
        # Type flow: ChatOpenAI|BaseChatModel|BaseLanguageModel → BaseLanguageModel
        # Compatible: ✅ BaseLanguageModel is in source types
        edge1 = {
            "id": "chatOpenAI_0-conversationChain_0",
            "source": "chatOpenAI_0",
            "target": "conversationChain_0",

            # Source: Get from chatOpenAI outputAnchors
            "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",

            # Target: Get from conversationChain inputAnchors
            "targetHandle": "conversationChain_0-input-model-BaseLanguageModel",

            "type": "buttonedge"
        }
        edges.append(edge1)

        # Connection 2: BufferMemory → ConversationChain (memory input)
        # Type flow: BufferMemory|BaseMemory → BaseMemory
        # Compatible: ✅ BaseMemory is in source types
        edge2 = {
            "id": "bufferMemory_0-conversationChain_0",
            "source": "bufferMemory_0",
            "target": "conversationChain_0",

            # Source: Get from bufferMemory outputAnchors
            "sourceHandle": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseMemory",

            # Target: Get from conversationChain inputAnchors
            "targetHandle": "conversationChain_0-input-memory-BaseMemory",

            "type": "buttonedge"
        }
        edges.append(edge2)

        # =================================================================
        # STEP 3: Validate Connections
        # =================================================================

        print("Validating connections...")

        # Check 1: All nodes connected
        connected_nodes = set()
        for edge in edges:
            connected_nodes.add(edge["source"])
            connected_nodes.add(edge["target"])

        for node in nodes:
            if node["id"] not in connected_nodes:
                print(f"  ⚠️  Warning: Node {node['id']} is disconnected")

        # Check 2: Has ending node
        ending_categories = ["Chains", "Agents"]
        has_ending = any(n["data"]["category"] in ending_categories for n in nodes)
        print(f"  {'✅' if has_ending else '❌'} Has ending node: {has_ending}")

        # Check 3: Type compatibility
        for edge in edges:
            source_node = next(n for n in nodes if n["id"] == edge["source"])
            target_node = next(n for n in nodes if n["id"] == edge["target"])

            source_anchor = next(a for a in source_node["data"]["outputAnchors"]
                               if a["id"] == edge["sourceHandle"])
            target_anchor = next(a for a in target_node["data"]["inputAnchors"]
                               if a["id"] == edge["targetHandle"])

            source_types = source_anchor["type"].split(" | ")
            target_types = target_anchor["type"].split(" | ")

            compatible = any(t in source_types for t in target_types)
            print(f"  {'✅' if compatible else '❌'} {edge['source']} → {edge['target']}: {compatible}")

        # =================================================================
        # STEP 4: Build and Deploy Flow
        # =================================================================

        flow_data = {
            "nodes": nodes,
            "edges": edges,
            "viewport": {"x": 0, "y": 0, "zoom": 1}
        }

        print("\n📦 Creating chatflow in Flowise...")
        chatflow = await client.create_chatflow(
            name="Complete 3-Node Conversation Flow",
            flow_data=json.dumps(flow_data),
            deployed=True
        )

        print(f"\n✅ Success!")
        print(f"   ID: {chatflow.id}")
        print(f"   Name: {chatflow.name}")
        print(f"   Deployed: {chatflow.deployed}")
        print(f"\nFlow Structure:")
        print("   ChatOpenAI ──┐")
        print("                ├──> ConversationChain")
        print("   BufferMemory ┘")

        return chatflow


if __name__ == "__main__":
    asyncio.run(create_conversation_flow())
```

---

## Summary Checklist

When creating connections, verify:

- [ ] Source node has outputAnchor with required data
- [ ] Target node has inputAnchor accepting that data type
- [ ] Types are compatible (check type hierarchy)
- [ ] Handle IDs follow correct format
- [ ] Single-connection limit respected (if `list: False`)
- [ ] All nodes are connected (no orphans)
- [ ] At least one ending node exists (Chain/Agent)
- [ ] Required inputs are satisfied
- [ ] No self-connections
- [ ] No cycles (unless AgentFlow)

---

## Additional Resources

- **flowise-ai-guide.md**: Comprehensive Flowise system documentation
- **flowise-implementation-helpers.js**: Helper functions and templates
- **Flowise UI**: Visual representation at http://your-flowise-url/chatflows

---

**Version**: 1.0.0 | **Created**: 2025-10-17 | **Author**: AI Assistant based on working implementation
