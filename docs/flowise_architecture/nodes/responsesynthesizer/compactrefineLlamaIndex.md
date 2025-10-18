# Compact and Refine

**Category**: Response Synthesizer | **Type**: CompactRefine | **Version**: 1.0

---

## Overview

CompactRefine is a slight variation of Refine that first compacts the text chunks into the smallest possible number of chunks.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Refine Prompt | `string` |  | The original query is as follows: {query}
We have provided an existing answer: {existingAnswer}
We have the opportunity to refine the existing answer (only if needed) with some more context below.
------------
{context}
------------
Given the new context, refine the original answer to better answer the query. If the context isn |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text QA Prompt | `string` |  | Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {query}
Answer: |

## Connections

**Outputs**: `CompactRefine`

## Common Use Cases

1. Use Compact and Refine when you need compactrefine is a slight variation of refine that first compacts the text chunks into the smallest possible number of chunks.
2. Connect to other nodes that accept `CompactRefine` input

---

**Source**: `packages/components/nodes/responsesynthesizer/CompactRefine/CompactRefine.ts`