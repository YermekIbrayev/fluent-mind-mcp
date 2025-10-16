# Glossary - Term Definitions

**Version**: 1.0.0 | **Part of**: [Constitution](INDEX.md)

---

## Work Type Categories

### Production Code
Code that runs in production environment, user-facing, or provides core business value.
- Full TDD required
- All quality gates must pass
- ≥80% test coverage

### Infrastructure Code
Scripts, configurations, build files, deployment automation.
- Tests recommended
- Relaxed quality gates
- Best effort coverage

### Experimental Code
Proof of concepts, spikes, research branches.
- No gates during exploration
- Must document learnings
- Cannot merge to main without meeting Production standards

---

## Critical Path

Code paths that:
- Handle authentication/authorization
- Process or store sensitive data
- Execute financial transactions
- Implement core security controls
- Manage data integrity

**Requirements**:
- 100% test coverage (no exceptions)
- Thorough security review
- Approval required for test patterns

---

## Complex Logic

Code with:
- Cyclomatic complexity >10
- Nesting depth >3
- Multiple conditional branches
- Non-obvious algorithm

**Recommendations**:
- Use Sequential Thinking MCP for planning
- Break into smaller functions
- Add comprehensive tests
- Document reasoning

---

## Step (in Planning Context)

A single, measurable unit of work:
- Single tool invocation
- Produces measurable output
- Can be verified complete/incomplete
- Execution time: <5 minutes

---

## Architectural Decision

A decision that:
- Affects multiple components
- Is costly/difficult to reverse
- Impacts system qualities (performance, security, maintainability)

**Requires**: Architecture Decision Record (ADR)

---

## Token Optimization

Techniques to reduce AI context consumption:
- Vertical slice architecture
- File size limits (≤200 lines)
- Modular documentation (≤20 lines per README)
- Clear naming conventions
- Progressive context loading

---

## Vertical Slice

Organizing code by feature (not technical layer):
- All related code colocated
- Feature is self-contained
- Independently comprehensible
- Reduces cross-file dependencies

**Benefits**: 80% reduction in context loading

---

## TDD Cycle

Red-Green-Refactor cycle:
1. **RED**: Write failing test
2. **Approve**: Get approval if needed
3. **GREEN**: Write minimal code to pass
4. **Verify**: Confirm test passes
5. **REFACTOR**: Improve quality
6. **Repeat**: Next functionality

---

## Quality Gates

Automated checks before committing code:
- Security scanning (Semgrep MCP)
- Test coverage checks
- IDE diagnostics
- Code quality metrics
- Documentation validation

**Varies by work type**: Production (all gates), Infrastructure (relaxed), Experimental (minimal)

---

## MCP Server

Model Context Protocol server providing specialized tools:
- Sequential Thinking (problem decomposition)
- Clean Code (code planning)
- Vibe-Check (assumption validation)
- Exa AI (code search)
- Context7 (documentation)
- Pieces (knowledge management)
- Semgrep (security scanning)
- GitHub (repository operations)

---

**See Also**:
- [Principle II: TDD](principles/02-tdd.md) - TDD details
- [Principle V: Quality Gates](principles/05-quality-gates.md) - Gate details
- [Principle VIII: Token-Efficient Architecture](principles/08-architecture.md) - Architecture patterns
