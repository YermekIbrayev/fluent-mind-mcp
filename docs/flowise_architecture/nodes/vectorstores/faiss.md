# Faiss

**Category**: Vector Stores | **Type**: Faiss | **Version**: 1.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Faiss library from Meta

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Base Path to load | `string` | Path to load faiss.index file | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Faiss`

## Common Use Cases

1. Use Faiss when you need upsert embedded data and perform similarity search upon query using faiss library from meta
2. Connect to other nodes that accept `Faiss` input

---

**Source**: `packages/components/nodes/vectorstores/Faiss/Faiss.ts`