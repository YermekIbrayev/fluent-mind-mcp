# Buffer Memory

**Category**: Memory | **Type**: BufferMemory | **Version**: 2.0

---

## Overview

Retrieve chat messages stored in database

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Outputs**: `BufferMemory`

## Common Use Cases

1. Use Buffer Memory when you need retrieve chat messages stored in database
2. Connect to other nodes that accept `BufferMemory` input

---

**Source**: `packages/components/nodes/memory/BufferMemory/BufferMemory.ts`