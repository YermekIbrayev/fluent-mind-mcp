# AWS DynamoDB KV Storage

**Category**: Tools | **Type**: AWSDynamoDBKVStorage | **Version**: 1.0

---

## Overview

Store and retrieve versioned text values in AWS DynamoDB

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| AWS Region | `options` | AWS Region where your DynamoDB tables are located | - |
| DynamoDB Table | `asyncOptions` | Select a DynamoDB table with partition key  | - |
| Operation | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Key Prefix | `string` | Optional prefix to add to all keys (e.g.,  | - |

## Connections

**Accepts Inputs From**:
- DynamoDB Table (`asyncOptions`)

**Outputs**: `AWSDynamoDBKVStorage`

## Common Use Cases

1. Use AWS DynamoDB KV Storage when you need store and retrieve versioned text values in aws dynamodb
2. Connect to other nodes that accept `AWSDynamoDBKVStorage` input

---

**Source**: `packages/components/nodes/tools/AWSDynamoDBKVStorage/AWSDynamoDBKVStorage.ts`