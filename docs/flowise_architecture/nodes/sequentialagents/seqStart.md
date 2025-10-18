# Start

**Category**: Sequential Agents | **Type**: Start | **Version**: 2.0

---

## Overview

Starting point of the conversation

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel` | Only compatible with models that are capable of function calling: ChatOpenAI, ChatMistral, ChatAnthr | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Agent Memory | `BaseCheckpointSaver` | Save the state of the agent | - |
| State | `State` | State is an object that is updated by nodes in the graph, passing from one node to another. By defau | - |
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |

## Connections

**Accepts Inputs From**:
- Chat Model (`BaseChatModel`)
- Agent Memory (`BaseCheckpointSaver`)
- State (`State`)
- Input Moderation (`Moderation`)

**Outputs**: `Start`

## Common Use Cases

1. Use Start when you need starting point of the conversation
2. Connect to other nodes that accept `Start` input

---

**Source**: `packages/components/nodes/sequentialagents/Start/Start.ts`