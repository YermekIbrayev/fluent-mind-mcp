# Refine

**Category**: Response Synthesizer | **Type**: Refine | **Version**: 1.0

---

## Overview

Create and refine an answer by sequentially going through each retrieved text chunk. This makes a separate LLM call per Node. Good for more detailed answers.

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

**Outputs**: `Refine`

## Common Use Cases

1. Use Refine when you need create and refine an answer by sequentially going through each retrieved text chunk. this makes a separate llm call per node. good for more detailed answers.
2. Connect to other nodes that accept `Refine` input

---

**Source**: `packages/components/nodes/responsesynthesizer/Refine/Refine.ts`