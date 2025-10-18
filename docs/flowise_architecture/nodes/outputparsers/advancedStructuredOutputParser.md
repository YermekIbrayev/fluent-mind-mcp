# Advanced Structured Output Parser

**Category**: null | **Type**: AdvancedStructuredOutputParser | **Version**: 1.0

---

## Overview

Parse the output of an LLM call into a given structure by providing a Zod schema.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Example JSON | `string` | Zod schema for the output of the model | z.object({
    title: z.string(), // Title of the movie as a string
    yearOfRelease: z.number().int(), // Release year as an integer number,
    genres: z.enum([
         |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Autofix | `boolean` | In the event that the first call fails, will make another call to the model to fix any errors. | - |

## Connections

**Outputs**: `AdvancedStructuredOutputParser`

## Common Use Cases

1. Use Advanced Structured Output Parser when you need parse the output of an llm call into a given structure by providing a zod schema.
2. Connect to other nodes that accept `AdvancedStructuredOutputParser` input

---

**Source**: `packages/components/nodes/outputparsers/StructuredOutputParserAdvanced/StructuredOutputParserAdvanced.ts`