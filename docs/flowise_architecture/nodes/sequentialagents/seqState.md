# State

**Category**: Sequential Agents | **Type**: State | **Version**: 2.0

---

## Overview

A centralized state object, updated by nodes in the graph, passing from one node to another

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Custom State | `tabs` | Structure for state. By default, state contains  | stateMemoryUI |

## Connections

**Accepts Inputs From**:
- Custom State (`tabs`)

**Outputs**: `State`

## Common Use Cases

1. Use State when you need a centralized state object, updated by nodes in the graph, passing from one node to another
2. Connect to other nodes that accept `State` input

---

**Source**: `packages/components/nodes/sequentialagents/State/State.ts`