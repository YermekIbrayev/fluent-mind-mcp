# Conversation Summary Buffer Memory

**Category**: Memory | **Type**: ConversationSummaryBufferMemory | **Version**: 1.0

---

## Overview

Uses token length to decide when to summarize conversations

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel` |  | - |
| Max Token Limit | `number` | Summarize conversations once token limit is reached. Default to 2000 | - |
| Memory Key | `string` |  | chat_history |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Session Id | `string` | If not specified, a random id will be used. Learn <a target= | - |

## Connections

**Accepts Inputs From**:
- Chat Model (`BaseChatModel`)

**Outputs**: `ConversationSummaryBufferMemory`

## Common Use Cases

1. Use Conversation Summary Buffer Memory when you need uses token length to decide when to summarize conversations
2. Connect to other nodes that accept `ConversationSummaryBufferMemory` input

---

**Source**: `packages/components/nodes/memory/ConversationSummaryBufferMemory/ConversationSummaryBufferMemory.ts`