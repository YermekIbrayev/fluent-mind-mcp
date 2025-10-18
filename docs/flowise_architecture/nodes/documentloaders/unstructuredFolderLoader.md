# Unstructured Folder Loader

**Category**: Document Loaders | **Type**: Document | **Version**: 3.0

---

## Overview

Use Unstructured.io to load data from a folder. Note: Currently doesn

## Credentials

**Required**: Yes

**Credential Types**:
- unstructuredApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Folder Path | `string` |  | - |
| Unstructured API URL | `string` | Unstructured API URL. Read <a target= | - |
| Strategy | `options` | The strategy to use for partitioning PDF/image. Options are fast, hi_res, auto. Default: auto. | - |

## Connections

**Outputs**: `Document`

## Common Use Cases

1. Use Unstructured Folder Loader when you need use unstructured.io to load data from a folder. note: currently doesn
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Unstructured/UnstructuredFolder.ts`