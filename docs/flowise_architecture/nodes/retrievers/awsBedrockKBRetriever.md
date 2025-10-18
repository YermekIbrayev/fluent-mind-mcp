# AWS Bedrock Knowledge Base Retriever

**Category**: Retrievers | **Type**: AWSBedrockKBRetriever | **Version**: 1.0

---

## Overview

Connect to AWS Bedrock Knowledge Base API and retrieve relevant chunks

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Region | `asyncOptions` |  | us-east-1 |
| Knowledge Base ID | `string` |  | - |
| SearchType | `options` | Knowledge Base search type. Possible values are HYBRID and SEMANTIC. If not specified, default will  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |
| TopK | `number` | Number of chunks to retrieve | - |

## Connections

**Accepts Inputs From**:
- Region (`asyncOptions`)

**Outputs**: `AWSBedrockKBRetriever`

## Common Use Cases

1. Use AWS Bedrock Knowledge Base Retriever when you need connect to aws bedrock knowledge base api and retrieve relevant chunks
2. Connect to other nodes that accept `AWSBedrockKBRetriever` input

---

**Source**: `packages/components/nodes/retrievers/AWSBedrockKBRetriever/AWSBedrockKBRetriever.ts`