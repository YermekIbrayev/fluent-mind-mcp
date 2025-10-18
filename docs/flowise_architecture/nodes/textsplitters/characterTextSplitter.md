# Character Text Splitter

**Category**: Text Splitters | **Type**: CharacterTextSplitter | **Version**: 1.0

---

## Overview

splits only on one type of character (defaults to 

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chunk Size | `number` | Number of characters in each chunk. Default is 1000. | - |
| Chunk Overlap | `number` | Number of characters to overlap between chunks. Default is 200. | - |
| Custom Separator | `string` | Separator to determine when to split the text, will override the default separator | - |

## Connections

**Outputs**: `CharacterTextSplitter`

## Common Use Cases

1. Use Character Text Splitter when you need splits only on one type of character (defaults to 
2. Connect to other nodes that accept `CharacterTextSplitter` input

---

**Source**: `packages/components/nodes/textsplitters/CharacterTextSplitter/CharacterTextSplitter.ts`