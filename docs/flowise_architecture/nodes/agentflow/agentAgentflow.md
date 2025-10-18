# Agent

**Category**: Agent Flows | **Type**: Agent | **Version**: 2.2

---

## Overview

Dynamically choose and utilize tools during runtime, enabling multi-step reasoning

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `asyncOptions` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Messages | `array` |  | - |

## Connections

**Accepts Inputs From**:
- Model (`asyncOptions`)
- Messages (`array`)

**Outputs**: `Agent`

## Common Use Cases

1. Use Agent when you need dynamically choose and utilize tools during runtime, enabling multi-step reasoning
2. Connect to other nodes that accept `Agent` input

---

**Source**: `packages/components/nodes/agentflow/Agent/Agent.ts`