# Research/Investigation Flow

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: [Standard Workflow](standard-feature.md), [MCP Servers Reference](../references/mcp-servers-ref.md)

---

## Purpose

Structured approach for research, spikes, and exploratory work.

**Use When:**
- Evaluating new technologies
- Investigating architectural options
- Prototyping approaches
- Feasibility studies
- Performance investigations
- Learning new libraries/frameworks

---

## Research Workflow

### 1. Query Pieces
Check if similar research done before:
- Use Pieces MCP: `ask_pieces_ltm`
- Search for related topics
- Review past findings
- Avoid duplicate research

### 2. Exa AI Search
Find code examples and tutorials:
- Use Exa AI MCP: `get_code_context_exa`
- Search for implementation examples
- Find best practices
- Discover patterns

### 3. Context7 Docs
Get official API documentation:
- Use Context7 MCP: `get-library-docs`
- Read official documentation
- Understand APIs and interfaces
- Check version-specific details

### 4. GitHub Source
Examine source code (if needed):
- Use GitHub MCP: `get_file_contents`
- Read actual implementations
- Understand internals
- Check for gotchas

### 5. Experiment
Create spike branch and prototype:
- Use **Experimental Code** rules (minimal gates)
- Branch naming: `spike/[description]`
- Quick and dirty prototypes OK
- Focus on learning, not production quality

**Quality Gates**: Minimal (see [Experimental Code](../principles/05-quality-gates.md#experimental-code-minimal-gates))

### 6. Vibe-Check Validation
Validate findings and approach:
- Use Vibe-Check MCP: `vibe_check`
- Validate approach soundness
- Check for hidden assumptions
- Identify risks

### 7. Document Findings
Save research results:
- Use Pieces MCP: `create_pieces_memory`
- Document what works
- Document what doesn't work
- Include code examples
- Note trade-offs

### 8. Create ADR (if needed)
If architectural decision made:
- Create ADR in `.specify/memory/decisions/`
- Document alternatives considered
- Explain choice rationale
- See [Principle VI: Knowledge Management](../principles/06-knowledge.md#architecture-decision-records-adrs)

### 9. Close or Convert
Choose next step:

**Close Spike:**
- Archive spike branch
- Findings documented in Pieces
- Research complete

**Convert to Production:**
- Meet Production Code standards
- Apply all [quality gates](../principles/05-quality-gates.md#production-code-all-gates-required)
- Follow [TDD](../principles/02-tdd.md)
- Create proper specification
- Use [Standard Workflow](standard-feature.md)

---

## MCP Integration for Research

**Step** | **MCP Server** | **Usage**
---------|---------------|----------
Query Past Work | Pieces | Check prior research
Find Examples | Exa AI | Code search, tutorials
Read Docs | Context7 | Official documentation
Check Source | GitHub | Read implementations
Problem Solving | Sequential Thinking | Break down complexity
Validate | Vibe-Check | Check assumptions
Document | Pieces | Save findings

---

## Research Anti-Patterns

❌ **Not checking Pieces first** - Repeat work
❌ **No documentation** - Knowledge lost
❌ **Analysis paralysis** - Research forever
❌ **Not time-boxing** - Research takes weeks
❌ **Merging spike code** - Poor quality to production
❌ **No decision record** - Why chosen unclear

---

## Research Best Practices

✅ **Time-box research** - Set deadline (e.g., 1-3 days max)
✅ **Document as you go** - Don't wait until end
✅ **Focus on decision-making** - What do we need to decide?
✅ **Prototype quickly** - Validate assumptions fast
✅ **Share findings** - Brief team on results
✅ **Create ADR** - If decision made

---

## Example: Evaluating Database Options

```
1. Query Pieces:
   - Have we evaluated databases before?
   - What did we choose last time?

2. Exa AI Search:
   - "PostgreSQL vs MongoDB for [use case]"
   - Find comparison articles
   - Read experiences

3. Context7 Docs:
   - PostgreSQL documentation
   - MongoDB documentation
   - Compare APIs

4. Experiment (spike branch):
   - Prototype with PostgreSQL
   - Prototype with MongoDB
   - Compare performance

5. Vibe-Check:
   - Are we missing something?
   - Hidden assumptions?
   - Risks identified?

6. Document to Pieces:
   - PostgreSQL pros/cons
   - MongoDB pros/cons
   - Performance comparison
   - Recommendation

7. Create ADR:
   - Document decision
   - Explain rationale
   - Record alternatives

8. Close spike branches:
   - Delete prototype code
   - Keep findings in Pieces + ADR
```

---

## When to Stop Research

**Stop When:**
- Sufficient information to make decision
- Time-box expired
- Diminishing returns
- Decision can be deferred

**Don't Stop When:**
- Critical unknowns remain
- High-risk decision needs more data
- Alternatives not fully explored

**Rule of Thumb**: Research to reduce uncertainty, not eliminate it.

---

**See Also**:
- [Principle I: MCP-First](../principles/01-mcp-first.md) - When to use MCPs
- [Principle VI: Knowledge Management](../principles/06-knowledge.md) - ADRs
- [MCP Servers Reference](../references/mcp-servers-ref.md) - Complete MCP list
- [Principle V: Quality Gates](../principles/05-quality-gates.md) - Experimental Code rules
- [Standard Workflow](standard-feature.md) - If converting spike to production
