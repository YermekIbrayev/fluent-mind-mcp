# ChatGroq

**Category**: Chat Models | **Type**: ChatGroq | **Version**: 1.0

---

## Overview

Wrapper around Groq LLM specific for LlamaIndex

## Credentials

**Required**: Yes

**Credential Types**:
- groqApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `ChatGroq`

## Common Use Cases

1. Use ChatGroq when you need wrapper around groq llm specific for llamaindex
2. Connect to other nodes that accept `ChatGroq` input

---

**Source**: `packages/components/nodes/chatmodels/Groq/ChatGroq_LlamaIndex.ts`