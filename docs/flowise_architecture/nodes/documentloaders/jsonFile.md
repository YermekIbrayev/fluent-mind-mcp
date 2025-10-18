# Json File

**Category**: Document Loaders | **Type**: Document | **Version**: 3.0

---

## Overview

Load data from JSON files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Json File | `file` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Pointers Extraction (separated by commas) | `string` | Ex: {  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents. You can add metadata dynamically from th | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Json File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Json File when you need load data from json files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Json/Json.ts`