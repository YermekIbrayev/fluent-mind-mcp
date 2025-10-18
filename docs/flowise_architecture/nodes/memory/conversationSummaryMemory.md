# Conversation Summary Memory

**Category**: Memory | **Type**: ConversationSummaryMemory | **Version**: 2.0

---

## Overview

Summarizes the conversation and stores the current summary in memory

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel` |  | - |
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Accepts Inputs From**:
- Chat Model (`BaseChatModel`)

**Outputs**: `ConversationSummaryMemory`

## Common Use Cases

1. Use Conversation Summary Memory when you need summarizes the conversation and stores the current summary in memory
2. Connect to other nodes that accept `ConversationSummaryMemory` input

---

**Source**: `packages/components/nodes/memory/ConversationSummaryMemory/ConversationSummaryMemory.ts`