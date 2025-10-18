# TreeSummarize

**Category**: Response Synthesizer | **Type**: TreeSummarize | **Version**: 1.0

---

## Overview

Given a set of text chunks and the query, recursively construct a tree and return the root node as the response. Good for summarization purposes.

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Prompt | `string` |  | Context information from multiple sources is below.
---------------------
{context}
---------------------
Given the information from multiple sources and not prior knowledge, answer the query.
Query: {query}
Answer: |

## Connections

**Outputs**: `TreeSummarize`

## Common Use Cases

1. Use TreeSummarize when you need given a set of text chunks and the query, recursively construct a tree and return the root node as the response. good for summarization purposes.
2. Connect to other nodes that accept `TreeSummarize` input

---

**Source**: `packages/components/nodes/responsesynthesizer/TreeSummarize/TreeSummarize.ts`