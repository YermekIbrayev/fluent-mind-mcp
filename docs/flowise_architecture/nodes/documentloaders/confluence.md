# Confluence

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from a Confluence Document

## Credentials

**Required**: Yes

**Credential Types**:
- confluenceCloudApi
- confluenceServerDCApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base URL | `string` |  | - |
| Space Key | `string` | Refer to <a target= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Limit | `number` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Confluence when you need load data from a confluence document
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Confluence/Confluence.ts`