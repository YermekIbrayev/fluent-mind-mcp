# Research/Investigation Flow

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: [Standard Feature Workflow](standard-feature.md), [MCP-First](../principles/01-mcp-first.md)

---

## When to Use

For exploration and learning:
- Evaluating new libraries
- Investigating bugs
- Researching approaches
- Proof of concept
- Technology spikes

---

## Flow

### 1. Query Existing Knowledge (Pieces MCP)
- Check if similar problems solved
- Learn from past decisions
- Find related patterns

### 2. Search for Examples (Exa AI MCP)
- Find code examples
- Discover best practices
- Learn from community

### 3. Read Documentation (Context7 MCP)
- Official library docs
- API references
- Integration guides

### 4. Examine Source (GitHub MCP)
- Review repository structure
- Read source code
- Check issues/discussions

### 5. Validate Findings (Vibe-Check MCP)
- Verify approach soundness
- Catch assumptions
- Identify risks

### 6. Document Results (Pieces MCP)
- Key findings
- Pros/cons of approaches
- Recommendations
- Code examples

---

## MCP Integration

```
Pieces → Exa AI → Context7 → GitHub → Vibe-Check → Pieces
```

**Start**: Query Pieces for existing knowledge
**Explore**: Use Exa AI and Context7 for research
**Deep Dive**: Examine with GitHub MCP
**Validate**: Check assumptions with Vibe-Check
**Capture**: Save learnings to Pieces

---

## Converting to Production

If research leads to implementation:

1. Document findings to Pieces MCP
2. Create specification (`/speckit.specify`)
3. Follow [Standard Feature Workflow](standard-feature.md)
4. Meet Production Code standards:
   - Full TDD
   - All quality gates
   - Proper documentation

---

## Quality Requirements

**During Research**:
- No quality gates required
- Experimental Code standards
- Focus on learning

**Before Merging to Main**:
- Must meet Production Code standards
- Cannot merge spike code without conversion
- Document learnings before closing

---

**See Also**:
- [Standard Feature Workflow](standard-feature.md) - For implementation
- [Principle I: MCP-First](../principles/01-mcp-first.md) - MCP server usage
- [Principle VI: Knowledge Management](../principles/06-knowledge.md) - Capturing learnings
