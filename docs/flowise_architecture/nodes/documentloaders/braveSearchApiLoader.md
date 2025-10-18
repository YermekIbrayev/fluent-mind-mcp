# BraveSearch API Document Loader

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load and process data from BraveSearch results

## Credentials

**Required**: Yes

**Credential Types**:
- braveSearchApi

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

1. Use BraveSearch API Document Loader when you need load and process data from bravesearch results
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/BraveSearchAPI/BraveSearchAPI.ts`