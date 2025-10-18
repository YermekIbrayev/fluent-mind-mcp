# Microsoft PowerPoint

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Load data from Microsoft PowerPoint files

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| PowerPoint File | `file` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Text Splitter | `TextSplitter` |  | - |
| Additional Metadata | `json` | Additional metadata to be added to the extracted documents | - |
| Omit Metadata Keys | `string` | Each document loader comes with a default set of metadata keys that are extracted from the document. | - |

## Connections

**Accepts Inputs From**:
- PowerPoint File (`file`)
- Text Splitter (`TextSplitter`)

**Outputs**: `Document`

## Common Use Cases

1. Use Microsoft PowerPoint when you need load data from microsoft powerpoint files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/MicrosoftPowerpoint/MicrosoftPowerpoint.ts`