# Zep Memory - Open Source

**Category**: Memory | **Type**: ZepMemory | **Version**: 2.0

---

## Overview

Summarizes the conversation and stores the memory in zep server

## Credentials

**Required**: Yes

**Credential Types**:
- zepMemoryApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base URL | `string` |  | http://127.0.0.1:8000 |
| Size | `number` | Window of size k to surface the last k back-and-forth to use as memory. | 10 |
| AI Prefix | `string` |  | ai |
| Human Prefix | `string` |  | human |
| Memory Key | `string` |  | chat_history |
| Input Key | `string` |  | input |
| Output Key | `string` |  | text |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Outputs**: `ZepMemory`

## Common Use Cases

1. Use Zep Memory - Open Source when you need summarizes the conversation and stores the memory in zep server
2. Connect to other nodes that accept `ZepMemory` input

---

**Source**: `packages/components/nodes/memory/ZepMemory/ZepMemory.ts`