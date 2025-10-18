# Chat Prompt Template

**Category**: Prompts | **Type**: ChatPromptTemplate | **Version**: 2.0

---

## Overview

Schema to represent a chat prompt

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| System Message | `string` |  | - |
| Human Message | `string` | This prompt will be added at the end of the messages as human message | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Format Prompt Values | `json` |  | - |
| Messages History | `tabs` | Add messages after System Message. This is useful when you want to provide few shot examples | messageHistoryCode |

## Connections

**Accepts Inputs From**:
- Messages History (`tabs`)

**Outputs**: `ChatPromptTemplate`

## Common Use Cases

1. Use Chat Prompt Template when you need schema to represent a chat prompt
2. Connect to other nodes that accept `ChatPromptTemplate` input

---

**Source**: `packages/components/nodes/prompts/ChatPromptTemplate/ChatPromptTemplate.ts`