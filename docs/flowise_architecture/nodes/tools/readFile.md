# Read File

**Category**: Tools | **Type**: ReadFile | **Version**: 2.0

---

## Overview

Read file from disk

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Workspace Path | `string` | Base workspace directory for file operations. All file paths will be relative to this directory. | - |
| Enforce Workspace Boundaries | `boolean` | When enabled, restricts file access to the workspace directory for security. Recommended: true | - |
| Max File Size (MB) | `number` | Maximum file size in megabytes that can be read | - |
| Allowed Extensions | `string` | Comma-separated list of allowed file extensions (e.g., .txt,.json,.md). Leave empty to allow all. | - |

## Connections

**Outputs**: `ReadFile`

## Common Use Cases

1. Use Read File when you need read file from disk
2. Connect to other nodes that accept `ReadFile` input

---

**Source**: `packages/components/nodes/tools/ReadFile/ReadFile.ts`