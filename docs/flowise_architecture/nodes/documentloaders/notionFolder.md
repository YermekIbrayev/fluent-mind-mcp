# Notion Folder

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from the exported and unzipped Notion folder

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Notion Folder | `string` | Get folder path | - |

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

1. Use Notion Folder when you need load data from the exported and unzipped notion folder
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Notion/NotionFolder.ts`