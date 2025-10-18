# Notion Page

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from Notion Page (including child pages all as separate documents)

## Credentials

**Required**: Yes

**Credential Types**:
- notionApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Notion Page Id | `string` | The last The 32 char hex in the url path. For example: https://www.notion.so/skarard/LangChain-Notio | - |

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

1. Use Notion Page when you need load data from notion page (including child pages all as separate documents)
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Notion/NotionPage.ts`