# Epub File

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Load data from EPUB files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Epub File | `file` |  | - |
| Usage | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Epub File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Epub File when you need load data from epub files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Epub/Epub.ts`