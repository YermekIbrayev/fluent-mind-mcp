# SerpApi For Web Search

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load and process data from web search results

## Credentials

**Required**: Yes

**Credential Types**:
- serpApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use SerpApi For Web Search when you need load and process data from web search results
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/SerpApi/SerpAPI.ts`