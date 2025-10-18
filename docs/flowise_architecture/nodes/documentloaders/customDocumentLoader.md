# Custom Document Loader

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Custom function for loading documents

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Javascript Function | `code` | Must return an array of document objects containing metadata and pageContent if  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Variables | `json` | Input variables can be used in the function with prefix $. For example: $var | - |

## Connections

**Accepts Inputs From**:
- Javascript Function (`code`)

**Outputs**: `Document`

## Common Use Cases

1. Use Custom Document Loader when you need custom function for loading documents
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/CustomDocumentLoader/CustomDocumentLoader.ts`