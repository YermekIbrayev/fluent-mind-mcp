# Loop

**Category**: Agent Flows | **Type**: Loop | **Version**: 1.1

---

## Overview

Loop back to a previous node

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Loop Back To | `asyncOptions` |  | - |
| Max Loop Count | `number` |  | - |
| Value | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Fallback Message | `string` | Message to display if the loop count is exceeded | - |
| Update Flow State | `array` | Update runtime state during the execution of the workflow | - |

## Connections

**Accepts Inputs From**:
- Loop Back To (`asyncOptions`)
- Update Flow State (`array`)

**Outputs**: `Loop`

## Common Use Cases

1. Use Loop when you need loop back to a previous node
2. Connect to other nodes that accept `Loop` input

---

**Source**: `packages/components/nodes/agentflow/Loop/Loop.ts`