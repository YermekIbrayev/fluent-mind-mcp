# Folder with Files

**Category**: Document Loaders | **Type**: Document | **Version**: 4.0

---

## Overview

Load data from folder with multiple files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Folder Path | `string` |  | - |
| Recursive | `boolean` |  | - |
| Pdf Usage | `options` | Only when loading PDF files | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Folder with Files when you need load data from folder with multiple files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Folder/Folder.ts`