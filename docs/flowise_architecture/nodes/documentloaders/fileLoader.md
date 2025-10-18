# File Loader

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

A generic file loader that can load different file types

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| File | `file` |  | - |
| Pdf Usage | `options` | Only when loading PDF files | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use File Loader when you need a generic file loader that can load different file types
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/File/File.ts`