# Agent as Tool

**Category**: Tools | **Type**: AgentAsTool | **Version**: 1.0

---

## Overview

Use as a tool to execute another agentflow

## Credentials

**Required**: Yes

**Credential Types**:
- agentflowApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Select Agent | `asyncOptions` |  | - |
| Tool Name | `string` |  | - |
| Tool Description | `string` | Description of what the tool does. This is for LLM to determine when to use this tool. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Return Direct | `boolean` |  | - |
| Override Config | `json` | Override the config passed to the Agentflow. | - |
| Base URL | `string` | Base URL to Flowise. By default, it is the URL of the incoming request. Useful when you need to exec | - |
| Start new session per message | `boolean` | Whether to continue the session with the Agentflow tool or start a new one with each interaction. Us | - |
| Use Question from Chat | `boolean` | Whether to use the question from the chat as input to the agentflow. If turned on, this will overrid | - |
| Custom Input | `string` | Custom input to be passed to the agentflow. Leave empty to let LLM decides the input. | - |

## Connections

**Accepts Inputs From**:
- Select Agent (`asyncOptions`)

**Outputs**: `AgentAsTool`

## Common Use Cases

1. Use Agent as Tool when you need use as a tool to execute another agentflow
2. Connect to other nodes that accept `AgentAsTool` input

---

**Source**: `packages/components/nodes/tools/AgentAsTool/AgentAsTool.ts`