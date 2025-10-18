# GitBook

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from GitBook

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Web Path | `string` | If want to load all paths from the GitBook provide only root path e.g.https://docs.gitbook.com/  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Should Load All Paths | `boolean` | Load from all paths in a given GitBook | - |
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use GitBook when you need load data from gitbook
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Gitbook/Gitbook.ts`