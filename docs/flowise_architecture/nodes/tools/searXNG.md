# SearXNG

**Category**: Tools | **Type**: SearXNG | **Version**: 3.0

---

## Overview

Wrapper around SearXNG - a free internet metasearch engine

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base URL | `string` |  | http://localhost:8080 |
| Tool Name | `string` |  | - |
| Tool Description | `string` |  | - |
| Format | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Headers | `json` | Custom headers for the request | - |

## Connections

**Outputs**: `SearXNG`

## Common Use Cases

1. Use SearXNG when you need wrapper around searxng - a free internet metasearch engine
2. Connect to other nodes that accept `SearXNG` input

---

**Source**: `packages/components/nodes/tools/Searxng/Searxng.ts`