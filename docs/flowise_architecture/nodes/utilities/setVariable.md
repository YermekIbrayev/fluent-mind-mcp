# Set Variable

**Category**: Utilities | **Type**: SetVariable | **Version**: 2.1

---

## Overview

Set variable which can be retrieved at a later stage. Variable is only available during runtime.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Variable Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input | `string | number | boolean | json | array` |  | - |
| Show Output | `boolean` | Show the output result in the Prediction API response | - |

## Connections

**Accepts Inputs From**:
- Input (`string | number | boolean | json | array`)

**Outputs**: `SetVariable`

## Common Use Cases

1. Use Set Variable when you need set variable which can be retrieved at a later stage. variable is only available during runtime.
2. Connect to other nodes that accept `SetVariable` input

---

**Source**: `packages/components/nodes/utilities/SetVariable/SetVariable.ts`