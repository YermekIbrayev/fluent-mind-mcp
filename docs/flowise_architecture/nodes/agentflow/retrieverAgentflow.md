# Retriever

**Category**: Agent Flows | **Type**: Retriever | **Version**: 1.0

---

## Overview

Retrieve information from vector database

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Knowledge (Document Stores) | `array` | Document stores to retrieve information from. Document stores must be upserted in advance. | - |

## Connections

**Accepts Inputs From**:
- Knowledge (Document Stores) (`array`)

**Outputs**: `Retriever`

## Common Use Cases

1. Use Retriever when you need retrieve information from vector database
2. Connect to other nodes that accept `Retriever` input

---

**Source**: `packages/components/nodes/agentflow/Retriever/Retriever.ts`