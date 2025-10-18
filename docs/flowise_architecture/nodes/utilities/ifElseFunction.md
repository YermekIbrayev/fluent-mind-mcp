# IfElse Function

**Category**: Utilities | **Type**: IfElseFunction | **Version**: 2.0

---

## Overview

Split flows based on If Else javascript functions

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| If Function | `code` | Function must return a value | if ( |
| Else Function | `code` | Function must return a value | return false; |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Variables | `json` | Input variables can be used in the function with prefix $. For example: $var | - |
| IfElse Name | `string` |  | - |

## Connections

**Accepts Inputs From**:
- If Function (`code`)
- Else Function (`code`)

**Outputs**: `IfElseFunction`

## Common Use Cases

1. Use IfElse Function when you need split flows based on if else javascript functions
2. Connect to other nodes that accept `IfElseFunction` input

---

**Source**: `packages/components/nodes/utilities/IfElseFunction/IfElseFunction.ts`