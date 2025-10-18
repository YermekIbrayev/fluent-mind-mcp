# DynamoDB Chat Memory

**Category**: Memory | **Type**: DynamoDBChatMemory | **Version**: 1.0

---

## Overview

Stores the conversation in dynamo db table

## Credentials

**Required**: Yes

**Credential Types**:
- dynamodbMemoryApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Table Name | `string` |  | - |
| Partition Key | `string` |  | - |
| Region | `string` | The aws region in which table is located | - |
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session ID | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Outputs**: `DynamoDBChatMemory`

## Common Use Cases

1. Use DynamoDB Chat Memory when you need stores the conversation in dynamo db table
2. Connect to other nodes that accept `DynamoDBChatMemory` input

---

**Source**: `packages/components/nodes/memory/DynamoDb/DynamoDb.ts`