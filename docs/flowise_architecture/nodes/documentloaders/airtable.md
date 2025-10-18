# Airtable

**Category**: Document Loaders | **Type**: Document | **Version**: 3.02

---

## Overview

Load data from Airtable table

## Credentials

**Required**: Yes

**Credential Types**:
- airtableApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base Id | `string` | If your table URL looks like: https://airtable.com/app11RobdGoX0YNsC/tblJdmvbrgizbYICO/viw9UrP77Id0C | - |
| Table Id | `string` | If your table URL looks like: https://airtable.com/app11RobdGoX0YNsC/tblJdmvbrgizbYICO/viw9UrP77Id0C | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| View Id | `string` | If your view URL looks like: https://airtable.com/app11RobdGoX0YNsC/tblJdmvbrgizbYICO/viw9UrP77Id0CE | - |
| Include Only Fields | `string` | Comma-separated list of field names or IDs to include. If empty, then ALL fields are used. Use field | - |
| Return All | `boolean` | If all results should be returned or only up to a given limit | - |
| Limit | `number` | Number of results to return. Ignored when Return All is enabled. | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |
| Filter By Formula | `string` | A formula used to filter records. The formula will be evaluated for each record, and if the result i | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Airtable when you need load data from airtable table
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Airtable/Airtable.ts`