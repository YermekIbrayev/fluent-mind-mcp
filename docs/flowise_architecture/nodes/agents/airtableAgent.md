# Airtable Agent

**Category**: Agents | **Type**: AgentExecutor | **Version**: 2.0

---

## Overview

Agent used to answer queries on Airtable table

## Credentials

**Required**: Yes

**Credential Types**:
- airtableApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Language Model | `BaseLanguageModel` |  | - |
| Base Id | `string` | If your table URL looks like: https://airtable.com/app11RobdGoX0YNsC/tblJdmvbrgizbYICO/viw9UrP77Id0C | - |
| Table Id | `string` | If your table URL looks like: https://airtable.com/app11RobdGoX0YNsC/tblJdmvbrgizbYICO/viw9UrP77Id0C | - |
| Return All | `boolean` | If all results should be returned or only up to a given limit | - |
| Limit | `number` | Number of results to return | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |

## Connections

**Accepts Inputs From**:
- Language Model (`BaseLanguageModel`)
- Input Moderation (`Moderation`)

**Outputs**: `AgentExecutor`

## Common Use Cases

1. Use Airtable Agent when you need agent used to answer queries on airtable table
2. Connect to other nodes that accept `AgentExecutor` input

---

**Source**: `packages/components/nodes/agents/AirtableAgent/AirtableAgent.ts`