# Chatflow Tool

**Category**: Tools | **Type**: ChatflowTool | **Version**: 5.1

---

## Overview

Use as a tool to execute another chatflow

## Credentials

**Required**: Yes

**Credential Types**:
- chatflowApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Select Chatflow | `asyncOptions` |  | - |
| Tool Name | `string` |  | - |
| Tool Description | `string` | Description of what the tool does. This is for LLM to determine when to use this tool. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Return Direct | `boolean` |  | - |
| Override Config | `json` | Override the config passed to the Chatflow. | - |
| Base URL | `string` | Base URL to Flowise. By default, it is the URL of the incoming request. Useful when you need to exec | - |
| Start new session per message | `boolean` | Whether to continue the session with the Chatflow tool or start a new one with each interaction. Use | - |
| Use Question from Chat | `boolean` | Whether to use the question from the chat as input to the chatflow. If turned on, this will override | - |
| Custom Input | `string` | Custom input to be passed to the chatflow. Leave empty to let LLM decides the input. | - |

## Connections

**Accepts Inputs From**:
- Select Chatflow (`asyncOptions`)

**Outputs**: `ChatflowTool`

## Common Use Cases

1. Use Chatflow Tool when you need use as a tool to execute another chatflow
2. Connect to other nodes that accept `ChatflowTool` input

---

**Source**: `packages/components/nodes/tools/ChatflowTool/ChatflowTool.ts`