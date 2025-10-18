# Google Sheets

**Category**: Document Loaders | **Type**: Document | **Version**: 1.0

---

## Overview

Load data from Google Sheets as documents

## Credentials

**Required**: Yes

**Credential Types**:
- googleSheetsOAuth2

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Select Spreadsheet | `asyncMultiOptions` | Select spreadsheet from your Google Drive | - |
| Include Headers | `boolean` | Whether to include the first row as headers | - |
| Value Render Option | `options` | How values should be represented in the output | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sheet Names | `string` | Comma-separated list of sheet names to load. If empty, loads all sheets. | - |
| Range | `string` | Range to load (e.g., A1:E10). If empty, loads entire sheet. | - |

## Connections

**Accepts Inputs From**:
- Select Spreadsheet (`asyncMultiOptions`)

**Outputs**: `Document`

## Common Use Cases

1. Use Google Sheets when you need load data from google sheets as documents
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/GoogleSheets/GoogleSheets.ts`