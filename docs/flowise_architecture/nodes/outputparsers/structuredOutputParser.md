# Structured Output Parser

**Category**: null | **Type**: StructuredOutputParser | **Version**: 1.0

---

## Overview

Parse the output of an LLM call into a given (JSON) structure.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| JSON Structure | `datagrid` | JSON structure for LLM to return | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Autofix | `boolean` | In the event that the first call fails, will make another call to the model to fix any errors. | - |

## Connections

**Accepts Inputs From**:
- JSON Structure (`datagrid`)

**Outputs**: `StructuredOutputParser`

## Common Use Cases

1. Use Structured Output Parser when you need parse the output of an llm call into a given (json) structure.
2. Connect to other nodes that accept `StructuredOutputParser` input

---

**Source**: `packages/components/nodes/outputparsers/StructuredOutputParser/StructuredOutputParser.ts`