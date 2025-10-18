# S3 Directory

**Category**: Document Loaders | **Type**: Document | **Version**: 4.0

---

## Overview

Load Data from S3 Buckets

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Bucket | `string` |  | - |
| Region | `asyncOptions` |  | us-east-1 |
| Pdf Usage | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Server URL | `string` | The fully qualified endpoint of the webservice. This is only for using a custom endpoint (for exampl | - |
| Prefix | `string` | Limits the response to keys that begin with the specified prefix | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)
- Region (`asyncOptions`)

**Outputs**: `Document`

## Common Use Cases

1. Use S3 Directory when you need load data from s3 buckets
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/S3Directory/S3Directory.ts`