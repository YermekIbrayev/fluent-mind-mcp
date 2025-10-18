# AWS Kendra

**Category**: Vector Stores | **Type**: Kendra | **Version**: 1.0

---

## Overview

Use AWS Kendra

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Region | `asyncOptions` |  | us-east-1 |
| Kendra Index ID | `string` | The ID of your AWS Kendra index | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| File Upload | `boolean` | Allow file upload on the chat | - |
| Top K | `number` | Number of top results to fetch. Default to 10 | - |
| Attribute Filter | `json` | Optional filter to apply when retrieving documents | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Region (`asyncOptions`)

**Outputs**: `Kendra`

## Common Use Cases

1. Use AWS Kendra when you need use aws kendra
2. Connect to other nodes that accept `Kendra` input

---

**Source**: `packages/components/nodes/vectorstores/Kendra/Kendra.ts`