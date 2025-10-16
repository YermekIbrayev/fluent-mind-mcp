# Claude Code - MCP Servers Index

**Version**: 2.0.0 (Modular) | **Last Updated**: 2025-10-16

Quick navigation hub for all available MCP (Model Context Protocol) servers.

---

## Quick Navigation by Need

**"I need code examples"** → [Exa AI](.specify/mcp-servers/search/exa-ai.md)

**"I need official docs"** → [Context7](.specify/mcp-servers/search/context7.md)

**"I need to solve a complex problem"** → [Sequential Thinking](.specify/mcp-servers/thinking/sequential-thinking.md)

**"I need to plan clean code"** → [Clean Code](.specify/mcp-servers/thinking/clean-code.md)

**"I need to check assumptions"** → [Vibe Check](.specify/mcp-servers/thinking/vibe-check.md)

**"I need to capture knowledge"** → [Pieces](.specify/mcp-servers/knowledge/pieces.md)

**"I need to work with GitHub"** → [GitHub](.specify/mcp-servers/devtools/github.md)

**"I need to test UI"** → [Chrome DevTools](.specify/mcp-servers/devtools/chrome-devtools.md)

**"I need code diagnostics"** → [IDE](.specify/mcp-servers/devtools/ide.md)

**"What workflows should I use?"** → [Workflows](.specify/mcp-servers/workflows.md)

---

## MCP Servers by Category

### 🔍 Search & Documentation
- [Exa AI](.specify/mcp-servers/search/exa-ai.md) - Real-time web search and code context
- [Context7](.specify/mcp-servers/search/context7.md) - Official library documentation

### 🧠 Thinking & Planning
- [Sequential Thinking](.specify/mcp-servers/thinking/sequential-thinking.md) - Dynamic problem-solving
- [Clean Code](.specify/mcp-servers/thinking/clean-code.md) - Code planning and design
- [Vibe Check](.specify/mcp-servers/thinking/vibe-check.md) - Assumption validation

### 💾 Knowledge Management
- [Pieces](.specify/mcp-servers/knowledge/pieces.md) - Long-term memory and context capture

### 🛠️ DevTools
- [GitHub](.specify/mcp-servers/devtools/github.md) - Repository operations
- [IDE](.specify/mcp-servers/devtools/ide.md) - Diagnostics and code execution
- [Chrome DevTools](.specify/mcp-servers/devtools/chrome-devtools.md) - Browser automation and testing

---

## Common Workflows

### Feature Development
```
Vibe Check → Sequential Thinking → Clean Code → IDE → Pieces → GitHub
```
[See full workflow](.specify/mcp-servers/workflows.md#feature-development-flow)

### Bug Investigation
```
Pieces → Exa AI → Context7 → Sequential Thinking → Pieces
```
[See full workflow](.specify/mcp-servers/workflows.md#bug-investigation-flow)

### Research/Spike
```
Exa AI → Context7 → GitHub → Vibe Check → Pieces
```
[See full workflow](.specify/mcp-servers/workflows.md#researchspike-flow)

### Performance Analysis
```
Chrome DevTools → Performance Trace → Analyze Insights
```
[See full workflow](.specify/mcp-servers/workflows.md#performance-analysis-flow)

**View all workflows**: [workflows.md](.specify/mcp-servers/workflows.md)

---

## MCP-First Priority

Use MCP servers when they provide:
1. **Accuracy/Reliability** - Correct, consistent results
2. **Auditability** - Traceable record of actions
3. **Learning Value** - Documents process for future
4. **Efficiency** - Reasonably performant (<10x slower)

Use traditional methods when:
- MCP server unavailable or having issues
- Significantly slower (>10x) for time-critical operations
- Not suited for the task

---

## How to Use This Index

**For Quick Reference**:
1. Use "Quick Navigation by Need" above
2. Load only the MCP server you need (~300-400 tokens)
3. Total: ~400-700 tokens vs 2,500+ tokens for full docs

**Token Efficiency**:
- Old monolithic file: 355 lines = ~2,500 tokens
- New modular approach: Index + 1 MCP = ~400-700 tokens
- **Savings: 70-75% token reduction**

---

## File Organization

```
project-root/
├── CLAUDE.md              # This file (navigation hub)
└── .specify/
    ├── mcp-servers/
    │   ├── search/        # Exa AI, Context7
    │   ├── thinking/      # Sequential Thinking, Clean Code, Vibe Check
    │   ├── knowledge/     # Pieces
    │   ├── devtools/      # GitHub, IDE, Chrome DevTools
    │   └── workflows.md   # Common workflow patterns
    └── memory/            # Constitution
        ├── INDEX.md
        ├── constitution.md
        └── principles/, workflows/, etc.
```

---

## Constitution Compliance

This documentation follows the project constitution:

- **Principle VIII**: Token-Efficient Architecture (all files ≤100 lines)
- **Principle VII**: Documentation Excellence (clear, concise, token-optimized)
- **Vertical Slice**: Organized by category (search, thinking, knowledge, devtools)

**Constitution Location**: `/Users/yermekibrayev/work/ai/fluent-mind-mcp/.specify/memory/constitution.md`

---

**Version**: 2.0.0 (Modular) | **Migration Date**: 2025-10-16
