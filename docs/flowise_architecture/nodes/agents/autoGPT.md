# AutoGPT

**Category**: Agents | **Type**: AutoGPT | **Version**: 2.0

---

## Overview

Autonomous agent with chain of thoughts for self-guided task completion

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Allowed Tools | `Tool` |  | - |
| Chat Model | `BaseChatModel` |  | - |
| Vector Store Retriever | `BaseRetriever` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| AutoGPT Name | `string` |  | - |
| AutoGPT Role | `string` |  | - |
| Maximum Loop | `number` |  | - |
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |

## Connections

**Accepts Inputs From**:
- Allowed Tools (`Tool`)
- Chat Model (`BaseChatModel`)
- Vector Store Retriever (`BaseRetriever`)
- Input Moderation (`Moderation`)

**Outputs**: `AutoGPT`

## Common Use Cases

1. Use AutoGPT when you need autonomous agent with chain of thoughts for self-guided task completion
2. Connect to other nodes that accept `AutoGPT` input

---

**Source**: `packages/components/nodes/agents/AutoGPT/AutoGPT.ts`