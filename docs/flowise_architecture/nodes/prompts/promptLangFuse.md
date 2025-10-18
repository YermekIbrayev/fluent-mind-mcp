# LangFuse Prompt Template

**Category**: Prompts | **Type**: PromptTemplate | **Version**: 1.0

---

## Overview

Fetch schema from LangFuse to represent a prompt for an LLM

## Credentials

**Required**: Yes

**Credential Types**:
- langfuseApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Prompt Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Format Prompt Values | `json` |  | - |

## Connections

**Outputs**: `PromptTemplate`

## Common Use Cases

1. Use LangFuse Prompt Template when you need fetch schema from langfuse to represent a prompt for an llm
2. Connect to other nodes that accept `PromptTemplate` input

---

**Source**: `packages/components/nodes/prompts/PromptLangfuse/PromptLangfuse.ts`