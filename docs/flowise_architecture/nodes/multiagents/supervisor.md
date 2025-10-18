# Supervisor

**Category**: Multi Agents | **Type**: Supervisor | **Version**: 3.0

---

## Overview

No description available.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Supervisor Name | `string` |  | Supervisor |
| Supervisor Prompt | `string` | Prompt must contains {team_members} | - |
| Tool Calling Chat Model | `BaseChatModel` | Only compatible with models that are capable of function calling: ChatOpenAI, ChatMistral, ChatAnthr | - |
| Recursion Limit | `number` | Maximum number of times a call can recurse. If not provided, defaults to 100. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Agent Memory | `BaseCheckpointSaver` | Save the state of the agent | - |
| Summarization | `boolean` | Return final output as a summarization of the conversation | - |
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |

## Connections

**Accepts Inputs From**:
- Tool Calling Chat Model (`BaseChatModel`)
- Agent Memory (`BaseCheckpointSaver`)
- Input Moderation (`Moderation`)

**Outputs**: `Supervisor`

## Common Use Cases

1. Use Supervisor when you need this functionality
2. Connect to other nodes that accept `Supervisor` input

---

**Source**: `packages/components/nodes/multiagents/Supervisor/Supervisor.ts`