# Custom List Output Parser

**Category**: null | **Type**: CustomListOutputParser | **Version**: 1.0

---

## Overview

Parse the output of an LLM call as a list of values.

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Length | `number` | Number of values to return | - |
| Separator | `string` | Separator between values | , |
| Autofix | `boolean` | In the event that the first call fails, will make another call to the model to fix any errors. | - |

## Connections

**Outputs**: `CustomListOutputParser`

## Common Use Cases

1. Use Custom List Output Parser when you need parse the output of an llm call as a list of values.
2. Connect to other nodes that accept `CustomListOutputParser` input

---

**Source**: `packages/components/nodes/outputparsers/CustomListOutputParser/CustomListOutputParser.ts`