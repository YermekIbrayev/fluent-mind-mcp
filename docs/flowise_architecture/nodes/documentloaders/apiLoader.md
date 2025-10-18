# API Loader

**Category**: Document Loaders | **Type**: Document | **Version**: 2.1

---

## Overview

Load data from an API

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Method | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |

## Connections

**Accepts Inputs From**:
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use API Loader when you need load data from an api
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/API/APILoader.ts`