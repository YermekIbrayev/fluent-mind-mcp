# MySQL Record Manager

**Category**: Record Manager | **Type**: MySQL RecordManager | **Version**: 1.0

---

## Overview

Use MySQL to keep track of document writes into the vector databases

## Credentials

**Required**: Yes

**Credential Types**:
- MySQLApi

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
| Additional Connection Configuration | `json` |  | - |
| Table Name | `string` |  | - |
| Namespace | `string` | If not specified, chatflowid will be used | - |

## Connections

**Outputs**: `MySQL RecordManager`

## Common Use Cases

1. Use MySQL Record Manager when you need use mysql to keep track of document writes into the vector databases
2. Connect to other nodes that accept `MySQL RecordManager` input

---

**Source**: `packages/components/nodes/recordmanager/MySQLRecordManager/MySQLrecordManager.ts`