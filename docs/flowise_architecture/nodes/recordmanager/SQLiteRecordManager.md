# SQLite Record Manager

**Category**: Record Manager | **Type**: SQLite RecordManager | **Version**: 1.1

---

## Overview

Use SQLite to keep track of document writes into the vector databases

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cleanup | `options` | Read more on the difference between different cleanup methods <a target= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Database File Path | `string` |  | - |
| Table Name | `string` |  | - |
| Namespace | `string` | If not specified, chatflowid will be used | - |

## Connections

**Outputs**: `SQLite RecordManager`

## Common Use Cases

1. Use SQLite Record Manager when you need use sqlite to keep track of document writes into the vector databases
2. Connect to other nodes that accept `SQLite RecordManager` input

---

**Source**: `packages/components/nodes/recordmanager/SQLiteRecordManager/SQLiteRecordManager.ts`