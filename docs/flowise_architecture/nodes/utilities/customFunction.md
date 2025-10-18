# Custom JS Function

**Category**: Utilities | **Type**: CustomFunction | **Version**: 3.0

---

## Overview

Execute custom javascript function

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Javascript Function | `code` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Variables | `json` | Input variables can be used in the function with prefix $. For example: $var | - |
| Function Name | `string` |  | - |
| Additional Tools | `Tool` | Tools can be used in the function with $tools.{tool_name}.invoke(args) | - |

## Connections

**Accepts Inputs From**:
- Additional Tools (`Tool`)
- Javascript Function (`code`)

**Outputs**: `CustomFunction`

## Common Use Cases

1. Use Custom JS Function when you need execute custom javascript function
2. Connect to other nodes that accept `CustomFunction` input

---

**Source**: `packages/components/nodes/utilities/CustomFunction/CustomFunction.ts`