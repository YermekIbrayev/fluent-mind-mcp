# Exa AI

**Category**: Search & Documentation | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Real-time web search and code context retrieval for programming tasks.

---

## Capabilities

- `web_search_exa` - Perform web searches with configurable result counts
- `get_code_context_exa` - Search for APIs, libraries, SDKs, and code examples
- Dynamic token allocation (100-1000+ tokens or specific count 1000-50000)
- Highest quality and freshest context for code examples

---

## When to Use

- Finding code examples and best practices
- Researching libraries, SDKs, and APIs
- Getting real-time information about programming topics
- Learning from community implementations
- Discovering latest framework features and patterns

---

## Key Functions

### web_search_exa

**Purpose**: Search the web for programming-related information

**Parameters**:
- `query` (required) - Search query
- `numResults` (optional) - Number of results to return (default: 5)

**Example**:
```
Query: "React Server Components examples"
Returns: Top 5 web results with code examples
```

### get_code_context_exa

**Purpose**: Get relevant code context for programming tasks

**Parameters**:
- `query` (required) - Search query for code context
- `tokensNum` (optional) - "dynamic" (default, 100-1000+ tokens) or specific number 1000-50000

**Example Queries**:
- "React useState hook examples"
- "Python pandas dataframe filtering"
- "Next.js partial prerendering configuration"
- "Express.js middleware patterns"

**Returns**: Most useful tokens for the query context

---

## Usage Tips

**Use "dynamic" token mode** when:
- You want optimal token efficiency
- Query is exploratory
- Not sure how much context needed

**Use specific token count** when:
- Need comprehensive documentation
- Specific amount of context required
- "dynamic" didn't return enough information

---

## Related

- [Context7](context7.md) - For official library documentation
- [Workflows](../workflows.md#research-flow) - Research workflow pattern
