# Recursive Character Text Splitter

**Category**: Text Splitters | **Type**: RecursiveCharacterTextSplitter | **Version**: 2.0

---

## Overview

Split documents recursively by different characters - starting with 

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chunk Size | `number` | Number of characters in each chunk. Default is 1000. | - |
| Chunk Overlap | `number` | Number of characters to overlap between chunks. Default is 200. | - |
| Custom Separators | `string` | Array of custom separators to determine when to split the text, will override the default separators | - |

## Connections

**Outputs**: `RecursiveCharacterTextSplitter`

## Common Use Cases

1. Use Recursive Character Text Splitter when you need split documents recursively by different characters - starting with 
2. Connect to other nodes that accept `RecursiveCharacterTextSplitter` input

---

**Source**: `packages/components/nodes/textsplitters/RecursiveCharacterTextSplitter/RecursiveCharacterTextSplitter.ts`