# Github

**Category**: Document Loaders | **Type**: Document | **Version**: 3.0

---

## Overview

Load data from a GitHub repository

## Credentials

**Required**: Yes

**Credential Types**:
- githubApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Repo Link | `string` |  | - |
| Branch | `string` |  | main |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Recursive | `boolean` |  | - |
| Max Concurrency | `number` |  | - |
| Github Base URL | `string` | Custom Github Base Url (e.g. Enterprise) | - |
| Github Instance API | `string` | Custom Github API Url (e.g. Enterprise) | - |
| Ignore Paths | `string` | An array of paths to be ignored | - |
| Max Retries | `number` | The maximum number of retries that can be made for a single call, with an exponential backoff betwee | - |
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Github when you need load data from a github repository
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Github/Github.ts`