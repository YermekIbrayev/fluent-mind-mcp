# FireCrawl

**Category**: Document Loaders | **Type**: Document | **Version**: 4.0

---

## Overview

Load data from URL using FireCrawl

## Credentials

**Required**: Yes

**Credential Types**:
- fireCrawlApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Type | `options` | Crawl a URL and all accessible subpages | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use FireCrawl when you need load data from url using firecrawl
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/FireCrawl/FireCrawl.ts`