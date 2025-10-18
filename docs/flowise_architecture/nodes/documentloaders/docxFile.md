# Docx File

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from DOCX files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Docx File | `file` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Docx File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Docx File when you need load data from docx files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Docx/Docx.ts`