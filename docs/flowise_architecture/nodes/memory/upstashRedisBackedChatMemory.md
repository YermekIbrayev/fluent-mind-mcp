# Upstash Redis-Backed Chat Memory

**Category**: Memory | **Type**: UpstashRedisBackedChatMemory | **Version**: 2.0

---

## Overview

Summarizes the conversation and stores the memory in Upstash Redis server

## Credentials

**Required**: Yes

**Credential Types**:
- upstashRedisMemoryApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Upstash Redis REST URL | `string` |  | - |
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |
| Session Timeouts | `number` | Seconds till a session expires. If not specified, the session will never expire. | - |

## Connections

**Outputs**: `UpstashRedisBackedChatMemory`

## Common Use Cases

1. Use Upstash Redis-Backed Chat Memory when you need summarizes the conversation and stores the memory in upstash redis server
2. Connect to other nodes that accept `UpstashRedisBackedChatMemory` input

---

**Source**: `packages/components/nodes/memory/UpstashRedisBackedChatMemory/UpstashRedisBackedChatMemory.ts`