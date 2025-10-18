# Redis Cache

**Category**: Cache | **Type**: RedisCache | **Version**: 1.0

---

## Overview

Cache LLM response in Redis, useful for sharing cache across multiple processes or servers

## Credentials

**Required**: Yes

**Credential Types**:
- redisCacheApi
- redisCacheUrlApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Time to Live (ms) | `number` |  | - |

## Connections

**Outputs**: `RedisCache`

## Common Use Cases

1. Use Redis Cache when you need cache llm response in redis, useful for sharing cache across multiple processes or servers
2. Connect to other nodes that accept `RedisCache` input

---

**Source**: `packages/components/nodes/cache/RedisCache/RedisCache.ts`