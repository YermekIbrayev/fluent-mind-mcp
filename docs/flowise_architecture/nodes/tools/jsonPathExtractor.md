# JSON Path Extractor

**Category**: Tools | **Type**: JSONPathExtractor | **Version**: 1.0

---

## Overview

Extract values from JSON using path expressions

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| JSON Path | `string` | Path to extract. Examples: data, user.name, items[0].id | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Return Null on Error | `boolean` | Return null instead of throwing error when extraction fails | - |

## Connections

**Outputs**: `JSONPathExtractor`

## Common Use Cases

1. Use JSON Path Extractor when you need extract values from json using path expressions
2. Connect to other nodes that accept `JSONPathExtractor` input

---

**Source**: `packages/components/nodes/tools/JSONPathExtractor/JSONPathExtractor.ts`