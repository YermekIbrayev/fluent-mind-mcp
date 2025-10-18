# Prompt Retriever

**Category**: Retrievers | **Type**: PromptRetriever | **Version**: 1.0

---

## Overview

Store prompt template with name & description to be later queried by MultiPromptChain

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Prompt Name | `string` |  | - |
| Prompt Description | `string` | Description of what the prompt does and when it should be used | - |
| Prompt System Message | `string` |  | - |

## Connections

**Outputs**: `PromptRetriever`

## Common Use Cases

1. Use Prompt Retriever when you need store prompt template with name & description to be later queried by multipromptchain
2. Connect to other nodes that accept `PromptRetriever` input

---

**Source**: `packages/components/nodes/retrievers/PromptRetriever/PromptRetriever.ts`