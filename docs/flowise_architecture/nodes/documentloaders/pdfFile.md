# Pdf File

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from PDF files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Pdf File | `file` |  | - |
| Usage | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Pdf File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Pdf File when you need load data from pdf files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Pdf/Pdf.ts`