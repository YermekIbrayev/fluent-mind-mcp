# Write File

**Category**: Tools | **Type**: WriteFile | **Version**: 2.0

---

## Overview

Write file to disk

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Workspace Path | `string` | Base workspace directory for file operations. All file paths will be relative to this directory. | - |
| Enforce Workspace Boundaries | `boolean` | When enabled, restricts file access to the workspace directory for security. Recommended: true | - |
| Max File Size (MB) | `number` | Maximum file size in megabytes that can be written | - |
| Allowed Extensions | `string` | Comma-separated list of allowed file extensions (e.g., .txt,.json,.md). Leave empty to allow all. | - |

## Connections

**Outputs**: `WriteFile`

## Common Use Cases

1. Use Write File when you need write file to disk
2. Connect to other nodes that accept `WriteFile` input

---

**Source**: `packages/components/nodes/tools/WriteFile/WriteFile.ts`