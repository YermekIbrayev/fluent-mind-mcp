# Redis-Backed Chat Memory

**Category**: Memory | **Type**: RedisBackedChatMemory | **Version**: 2.0

---

## Overview

Summarizes the conversation and stores the memory in Redis server

## Credentials

**Required**: Yes

**Credential Types**:
- redisCacheApi
- redisCacheUrlApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |
| Session Timeouts | `number` | Seconds till a session expires. If not specified, the session will never expire. | - |
| Window Size | `number` | Window of size k to surface the last k back-and-forth to use as memory. | - |

## Connections

**Outputs**: `RedisBackedChatMemory`

## Common Use Cases

1. Use Redis-Backed Chat Memory when you need summarizes the conversation and stores the memory in redis server
2. Connect to other nodes that accept `RedisBackedChatMemory` input

---

**Source**: `packages/components/nodes/memory/RedisBackedChatMemory/RedisBackedChatMemory.ts`