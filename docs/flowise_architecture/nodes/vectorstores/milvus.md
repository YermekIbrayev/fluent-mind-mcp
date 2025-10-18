# Milvus

**Category**: Vector Stores | **Type**: Milvus | **Version**: 2.1

---

## Overview

Upsert embedded data and perform similarity search upon query using Milvus, world

## Credentials

**Required**: Yes

**Credential Types**:
- milvusAuth

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Milvus Server URL | `string` |  | - |
| Milvus Collection Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Milvus Partition Name | `string` |  | _default |
| File Upload | `boolean` | Allow file upload on the chat | - |
| Milvus Text Field | `string` |  | - |
| Milvus Filter | `string` | Filter data with a simple string query. Refer Milvus <a target= | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |
| Secure | `boolean` | Enable secure connection to Milvus server | - |
| Client PEM Path | `string` | Path to the client PEM file | - |
| Client Key Path | `string` | Path to the client key file | - |
| CA PEM Path | `string` | Path to the root PEM file | - |
| Server Name | `string` | Server name for the secure connection | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Milvus`

## Common Use Cases

1. Use Milvus when you need upsert embedded data and perform similarity search upon query using milvus, world
2. Connect to other nodes that accept `Milvus` input

---

**Source**: `packages/components/nodes/vectorstores/Milvus/Milvus.ts`