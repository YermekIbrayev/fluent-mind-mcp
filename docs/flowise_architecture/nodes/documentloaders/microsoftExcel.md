# Microsoft Excel

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Load data from Microsoft Excel files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Excel File | `file` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Excel File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Microsoft Excel when you need load data from microsoft excel files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/MicrosoftExcel/MicrosoftExcel.ts`