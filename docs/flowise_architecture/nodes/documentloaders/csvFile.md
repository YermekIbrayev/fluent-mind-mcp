# Csv File

**Category**: Document Loaders | **Type**: Document | **Version**: 3.0

---

## Overview

Load data from CSV files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Csv File | `file` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Single Column Extraction | `string` | Extracting a single column | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Csv File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Csv File when you need load data from csv files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Csv/Csv.ts`