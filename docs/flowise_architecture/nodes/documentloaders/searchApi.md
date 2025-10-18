# SearchApi For Web Search

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from real-time search results

## Credentials

**Required**: Yes

**Credential Types**:
- searchApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` |  | - |
| Custom Parameters | `json` |  | - |
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use SearchApi For Web Search when you need load data from real-time search results
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/SearchApi/SearchAPI.ts`