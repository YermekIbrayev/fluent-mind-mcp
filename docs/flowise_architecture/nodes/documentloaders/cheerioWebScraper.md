# Cheerio Web Scraper

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Load data from webpages

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| URL | `string` |  | - |
| Get Relative Links Method | `options` | Select a method to retrieve relative links | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Cheerio Web Scraper when you need load data from webpages
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/Cheerio/Cheerio.ts`