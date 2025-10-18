# Buffer Window Memory

**Category**: Memory | **Type**: BufferWindowMemory | **Version**: 2.0

---

## Overview

Uses a window of size k to surface the last k back-and-forth to use as memory

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Size | `number` | Window of size k to surface the last k back-and-forth to use as memory. | 4 |
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Outputs**: `BufferWindowMemory`

## Common Use Cases

1. Use Buffer Window Memory when you need uses a window of size k to surface the last k back-and-forth to use as memory
2. Connect to other nodes that accept `BufferWindowMemory` input

---

**Source**: `packages/components/nodes/memory/BufferWindowMemory/BufferWindowMemory.ts`