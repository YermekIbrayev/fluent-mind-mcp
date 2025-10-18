# Zep Collection - Open Source

**Category**: Vector Stores | **Type**: Zep | **Version**: 2.0

---

## Overview

Upsert embedded data and perform similarity or mmr search upon query using Zep, a fast and scalable building block for LLM apps

## Credentials

**Required**: Yes

**Credential Types**:
- zepMemoryApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Base URL | `string` |  | http://127.0.0.1:8000 |
| Zep Collection | `string` |  | - |
| Embedding Dimension | `number` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Zep Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Zep`

## Common Use Cases

1. Use Zep Collection - Open Source when you need upsert embedded data and perform similarity or mmr search upon query using zep, a fast and scalable building block for llm apps
2. Connect to other nodes that accept `Zep` input

---

**Source**: `packages/components/nodes/vectorstores/Zep/Zep.ts`