# BabyAGI

**Category**: Agents | **Type**: BabyAGI | **Version**: 2.0

---

## Overview

Task Driven Autonomous Agent which creates new task and reprioritizes task list based on objective

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel` |  | - |
| Vector Store | `VectorStore` |  | - |
| Task Loop | `number` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |

## Connections

**Accepts Inputs From**:
- Chat Model (`BaseChatModel`)
- Vector Store (`VectorStore`)
- Input Moderation (`Moderation`)

**Outputs**: `BabyAGI`

## Common Use Cases

1. Use BabyAGI when you need task driven autonomous agent which creates new task and reprioritizes task list based on objective
2. Connect to other nodes that accept `BabyAGI` input

---

**Source**: `packages/components/nodes/agents/BabyAGI/BabyAGI.ts`