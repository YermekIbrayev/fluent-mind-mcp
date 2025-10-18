# Condition Agent

**Category**: Agent Flows | **Type**: ConditionAgent | **Version**: 1.1

---

## Overview

Utilize an agent to split flows based on dynamic conditions

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `asyncOptions` |  | - |
| Instructions | `string` | A general instructions of what the condition agent should do | - |
| Input | `string` | Input to be used for the condition agent | <p><span class= |
| Scenarios | `array` | Define the scenarios that will be used as the conditions to split the flow | - |

## Connections

**Accepts Inputs From**:
- Model (`asyncOptions`)
- Scenarios (`array`)

**Outputs**: `ConditionAgent`

## Common Use Cases

1. Use Condition Agent when you need utilize an agent to split flows based on dynamic conditions
2. Connect to other nodes that accept `ConditionAgent` input

---

**Source**: `packages/components/nodes/agentflow/ConditionAgent/ConditionAgent.ts`