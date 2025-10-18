# Markdown Text Splitter

**Category**: Text Splitters | **Type**: MarkdownTextSplitter | **Version**: 1.1

---

## Overview

Split your content into documents based on the Markdown headers

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Split by Headers | `options` | Split documents at specified header levels. Headers will be included with their content. | disabled |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chunk Size | `number` | Number of characters in each chunk. Default is 1000. | - |
| Chunk Overlap | `number` | Number of characters to overlap between chunks. Default is 200. | - |

## Connections

**Outputs**: `MarkdownTextSplitter`

## Common Use Cases

1. Use Markdown Text Splitter when you need split your content into documents based on the markdown headers
2. Connect to other nodes that accept `MarkdownTextSplitter` input

---

**Source**: `packages/components/nodes/textsplitters/MarkdownTextSplitter/MarkdownTextSplitter.ts`