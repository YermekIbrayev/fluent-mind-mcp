# Tool

**Category**: Agent Flows | **Type**: Tool | **Version**: 1.1

---

## Overview

Tools allow LLM to interact with external systems

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Tool | `asyncOptions` |  | - |
| Tool Input Arguments | `array` |  | - |
| Input Argument Value | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Tool (`asyncOptions`)
- Tool Input Arguments (`array`)

**Outputs**: `Tool`

## Common Use Cases

1. Use Tool when you need tools allow llm to interact with external systems
2. Connect to other nodes that accept `Tool` input

---

**Source**: `packages/components/nodes/agentflow/Tool/Tool.ts`