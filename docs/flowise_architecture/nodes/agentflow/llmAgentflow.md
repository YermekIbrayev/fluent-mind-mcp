# LLM

**Category**: Agent Flows | **Type**: LLM | **Version**: 1.0

---

## Overview

Large language models to analyze user-provided inputs and generate responses

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

**Outputs**: `LLM`

## Common Use Cases

1. Use LLM when you need large language models to analyze user-provided inputs and generate responses
2. Connect to other nodes that accept `LLM` input

---

**Source**: `packages/components/nodes/agentflow/LLM/LLM.ts`