# CSV Agent

**Category**: Agents | **Type**: AgentExecutor | **Version**: 3.0

---

## Overview

Agent used to answer queries on CSV data

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Csv File | `file` |  | - |
| Language Model | `BaseLanguageModel` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| System Message | `string` |  | - |
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |
| Custom Pandas Read_CSV Code | `code` | Custom Pandas <a target= | read_csv(csv_data) |

## Connections

**Accepts Inputs From**:
- Csv File (`file`)
- Language Model (`BaseLanguageModel`)
- Input Moderation (`Moderation`)
- Custom Pandas Read_CSV Code (`code`)

**Outputs**: `AgentExecutor`

## Common Use Cases

1. Use CSV Agent when you need agent used to answer queries on csv data
2. Connect to other nodes that accept `AgentExecutor` input

---

**Source**: `packages/components/nodes/agents/CSVAgent/CSVAgent.ts`