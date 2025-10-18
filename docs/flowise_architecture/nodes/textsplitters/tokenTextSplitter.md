# Token Text Splitter

**Category**: Text Splitters | **Type**: TokenTextSplitter | **Version**: 1.0

---

## Overview

Splits a raw text string by first converting the text into BPE tokens, then split these tokens into chunks and convert the tokens within a single chunk back into text.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Encoding Name | `options` |  | - |

## Connections

**Outputs**: `TokenTextSplitter`

## Common Use Cases

1. Use Token Text Splitter when you need splits a raw text string by first converting the text into bpe tokens, then split these tokens into chunks and convert the tokens within a single chunk back into text.
2. Connect to other nodes that accept `TokenTextSplitter` input

---

**Source**: `packages/components/nodes/textsplitters/TokenTextSplitter/TokenTextSplitter.ts`