# Principle IV: Comprehensive Planning

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Specification-Driven](03-spec-driven.md), [Standard Workflow](../workflows/standard-feature.md)

---

## Guideline

Planning requirements scale with task complexity.

---

## Planning Levels

### Trivial (1-2 steps, <15 min)
- No planning required
- Inline TODO comments acceptable
- Examples: Fix typo, update config, add log statement

### Simple (3-5 steps, 15-60 min)
- Single file: `.plans/NNNN_task.md`
- Contents: Goal, approach, steps, MCP servers, success criteria
- Examples: Add logging, update dependency, fix bug, add validation

### Moderate (6-10 steps, 1-4 hours)
- Two files: `01_initial_plan.md` + `02_revised_plan.md`
- Initial: First understanding, high-level approach, challenges
- Revised: Detailed breakdown, MCP mapping, dependencies, risks, success criteria
- Examples: Refactor module, add feature with tests, implement API endpoint, schema migration

### Complex (11+ steps, >4 hours)
- Four files: `01_initial_plan.md` + `02_revised_plan.md` + `03_mcp_usage_plan.md` + `04_execution_log.md`
- Execution log: Actual execution, MCP inputs/outputs, issues, outcomes, time analysis, lessons learned
- Examples: New feature with spec, major refactoring, multi-component integration, performance optimization

---

## What Counts as a "Step"?

- Single tool invocation
- Produces measurable output
- Can be verified complete/incomplete
- Execution time: <5 minutes

---

## Context Budget Planning

For AI-assisted development:

- **Must-Have Context (20%)**: Files being modified, direct dependencies, interfaces, tests, specifications
- **Should-Have Context (30%)**: Related modules, parent abstractions, configuration, similar implementations
- **Optional Context (50% reserve)**: Documentation, historical decisions, similar features, external docs, benchmarks

---

**See Also**:
- [Principle III: Specification-Driven](03-spec-driven.md) - Specification requirements
- [Principle VIII: Token-Efficient Architecture](08-architecture.md) - Context optimization
- [Standard Feature Workflow](../workflows/standard-feature.md) - Planning in practice
