# Worker

**Category**: Multi Agents | **Type**: Worker | **Version**: 2.0

---

## Overview

No description available.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Worker Name | `string` |  | - |
| Worker Prompt | `string` |  | - |
| Supervisor | `Supervisor` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Tools | `Tool` |  | - |
| Tool Calling Chat Model | `BaseChatModel` | Only compatible with models that are capable of function calling: ChatOpenAI, ChatMistral, ChatAnthr | - |
| Format Prompt Values | `json` |  | - |
| Max Iterations | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Tools (`Tool`)
- Supervisor (`Supervisor`)
- Tool Calling Chat Model (`BaseChatModel`)

**Outputs**: `Worker`

## Common Use Cases

1. Use Worker when you need this functionality
2. Connect to other nodes that accept `Worker` input

---

**Source**: `packages/components/nodes/multiagents/Worker/Worker.ts`