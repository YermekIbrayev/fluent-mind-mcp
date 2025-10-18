# Vectara Upload File

**Category**: Vector Stores | **Type**: Vectara | **Version**: 1.0

---

## Overview

Upload files to Vectara

## Credentials

**Required**: Yes

**Credential Types**:
- vectaraApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| File | `file` | File to upload to Vectara. Supported file types: https://docs.vectara.com/docs/api-reference/indexin | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Metadata Filter | `string` | Filter to apply to Vectara metadata. Refer to the <a target= | - |
| Sentences Before | `number` | Number of sentences to fetch before the matched sentence. Defaults to 2. | - |
| Sentences After | `number` | Number of sentences to fetch after the matched sentence. Defaults to 2. | - |
| Lambda | `number` | Improves retrieval accuracy by adjusting the balance (from 0 to 1) between neural search and keyword | - |
| Top K | `number` | Number of top results to fetch. Defaults to 4 | - |

## Connections

**Accepts Inputs From**:
- File (`file`)

**Outputs**: `Vectara`

## Common Use Cases

1. Use Vectara Upload File when you need upload files to vectara
2. Connect to other nodes that accept `Vectara` input

---

**Source**: `packages/components/nodes/vectorstores/Vectara/Vectara_Upload.ts`