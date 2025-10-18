# Jira

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Load issues from Jira

## Credentials

**Required**: Yes

**Credential Types**:
- jiraApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Host | `string` |  | - |
| Project Key | `string` |  | main |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Limit per request | `number` |  | - |
| Created after | `string` |  | - |
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Jira when you need load issues from jira
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Jira/Jira.ts`