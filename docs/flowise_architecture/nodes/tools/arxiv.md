# Arxiv

**Category**: Tools | **Type**: Arxiv | **Version**: 1.0

---

## Overview

Search and read content from academic papers on Arxiv

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Name | `string` | Name of the tool | arxiv_search |
| Description | `string` | Describe to LLM when it should use this tool | - |
| Top K Results | `number` | Number of top results to return from Arxiv search | 3 |
| Max Query Length | `number` | Maximum length of the search query | 300 |
| Max Content Length | `number` | Maximum length of the returned content. Set to 0 for unlimited | 10000 |
| Load Full Content | `boolean` | Download PDFs and extract full paper content instead of just summaries. Warning: This is slower and  | - |
| Continue On Failure | `boolean` | Continue processing other papers if one fails to download/parse (only applies when Load Full Content | - |
| Use Legacy Build | `boolean` | Use legacy PDF.js build for PDF parsing (only applies when Load Full Content is enabled) | - |

## Connections

**Outputs**: `Arxiv`

## Common Use Cases

1. Use Arxiv when you need search and read content from academic papers on arxiv
2. Connect to other nodes that accept `Arxiv` input

---

**Source**: `packages/components/nodes/tools/Arxiv/Arxiv.ts`