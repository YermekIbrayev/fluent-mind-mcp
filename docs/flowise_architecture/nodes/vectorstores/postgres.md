# Postgres

**Category**: Vector Stores | **Type**: Postgres | **Version**: 7.0

---

## Overview

Upsert embedded data and perform similarity search upon query using pgvector on Postgres

## Credentials

**Required**: Yes

**Credential Types**:
- PostgresApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Host | `string` |  | - |
| Database | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| Port | `number` |  | - |
| SSL | `boolean` | Use SSL to connect to Postgres | - |
| Table Name | `string` | Different option to connect to Postgres | typeorm |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Postgres`

## Common Use Cases

1. Use Postgres when you need upsert embedded data and perform similarity search upon query using pgvector on postgres
2. Connect to other nodes that accept `Postgres` input

---

**Source**: `packages/components/nodes/vectorstores/Postgres/Postgres.ts`