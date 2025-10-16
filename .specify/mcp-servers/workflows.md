# MCP Server Workflows

**Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Common workflow patterns integrating multiple MCP servers for typical development tasks.

---

## Feature Development Flow

**Goal**: Plan and implement a new feature with full quality checks

```
1. Vibe Check → Validate approach and assumptions
2. Sequential Thinking → Break down problem
3. Clean Code → Plan architecture and design
4. IDE → Check diagnostics before implementation
5. [Implement feature]
6. IDE → Validate diagnostics after implementation
7. Pieces → Capture learnings and patterns
8. GitHub → Commit and create PR
```

**MCP Servers**: Vibe Check, Sequential Thinking, Clean Code, IDE, Pieces, GitHub

---

## Bug Investigation Flow

**Goal**: Research and solve a bug efficiently

```
1. Pieces → Query for similar past issues
2. Exa AI → Search for community solutions
3. Context7 → Check official documentation
4. Sequential Thinking → Analyze root cause
5. [Implement fix]
6. IDE → Validate fix with diagnostics
7. Pieces → Document solution for future
8. GitHub → Commit fix
```

**MCP Servers**: Pieces, Exa AI, Context7, Sequential Thinking, IDE, GitHub

---

## Research/Spike Flow

**Goal**: Explore new libraries, frameworks, or approaches

```
1. Exa AI → Get code examples and community practices
2. Context7 → Read official documentation
3. GitHub → Examine source code and issues
4. Vibe Check → Validate findings and approach
5. Pieces → Document research findings
6. [Optional] Chrome DevTools → Test in browser if UI-related
```

**MCP Servers**: Exa AI, Context7, GitHub, Vibe Check, Pieces, Chrome DevTools (optional)

---

## Performance Analysis Flow

**Goal**: Identify and fix performance issues

```
1. Chrome DevTools → Start performance trace
2. Chrome DevTools → Analyze Core Web Vitals
3. Chrome DevTools → Deep dive into specific insights
4. Exa AI → Research optimization techniques
5. Sequential Thinking → Plan optimization approach
6. [Implement optimizations]
7. Chrome DevTools → Verify improvements
8. Pieces → Document optimization patterns
```

**MCP Servers**: Chrome DevTools, Exa AI, Sequential Thinking, Pieces

---

## Code Review Flow

**Goal**: Review code changes thoroughly

```
1. GitHub → Get PR details and files
2. IDE → Check diagnostics for changed files
3. Vibe Check → Validate approach and assumptions
4. GitHub → Create review with feedback
5. [Wait for changes]
6. GitHub → Approve and merge
7. Pieces → Capture notable review insights
```

**MCP Servers**: GitHub, IDE, Vibe Check, Pieces

---

## UI Testing Flow

**Goal**: Test user interface and interactions

```
1. Chrome DevTools → Open page
2. Chrome DevTools → Take snapshot (get UIDs)
3. Chrome DevTools → Interact with elements
4. Chrome DevTools → Check console for errors
5. Chrome DevTools → Take screenshots for documentation
6. [Optional] Emulate network/CPU for slow conditions
7. Pieces → Document testing findings
```

**MCP Servers**: Chrome DevTools, Pieces

---

## Knowledge Capture Flow

**Goal**: Save important project context and decisions

```
1. [Complete work]
2. Pieces → Create memory with:
   - Summary description
   - Detailed narrative
   - Associated files (absolute paths)
   - External links (GitHub, docs)
   - Project root path
3. GitHub → Commit with clear message
4. [Optional] Vibe Learn → Track patterns if mistakes made
```

**MCP Servers**: Pieces, GitHub, Vibe Check (optional)

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

## Related

- [Constitution](../memory/constitution.md) - Development principles
- [MCP-First Principle](../memory/principles/01-mcp-first.md) - Detailed guidance
