# Requests Delete

**Category**: Tools | **Type**: RequestsDelete | **Version**: 1.0

---

## Overview

Execute HTTP DELETE requests

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| URL | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Name | `string` | Name of the tool | requests_delete |
| Description | `string` | Describe to LLM when it should use this tool | - |
| Headers | `string` |  | - |
| Query Params Schema | `code` | Description of the available query params to enable LLM to figure out which query params to use | - |
| Max Output Length | `number` | Max length of the output. Remove this if you want to return the entire response | 2000 |

## Connections

**Accepts Inputs From**:
- Query Params Schema (`code`)

**Outputs**: `RequestsDelete`

## Common Use Cases

1. Use Requests Delete when you need execute http delete requests
2. Connect to other nodes that accept `RequestsDelete` input

---

**Source**: `packages/components/nodes/tools/RequestsDelete/RequestsDelete.ts`