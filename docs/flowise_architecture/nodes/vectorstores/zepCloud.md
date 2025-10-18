# Zep Collection - Cloud

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
| Zep Collection | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Zep Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)

**Outputs**: `Zep`

## Common Use Cases

1. Use Zep Collection - Cloud when you need upsert embedded data and perform similarity or mmr search upon query using zep, a fast and scalable building block for llm apps
2. Connect to other nodes that accept `Zep` input

---

**Source**: `packages/components/nodes/vectorstores/ZepCloud/ZepCloud.ts`