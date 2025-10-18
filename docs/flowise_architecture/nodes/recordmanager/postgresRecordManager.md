# Postgres Record Manager

**Category**: Record Manager | **Type**: Postgres RecordManager | **Version**: 1.0

---

## Overview

Use Postgres to keep track of document writes into the vector databases

## Credentials

**Required**: Yes

**Credential Types**:
- PostgresApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Host | `string` |  | - |
| Database | `string` |  | - |
| Cleanup | `options` | Read more on the difference between different cleanup methods <a target= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Port | `number` |  | - |
| SSL | `boolean` | Use SSL to connect to Postgres | - |
| Additional Connection Configuration | `json` |  | - |
| Table Name | `string` |  | - |
| Namespace | `string` | If not specified, chatflowid will be used | - |

## Connections

**Outputs**: `Postgres RecordManager`

## Common Use Cases

1. Use Postgres Record Manager when you need use postgres to keep track of document writes into the vector databases
2. Connect to other nodes that accept `Postgres RecordManager` input

---

**Source**: `packages/components/nodes/recordmanager/PostgresRecordManager/PostgresRecordManager.ts`