# Agent Memory

**Category**: Memory | **Type**: AgentMemory | **Version**: 2.0

---

## Overview

Memory for agentflow to remember the state of the conversation

## Credentials

**Required**: Yes

**Credential Types**:
- PostgresApi
- MySQLApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Database | `options` |  | - |

## Connections

**Outputs**: `AgentMemory`

## Common Use Cases

1. Use Agent Memory when you need memory for agentflow to remember the state of the conversation
2. Connect to other nodes that accept `AgentMemory` input

---

**Source**: `packages/components/nodes/memory/AgentMemory/AgentMemory.ts`