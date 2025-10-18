# Ollama Embeddings

**Category**: Embeddings | **Type**: OllamaEmbeddings | **Version**: 1.0

---

## Overview

Generate embeddings for a given text using open source model on Ollama

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base URL | `string` |  | http://localhost:11434 |
| Model Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Number of GPU | `number` | The number of layers to send to the GPU(s). On macOS it defaults to 1 to enable metal support, 0 to  | - |
| Number of Thread | `number` | Sets the number of threads to use during computation. By default, Ollama will detect this for optima | - |
| Use MMap | `boolean` |  | - |

## Connections

**Outputs**: `OllamaEmbeddings`

## Common Use Cases

1. Use Ollama Embeddings when you need generate embeddings for a given text using open source model on ollama
2. Connect to other nodes that accept `OllamaEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/OllamaEmbedding/OllamaEmbedding.ts`