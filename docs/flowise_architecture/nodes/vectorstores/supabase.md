# Supabase

**Category**: Vector Stores | **Type**: Supabase | **Version**: 4.0

---

## Overview

Upsert embedded data and perform similarity or mmr search upon query using Supabase via pgvector extension

## Credentials

**Required**: Yes

**Credential Types**:
- supabaseApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Supabase Project URL | `string` |  | - |
| Table Name | `string` |  | - |
| Query Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| Supabase Metadata Filter | `json` |  | - |
| Supabase RPC Filter | `string` | Query builder-style filtering. If this is set, will override the metadata filter. Refer <a href= | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Supabase`

## Common Use Cases

1. Use Supabase when you need upsert embedded data and perform similarity or mmr search upon query using supabase via pgvector extension
2. Connect to other nodes that accept `Supabase` input

---

**Source**: `packages/components/nodes/vectorstores/Supabase/Supabase.ts`