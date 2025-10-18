# Execute Flow

**Category**: Agent Flows | **Type**: ExecuteFlow | **Version**: 1.1

---

## Overview

Execute another flow

## Credentials

**Required**: Yes

**Credential Types**:
- chatflowApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Select Flow | `asyncOptions` |  | - |
| Input | `string` |  | - |
| Return Response As | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Override Config | `json` | Override the config passed to the flow | - |
| Base URL | `string` | Base URL to Flowise. By default, it is the URL of the incoming request. Useful when you need to exec | - |

## Connections

**Accepts Inputs From**:
- Select Flow (`asyncOptions`)

**Outputs**: `ExecuteFlow`

## Common Use Cases

1. Use Execute Flow when you need execute another flow
2. Connect to other nodes that accept `ExecuteFlow` input

---

**Source**: `packages/components/nodes/agentflow/ExecuteFlow/ExecuteFlow.ts`