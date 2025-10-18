# Custom Function

**Category**: Agent Flows | **Type**: CustomFunction | **Version**: 1.0

---

## Overview

Execute custom function

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Variable Value | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Variables | `array` | Input variables can be used in the function with prefix $. For example: $foo | - |

## Connections

**Accepts Inputs From**:
- Input Variables (`array`)

**Outputs**: `CustomFunction`

## Common Use Cases

1. Use Custom Function when you need execute custom function
2. Connect to other nodes that accept `CustomFunction` input

---

**Source**: `packages/components/nodes/agentflow/CustomFunction/CustomFunction.ts`