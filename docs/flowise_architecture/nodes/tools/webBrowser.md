# Web Browser

**Category**: Tools | **Type**: WebBrowser | **Version**: 1.0

---

## Overview

Gives agent the ability to visit a website and extract information

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Language Model | `BaseLanguageModel` |  | - |
| Embeddings | `Embeddings` |  | - |

## Connections

**Accepts Inputs From**:
- Language Model (`BaseLanguageModel`)
- Embeddings (`Embeddings`)

**Outputs**: `WebBrowser`

## Common Use Cases

1. Use Web Browser when you need gives agent the ability to visit a website and extract information
2. Connect to other nodes that accept `WebBrowser` input

---

**Source**: `packages/components/nodes/tools/WebBrowser/WebBrowser.ts`