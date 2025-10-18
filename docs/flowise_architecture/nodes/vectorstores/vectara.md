# Vectara

**Category**: Vector Stores | **Type**: Vectara | **Version**: 2.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Vectara, a LLM-powered search-as-a-service

## Credentials

**Required**: Yes

**Credential Types**:
- vectaraApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| File | `file` | File to upload to Vectara. Supported file types: https://docs.vectara.com/docs/api-reference/indexin | - |
| Metadata Filter | `string` | Filter to apply to Vectara metadata. Refer to the <a target= | - |
| Sentences Before | `number` | Number of sentences to fetch before the matched sentence. Defaults to 2. | - |
| Sentences After | `number` | Number of sentences to fetch after the matched sentence. Defaults to 2. | - |
| Lambda | `number` | Enable hybrid search to improve retrieval accuracy by adjusting the balance (from 0 to 1) between ne | - |
| Top K | `number` | Number of top results to fetch. Defaults to 5 | - |
| MMR K | `number` | Number of top results to fetch for MMR. Defaults to 50 | - |
| MMR diversity bias | `number` | The diversity bias to use for MMR. This is a value between 0.0 and 1.0 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- File (`file`)

**Outputs**: `Vectara`

## Common Use Cases

1. Use Vectara when you need upsert embedded data and perform similarity search upon query using vectara, a llm-powered search-as-a-service
2. Connect to other nodes that accept `Vectara` input

---

**Source**: `packages/components/nodes/vectorstores/Vectara/Vectara.ts`