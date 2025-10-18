# HtmlToMarkdown Text Splitter

**Category**: Text Splitters | **Type**: HtmlToMarkdownTextSplitter | **Version**: 1.0

---

## Overview

Converts Html to Markdown and then split your content into documents based on the Markdown headers

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chunk Size | `number` | Number of characters in each chunk. Default is 1000. | - |
| Chunk Overlap | `number` | Number of characters to overlap between chunks. Default is 200. | - |

## Connections

**Outputs**: `HtmlToMarkdownTextSplitter`

## Common Use Cases

1. Use HtmlToMarkdown Text Splitter when you need converts html to markdown and then split your content into documents based on the markdown headers
2. Connect to other nodes that accept `HtmlToMarkdownTextSplitter` input

---

**Source**: `packages/components/nodes/textsplitters/HtmlToMarkdownTextSplitter/HtmlToMarkdownTextSplitter.ts`