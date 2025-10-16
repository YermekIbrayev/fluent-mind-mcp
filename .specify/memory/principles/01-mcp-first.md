# Principle I: MCP-First Architecture

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [MCP Servers Reference](../references/mcp-servers-ref.md), [Standard Workflow](../workflows/standard-feature.md)

---

## Guideline

Leverage MCP servers when they provide clear advantages.

---

## Priority Order

Use MCP servers when they provide:

1. **Accuracy/Reliability** - Produces correct, consistent results
2. **Auditability** - Creates traceable record of actions
3. **Learning Value** - Documents process for future reference
4. **Efficiency** - Reasonably performant (<10x slower than alternative)

---

## Use Traditional Methods When

- MCP server unavailable or experiencing issues
- Significantly slower (>10x) for time-critical operations
- Not suited for the task

---

## Available MCP Servers

**Development & Planning**:
- Sequential Thinking - Complex problem decomposition
- Clean Code - Code planning and design
- Vibe-Check - Assumption validation and bias detection

**Code Search & Documentation**:
- Exa AI - Code examples and best practices
- Context7 - Official library documentation
- GitHub - Repository search and analysis

**Quality & Security**:
- Semgrep - Security scanning
- IDE - Diagnostics and type checking

**Testing**:
- Chrome DevTools - Browser automation and testing
- IDE - Code execution and testing

**Knowledge Management**:
- Pieces - Long-term memory and context capture
- Vibe-Check - Pattern learning and mistake tracking

**Git Operations**:
- GitHub - Repository operations and PR management

---

## Integration in Workflows

**Feature Development**:
```
Vibe-Check → Sequential Thinking → Clean Code → IDE → Semgrep → Pieces → GitHub
```

**Bug Investigation**:
```
Pieces → Exa AI → Context7 → Sequential Thinking → Pieces
```

**Research/Spike**:
```
Exa AI → Context7 → GitHub → Vibe-Check → Pieces
```

---

**See Also**:
- [MCP Servers Reference](../references/mcp-servers-ref.md) - Complete server documentation
- [Standard Feature Workflow](../workflows/standard-feature.md) - MCP integration in practice
- [Principle VI: Knowledge Management](06-knowledge.md) - Pieces MCP usage
