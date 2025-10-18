# Multi Query Retriever

**Category**: Retrievers | **Type**: MultiQueryRetriever | **Version**: 1.0

---

## Overview

Generate multiple queries from different perspectives for a given user input query

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store | `VectorStore` |  | - |
| Language Model | `BaseLanguageModel` |  | - |
| Prompt | `string` | Prompt for the language model to generate alternative questions. Use {question} to refer to the orig | - |

## Connections

**Accepts Inputs From**:
- Vector Store (`VectorStore`)
- Language Model (`BaseLanguageModel`)

**Outputs**: `MultiQueryRetriever`

## Common Use Cases

1. Use Multi Query Retriever when you need generate multiple queries from different perspectives for a given user input query
2. Connect to other nodes that accept `MultiQueryRetriever` input

---

**Source**: `packages/components/nodes/retrievers/MultiQueryRetriever/MultiQueryRetriever.ts`