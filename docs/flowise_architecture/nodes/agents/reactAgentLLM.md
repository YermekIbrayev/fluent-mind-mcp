# ReAct Agent for LLMs

**Category**: Agents | **Type**: AgentExecutor | **Version**: 2.0

---

## Overview

Agent that uses the ReAct logic to decide what action to take, optimized to be used with LLMs

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Allowed Tools | `Tool` |  | - |
| Language Model | `BaseLanguageModel` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |
| Max Iterations | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Allowed Tools (`Tool`)
- Language Model (`BaseLanguageModel`)
- Input Moderation (`Moderation`)

**Outputs**: `AgentExecutor`

## Common Use Cases

1. Use ReAct Agent for LLMs when you need agent that uses the react logic to decide what action to take, optimized to be used with llms
2. Connect to other nodes that accept `AgentExecutor` input

---

**Source**: `packages/components/nodes/agents/ReActAgentLLM/ReActAgentLLM.ts`