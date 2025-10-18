# Unstructured File Loader

**Category**: Document Loaders | **Type**: Document | **Version**: 4.0

---

## Overview

Use Unstructured.io to load data from a file path

## Credentials

**Required**: Yes

**Credential Types**:
- unstructuredApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Unstructured API URL | `string` | Unstructured API URL. Read <a target= | - |
| Strategy | `options` | The strategy to use for partitioning PDF/image. Options are fast, hi_res, auto. Default: auto. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| File Path | `string` | Files to be processed. Multiple files can be uploaded. | - |

## Connections

**Outputs**: `Document`

## Common Use Cases

1. Use Unstructured File Loader when you need use unstructured.io to load data from a file path
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Unstructured/UnstructuredFile.ts`