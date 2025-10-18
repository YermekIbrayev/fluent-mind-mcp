# AWS ChatBedrock

**Category**: Chat Models | **Type**: AWSChatBedrock | **Version**: 6.1

---

## Overview

Wrapper around AWS Bedrock large language models that use the Converse API

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Region | `asyncOptions` |  | us-east-1 |
| Model Name | `asyncOptions` |  | anthropic.claude-3-haiku-20240307-v1:0 |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Custom Model Name | `string` | If provided, will override model selected from Model Name option | - |
| Streaming | `boolean` |  | - |
| Temperature | `number` | Temperature parameter may not apply to certain model. Please check available model parameters | - |
| Max Tokens to Sample | `number` | Max Tokens parameter may not apply to certain model. Please check available model parameters | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |
| Latency Optimized | `boolean` | Enable latency optimized configuration for supported models. Refer to the supported <a href= | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Region (`asyncOptions`)
- Model Name (`asyncOptions`)

**Outputs**: `AWSChatBedrock`

## Common Use Cases

1. Use AWS ChatBedrock when you need wrapper around aws bedrock large language models that use the converse api
2. Connect to other nodes that accept `AWSChatBedrock` input

---

**Source**: `packages/components/nodes/chatmodels/AWSBedrock/AWSChatBedrock.ts`