# Principle VI: Knowledge Management and Learning

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [MCP-First](01-mcp-first.md), [Documentation](07-documentation.md)

---

## Guideline

Capture and reuse knowledge systematically.

---

## Save to Pieces MCP When

- **Architectural decisions**: Design choices, technology selections, pattern implementations
- **Complex problems solved**: Non-obvious bug fixes, performance optimizations, integration challenges
- **Implementation patterns**: Successful approaches, reusable patterns, best practices
- **Security issues**: Vulnerabilities, remediation approaches, security patterns
- **Performance optimizations**: Bottlenecks, optimization techniques, performance patterns
- **Integration patterns**: API integration, service communication, data transformation

---

## Query Pieces MCP Before

- Starting new work (check if similar problems solved)
- Making architectural decisions (learn from past choices)
- Debugging issues (find similar past issues)
- Writing documentation (reuse successful patterns)

---

## Architecture Decision Records (ADRs)

### When to Create ADR

Decision must be:
- Affects multiple components (not isolated to one)
- Costly/difficult to reverse later
- Impacts system qualities

### Examples Requiring ADR

- Database choice (PostgreSQL vs MongoDB)
- Framework selection (React vs Vue)
- API design pattern (REST vs GraphQL)
- Authentication strategy (JWT vs sessions)
- Deployment approach (containers vs serverless)

### ADR Format

Save in `.specify/memory/decisions/`

**Structure**:
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: Issue, situation, constraints
- **Decision**: What we're proposing/doing
- **Alternatives Considered**: Other options with pros/cons
- **Consequences**: What becomes easier/harder (positive/negative/neutral)
- **References**: Related ADRs, docs, PRs

**Rule of Thumb**: If you'll need to explain "why" in 6 months, write ADR.

---

**See Also**:
- [Principle I: MCP-First](01-mcp-first.md) - Pieces MCP usage
- [Principle VII: Documentation](07-documentation.md) - Documentation requirements
- [Standard Feature Workflow](../workflows/standard-feature.md) - Knowledge capture in practice
