# Principle VI: Knowledge Management and Learning

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [MCP Servers Reference](../references/mcp-servers-ref.md), [Documentation](07-documentation.md)

**Prerequisites**: Understand [Architectural Decision](../glossary.md#architectural-decision)

---

## Guideline

Capture and reuse knowledge systematically.

---

## Pieces MCP Integration

### Save to Pieces When

Save important information to Pieces MCP for future reference:

**Architectural Decisions:**
- Important design choices
- Technology selections
- Pattern implementations

**Complex Problems Solved:**
- Non-obvious bug fixes
- Performance optimizations
- Integration challenges

**Implementation Patterns:**
- Successful approaches
- Reusable patterns
- Best practices discovered

**Security Issues:**
- Vulnerabilities identified
- Remediation approaches
- Security patterns

**Performance Optimizations:**
- Bottlenecks found
- Optimization techniques
- Performance patterns

**Integration Patterns:**
- API integration approaches
- Service communication patterns
- Data transformation patterns

### Query Pieces Before

Query Pieces MCP before starting work:

**Starting New Work:**
- Check if similar problems solved
- Find reusable patterns
- Learn from past approaches

**Making Architectural Decisions:**
- Learn from past choices
- Understand trade-offs made
- Avoid repeating mistakes

**Debugging Issues:**
- Find similar past issues
- Check if already solved
- Reuse successful approaches

**Writing Documentation:**
- Reuse successful patterns
- Check past documentation approaches
- Maintain consistency

---

## Architecture Decision Records (ADRs)

### When to Create an ADR

Create ADR when decision meets [Architectural Decision](../glossary.md#architectural-decision) criteria:

**Decision Tree:**
```
Is this decision...
  └─ Isolated to one component?
      ├─ YES → Comment/note suffices
      └─ NO → Continue
           └─ Easy to reverse later?
               ├─ YES → Comment/note suffices
               └─ NO → Create ADR
```

**Examples Requiring ADR:**
- Database choice (PostgreSQL vs MongoDB)
- Framework selection (React vs Vue)
- API design pattern (REST vs GraphQL)
- Authentication strategy (JWT vs sessions)
- Deployment approach (containers vs serverless)

**Examples NOT Requiring ADR:**
- Local variable naming
- Single-function refactoring
- File organization within module
- Logging library choice (easily reversible)

**Rule of Thumb**: If you'll need to explain "why" in 6 months, write ADR.

**When in Doubt**: Ask Vibe-Check MCP if ADR is warranted.

---

### ADR Format

**Location**: `.specify/memory/decisions/`

**Template:**
```markdown
# ADR NNNN: [Decision Title]

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Authors**: [Names]

## Context

What is the issue that motivates this decision?
- Current situation
- Constraints
- Forces at play

## Decision

What is the change we're proposing/doing?
- Clear statement of decision
- Approach chosen
- Key aspects

## Alternatives Considered

What other options did we consider?
1. Alternative A
   - Pros: ...
   - Cons: ...
2. Alternative B
   - Pros: ...
   - Cons: ...

## Consequences

What becomes easier or harder due to this change?

**Positive:**
- Benefit 1
- Benefit 2

**Negative:**
- Trade-off 1
- Trade-off 2

**Neutral:**
- Side effect 1

## References

- Related ADRs
- External documentation
- Implementation PRs
```

---

## Knowledge Management Anti-Patterns

❌ **Not documenting decisions** - Knowledge lost
❌ **Documenting too late** - Context forgotten
❌ **Not querying before starting** - Repeat mistakes
❌ **Not updating Pieces** - Stale information
❌ **ADRs without context** - Unclear why chosen
❌ **No alternatives documented** - Can't learn from trade-offs

---

## Knowledge Management Benefits

✅ **Prevent repeated mistakes** - Learn from past
✅ **Preserve context** - Understand why decisions made
✅ **Faster onboarding** - New team members catch up quickly
✅ **Better decisions** - Informed by historical data
✅ **Reusable patterns** - Don't reinvent wheel
✅ **Continuous improvement** - Build on successes

---

## Knowledge Capture Workflow

### During Development

1. **Encounter Challenge** - Problem, decision, or discovery
2. **Solve/Decide** - Work through issue
3. **Immediate Capture** - While context fresh
   - Simple fix → Save to Pieces MCP
   - Architectural decision → Create ADR
4. **Tag Appropriately** - Make findable later

### After Completion

1. **Review Execution Log** - What was learned?
2. **Extract Key Insights** - Important patterns/approaches
3. **Update Knowledge Base**:
   - Add to Pieces MCP
   - Create/update ADRs
   - Update team wiki/docs
4. **Share with Team** - Brief mention in standup/retro

### Before Starting New Work

1. **Query Pieces** - Similar problems solved?
2. **Read Relevant ADRs** - Architectural constraints?
3. **Check Past Execution Logs** - Time estimates accurate?
4. **Apply Learnings** - Benefit from past experience

---

**See Also**:
- [Principle VII: Documentation](07-documentation.md) - Documentation requirements
- [Glossary: Architectural Decision](../glossary.md#architectural-decision) - When ADR needed
- [MCP Servers Reference](../references/mcp-servers-ref.md) - Pieces MCP details
- [Principle IV: Planning](04-planning.md) - Execution logs
