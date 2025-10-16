# Context7

**Category**: Search & Documentation | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Retrieve up-to-date official documentation for libraries and frameworks.

---

## Capabilities

- `resolve-library-id` - Convert package/library name to Context7-compatible ID
- `get-library-docs` - Fetch documentation with optional topic focus
- Supports version-specific docs (e.g., `/vercel/next.js/v14.3.0`)
- Token-configurable output (default: 5000 tokens)

---

## When to Use

- Getting official library documentation
- Understanding API contracts and interfaces
- Checking version-specific features
- Learning library best practices
- Verifying correct API usage

---

## Workflow

**Always use this 2-step process:**

1. **Resolve Library ID** (unless user provides `/org/project` format)
   ```
   resolve-library-id("next.js")
   → Returns: /vercel/next.js
   ```

2. **Get Documentation**
   ```
   get-library-docs(
     context7CompatibleLibraryID: "/vercel/next.js",
     topic: "routing",
     tokens: 5000
   )
   ```

---

## Key Functions

### resolve-library-id

**Purpose**: Find Context7-compatible library ID from package name

**Parameters**:
- `libraryName` (required) - Package/library name to search

**Returns**: Matching library ID in `/org/project` format

**Selection Criteria**:
- Name similarity (exact matches prioritized)
- Description relevance
- Documentation coverage (higher code snippet counts preferred)
- Trust score (7-10 considered more authoritative)

### get-library-docs

**Purpose**: Fetch library documentation

**Parameters**:
- `context7CompatibleLibraryID` (required) - ID from resolve-library-id
- `tokens` (optional) - Max tokens to retrieve (default: 5000)
- `topic` (optional) - Focus area (e.g., "hooks", "routing", "authentication")

**Example**:
```
ID: /mongodb/docs
Topic: "aggregation"
Tokens: 3000
Returns: MongoDB aggregation documentation (~3000 tokens)
```

---

## Related

- [Exa AI](exa-ai.md) - For code examples and community resources
- [Workflows](../workflows.md#research-flow) - Research workflow pattern
