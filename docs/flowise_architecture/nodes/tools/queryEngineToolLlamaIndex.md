# QueryEngine Tool

**Category**: Tools | **Type**: QueryEngineTool | **Version**: 2.0

---

## Overview

Tool used to invoke query engine

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base QueryEngine | `BaseQueryEngine` |  | - |
| Tool Name | `string` | Tool name must be small capital letter with underscore. Ex: my_tool | - |
| Tool Description | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Base QueryEngine (`BaseQueryEngine`)

**Outputs**: `QueryEngineTool`

## Common Use Cases

1. Use QueryEngine Tool when you need tool used to invoke query engine
2. Connect to other nodes that accept `QueryEngineTool` input

---

**Source**: `packages/components/nodes/tools/QueryEngineTool/QueryEngineTool.ts`