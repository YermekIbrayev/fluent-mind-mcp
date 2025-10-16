# MCP Servers Reference

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > References

**Full Details**: [Principle I: MCP-First Architecture](../principles/01-mcp-first.md)

---

## Complete MCP Server List

| MCP Server | Primary Use Cases | Key Tools |
|------------|-------------------|-----------|
| **GitHub** | Repository operations, file management, PRs, issues | `create_repository`, `create_branch`, `push_files`, `create_pull_request` |
| **Exa AI** | Code search, implementation examples, best practices | `get_code_context_exa`, `web_search_exa` |
| **Context7** | Library docs, API references, framework documentation | `resolve-library-id`, `get-library-docs` |
| **Semgrep** | Security scanning, vulnerability detection | `scan` |
| **Vibe-Check** | Approach validation, assumption checking, learning | `vibe_check`, `vibe_learn`, `check_constitution` |
| **Sequential Thinking** | Complex problem decomposition, multi-step reasoning | `sequentialthinking` |
| **Pieces** | Project decisions memory, implementation queries | `create_pieces_memory`, `ask_pieces_ltm` |
| **Chrome DevTools** | Browser automation, UI testing, performance | `take_snapshot`, `click`, `fill`, `wait_for` |
| **IDE** | Language diagnostics, Jupyter execution | `getDiagnostics`, `executeCode` |
| **Clean Code** | Code planning with clean principles | `cleancode` |
| **Chroma** | Vector database, RAG, semantic search | Collection operations, search |

---

## When to Use Each MCP

### Development & Planning
- **Sequential Thinking**: Complex decisions, multi-step problems
- **Clean Code**: Architecture planning before coding
- **Vibe-Check**: Validate approach, catch assumptions

### Code Search & Documentation
- **Exa AI**: Find code examples, tutorials, patterns
- **Context7**: Official library documentation
- **GitHub**: Read source code, search repositories

### Quality & Security
- **Semgrep**: Security vulnerability scanning
- **IDE**: Type errors, diagnostics, linting

### Testing
- **Chrome DevTools**: UI testing, browser automation
- **IDE**: Run tests, check diagnostics

### Knowledge Management
- **Pieces**: Remember decisions, query past work
- **Vibe-Check**: Learn from mistakes (`vibe_learn`)

### Git Operations
- **GitHub**: All repository operations, PRs, issues

---

## MCP-First Decision Criteria

Use MCP servers when they provide advantages in priority order:

1. **Accuracy/Reliability** - Correct, consistent results
2. **Auditability** - Traceable record
3. **Learning Value** - Documents process
4. **Efficiency** - Reasonably performant (<10x slower)

**Use traditional methods if:**
- MCP server unavailable or experiencing issues
- Significantly slower (>10x) for time-critical ops
- Not suited for specific task

---

## Common MCP Workflows

### Feature Development
1. **Vibe-Check**: Validate approach
2. **Sequential Thinking**: Break down complex logic
3. **Clean Code**: Plan architecture
4. **IDE**: Check diagnostics during coding
5. **Semgrep**: Security scan before commit
6. **Pieces**: Save learnings
7. **GitHub**: Commit and create PR

### Bug Investigation
1. **Pieces**: Query similar past issues
2. **Exa AI**: Find solutions/patterns
3. **Context7**: Check library docs
4. **Sequential Thinking**: Debug complex issues
5. **Pieces**: Save fix for future

### Research/Spike
1. **Exa AI**: Search for code examples
2. **Context7**: Get official docs
3. **GitHub**: Examine source code
4. **Vibe-Check**: Validate findings
5. **Pieces**: Document research results

---

**See Also**:
- [Principle I: MCP-First Architecture](../principles/01-mcp-first.md) - When to use MCPs
- [Standard Feature Workflow](../workflows/standard-feature.md) - MCP integration
- [Research/Investigation Flow](../workflows/research.md) - MCP for research
