# Oxylabs

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Extract data from URLs using Oxylabs

## Credentials

**Required**: Yes

**Credential Types**:
- oxylabsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Query | `string` | Website URL of query keyword. | - |
| Source | `options` | Target website to scrape. | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Oxylabs when you need extract data from urls using oxylabs
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Oxylabs/Oxylabs.ts`