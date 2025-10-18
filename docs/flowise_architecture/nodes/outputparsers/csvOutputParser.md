# CSV Output Parser

**Category**: null | **Type**: CSVListOutputParser | **Version**: 1.0

---

## Overview

Parse the output of an LLM call as a comma-separated list of values

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Autofix | `boolean` | In the event that the first call fails, will make another call to the model to fix any errors. | - |

## Connections

**Outputs**: `CSVListOutputParser`

## Common Use Cases

1. Use CSV Output Parser when you need parse the output of an llm call as a comma-separated list of values
2. Connect to other nodes that accept `CSVListOutputParser` input

---

**Source**: `packages/components/nodes/outputparsers/CSVListOutputParser/CSVListOutputParser.ts`