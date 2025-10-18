# GroqChat

**Category**: Chat Models | **Type**: GroqChat | **Version**: 4.0

---

## Overview

Wrapper around Groq API with LPU Inference Engine

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
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Streaming | `boolean` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `GroqChat`

## Common Use Cases

1. Use GroqChat when you need wrapper around groq api with lpu inference engine
2. Connect to other nodes that accept `GroqChat` input

---

**Source**: `packages/components/nodes/chatmodels/Groq/Groq.ts`