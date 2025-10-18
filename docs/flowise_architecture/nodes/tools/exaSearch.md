# Exa Search

**Category**: Tools | **Type**: ExaSearch | **Version**: 1.1

---

## Overview

Wrapper around Exa Search API - search engine fully designed for use by LLMs

## Credentials

**Required**: Yes

**Credential Types**:
- exaSearchApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Tool Description | `string` | Description of what the tool does. This is for LLM to determine when to use this tool. | - |
| Search Type | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Num of Results | `number` | Number of search results to return. Default 10. Max 10 for basic plans. Up to thousands for custom p | - |

## Connections

**Outputs**: `ExaSearch`

## Common Use Cases

1. Use Exa Search when you need wrapper around exa search api - search engine fully designed for use by llms
2. Connect to other nodes that accept `ExaSearch` input

---

**Source**: `packages/components/nodes/tools/ExaSearch/ExaSearch.ts`