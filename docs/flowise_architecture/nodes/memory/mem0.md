# Mem0

**Category**: Memory | **Type**: Mem0 | **Version**: 1.1

---

## Overview

Stores and manages chat memory using Mem0 service

## Credentials

**Required**: Yes

**Credential Types**:
- mem0MemoryApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| User ID | `string` | Unique identifier for the user. Required only if  | flowise-default-user |
| Search Only | `boolean` | Search only mode | - |
| Run ID | `string` | Unique identifier for the run session | - |
| Agent ID | `string` | Identifier for the agent | - |
| App ID | `string` | Identifier for the application | - |
| Project ID | `string` | Identifier for the project | - |
| Organization ID | `string` | Identifier for the organization | - |
| Memory Key | `string` |  | history |
| Input Key | `string` |  | input |
| Output Key | `string` |  | text |

## Connections

**Outputs**: `Mem0`

## Common Use Cases

1. Use Mem0 when you need stores and manages chat memory using mem0 service
2. Connect to other nodes that accept `Mem0` input

---

**Source**: `packages/components/nodes/memory/Mem0/Mem0.ts`