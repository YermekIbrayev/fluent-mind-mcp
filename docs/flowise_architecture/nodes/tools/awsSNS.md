# AWS SNS

**Category**: Tools | **Type**: AWSSNS | **Version**: 1.0

---

## Overview

Publish messages to AWS SNS topics

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| AWS Region | `options` | AWS Region where your SNS topics are located | - |
| SNS Topic | `asyncOptions` | Select the SNS topic to publish to | - |

## Connections

**Accepts Inputs From**:
- SNS Topic (`asyncOptions`)

**Outputs**: `AWSSNS`

## Common Use Cases

1. Use AWS SNS when you need publish messages to aws sns topics
2. Connect to other nodes that accept `AWSSNS` input

---

**Source**: `packages/components/nodes/tools/AWSSNS/AWSSNS.ts`