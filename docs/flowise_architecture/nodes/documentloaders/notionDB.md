# Notion Database

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from Notion Database (each row is a separate document with all properties as metadata)

## Credentials

**Required**: Yes

**Credential Types**:
- notionApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Notion Database Id | `string` | If your URL looks like - https://www.notion.so/abcdefh?v=long_hash_2, then abcdefh is the database I | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Notion Database when you need load data from notion database (each row is a separate document with all properties as metadata)
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Notion/NotionDB.ts`