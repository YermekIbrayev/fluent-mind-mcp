# Apify Website Content Crawler

**Category**: Document Loaders | **Type**: Document | **Version**: 3.0

---

## Overview

Load data from Apify Website Content Crawler

## Credentials

**Required**: Yes

**Credential Types**:
- apifyApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Start URLs | `string` | One or more URLs of pages where the crawler will start, separated by commas. | - |
| Crawler type | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Apify Website Content Crawler when you need load data from apify website content crawler
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/ApifyWebsiteContentCrawler/ApifyWebsiteContentCrawler.ts`