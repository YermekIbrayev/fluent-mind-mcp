# Google Drive

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Load documents from Google Drive files

## Credentials

**Required**: Yes

**Credential Types**:
- googleDriveOAuth2

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| File Types | `multiOptions` | Types of files to load | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Select Files | `asyncMultiOptions` | Select files from your Google Drive | - |
| Folder ID | `string` | Google Drive folder ID to load all files from (alternative to selecting specific files) | - |

## Connections

**Accepts Inputs From**:
- Select Files (`asyncMultiOptions`)
- File Types (`multiOptions`)

**Outputs**: `Document`

## Common Use Cases

1. Use Google Drive when you need load documents from google drive files
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/GoogleDrive/GoogleDrive.ts`