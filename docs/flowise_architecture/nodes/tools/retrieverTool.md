# Retriever Tool

**Category**: Tools | **Type**: RetrieverTool | **Version**: 3.0

---

## Overview

Use a retriever as allowed tool for agent

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Retriever Name | `string` |  | - |
| Retriever Description | `string` | When should agent uses to retrieve documents | - |
| Retriever | `BaseRetriever` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Return Source Documents | `boolean` |  | - |
| Additional Metadata Filter | `json` | Add additional metadata filter on top of the existing filter from vector store | - |

## Connections

**Accepts Inputs From**:
- Retriever (`BaseRetriever`)

**Outputs**: `RetrieverTool`

## Common Use Cases

1. Use Retriever Tool when you need use a retriever as allowed tool for agent
2. Connect to other nodes that accept `RetrieverTool` input

---

**Source**: `packages/components/nodes/tools/RetrieverTool/RetrieverTool.ts`