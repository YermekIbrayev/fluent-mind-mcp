# Chain Tool

**Category**: Tools | **Type**: ChainTool | **Version**: 1.0

---

## Overview

Use a chain as allowed tool for agent

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chain Name | `string` |  | - |
| Chain Description | `string` |  | - |
| Base Chain | `BaseChain` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Return Direct | `boolean` |  | - |

## Connections

**Accepts Inputs From**:
- Base Chain (`BaseChain`)

**Outputs**: `ChainTool`

## Common Use Cases

1. Use Chain Tool when you need use a chain as allowed tool for agent
2. Connect to other nodes that accept `ChainTool` input

---

**Source**: `packages/components/nodes/tools/ChainTool/ChainTool.ts`