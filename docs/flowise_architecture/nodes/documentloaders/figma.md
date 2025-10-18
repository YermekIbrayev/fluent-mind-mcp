# Figma

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from a Figma file

## Credentials

**Required**: Yes

**Credential Types**:
- figmaApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| File Key | `string` | The file key can be read from any Figma file URL: https://www.figma.com/file/:key/:title. For exampl | - |
| Node IDs | `string` | A list of Node IDs, seperated by comma. Refer to <a target= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Recursive | `boolean` |  | - |
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Figma when you need load data from a figma file
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Figma/Figma.ts`