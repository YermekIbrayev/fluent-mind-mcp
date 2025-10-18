# MongoDB Atlas Chat Memory

**Category**: Memory | **Type**: MongoDBAtlasChatMemory | **Version**: 1.0

---

## Overview

Stores the conversation in MongoDB Atlas

## Credentials

**Required**: Yes

**Credential Types**:
- mongoDBUrlApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Database | `string` |  | - |
| Collection Name | `string` |  | - |
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Outputs**: `MongoDBAtlasChatMemory`

## Common Use Cases

1. Use MongoDB Atlas Chat Memory when you need stores the conversation in mongodb atlas
2. Connect to other nodes that accept `MongoDBAtlasChatMemory` input

---

**Source**: `packages/components/nodes/memory/MongoDBMemory/MongoDBMemory.ts`