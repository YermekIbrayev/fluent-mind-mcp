# Principle II: Test-First Development (NON-NEGOTIABLE)

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [TDD Quick Reference](../references/tdd-quick-ref.md), [Quality Gates](05-quality-gates.md)

**Prerequisites**: Understand [Critical Path](../glossary.md#critical-path) definition

---

## Mandate

TDD is **required** for all Production Code - tests before implementation.

---

## The Sacred Cycle (Red-Green-Refactor)

**Diagram**: [View TDD Cycle](../diagrams/tdd-cycle.mermaid)

**Text Flow**:
```
RED → Approve (if needed) → GREEN → REFACTOR → Repeat
```

### Steps

**1. RED - Write Failing Test**
- Demonstrate the requirement through a test
- Test must fail for the right reason
- Defines expected behavior

**2. Approve (if needed)**
- Get approval for new patterns/critical paths
- Via User or Vibe-Check MCP
- Fast-track for routine tests (see below)

**3. GREEN - Write Minimal Code**
- Write just enough code to pass the test
- Don't add extra features
- Focus on making it work

**4. Verify Test Passes**
- Confirm implementation satisfies test
- All tests still green

**5. REFACTOR - Improve Quality**
- Improve code quality
- Keep tests green throughout
- Reduce complexity, improve readability

**6. Repeat**
- Continue cycle for next functionality
- Build features incrementally

---

## Approval Process

### Approval Required
Get approval (User or Vibe-Check MCP) for:
- New test patterns or testing strategies
- [Critical path](../glossary.md#critical-path) tests (security, data, APIs)
- Non-obvious test scenarios or edge cases
- First test for a new module/feature

### Fast-Track (No Approval Needed)
Proceed directly for:
- Routine tests following established patterns
- Additional test cases for existing scenarios
- Refactoring existing tests
- Tests for bug fixes following existing patterns

---

## Quality Metrics

| Metric | Requirement | Notes |
|--------|-------------|-------|
| **Test Coverage** | ≥80% overall | 100% for [Critical Paths](../glossary.md#critical-path) |
| **Unit Tests** | <100ms per test | Isolated, no shared state |
| **Integration Tests** | <5s per test | Can use external dependencies |
| **Test Names** | Descriptive | Must explain what they verify |

### Test Quality Standards
- All tests must **pass** (no flaky tests)
- No skipped tests in Production Code
- Tests must be **isolated** (no shared state)
- Coverage must include **edge cases**

---

## Work Type Requirements

### Production Code
- **Full TDD required** (no exceptions)
- RED-GREEN-REFACTOR cycle mandatory
- Coverage: ≥80% overall, 100% Critical Path

### Infrastructure Code
- Tests **recommended** (e.g., validate configs, test scripts)
- TDD cycle optional
- Coverage: Best effort

### Experimental Code
- Tests **optional** (but document findings)
- TDD not required during exploration
- Must convert to Production standards before merging to main

**See Also**: [Work Type Categories](../glossary.md#work-type-categories)

---

## Expert Review Cycle (for Documentation & Constitution)

**Purpose**: Apply TDD methodology to constitution and documentation improvements.

**When to Use**: Constitution updates, major documentation refactoring, process improvements.

**Diagram**: [View Expert Review Cycle](../diagrams/expert-review-cycle.mermaid)

**The Cycle**:

1. **GREEN** - Existing code/docs (current state)
2. **Create Task Proposals** - Analyze issues, propose improvements
3. **Submit Code + Tasks (RED)** - Get expert feedback on both
4. **Merge Task Lists** - Combine our ideas + expert suggestions
5. **Submit for Approval** - Validate approach (target ≥4.5/5)
6. **Implement (REFACTOR)** - Execute approved tasks
7. **Submit for Final Review** - Get final ratings (target ≥4.5/5)
8. **Check Exit** - If rating ≥ target: complete, else loop

**MCP Integration**: Use Experts MCP (`ask_bob`, `ask_martin`) for reviews.

**Exit Criteria**: Average rating ≥4.5/5, all CRITICAL/HIGH tasks done, measurable improvement.

---

## Common TDD Anti-Patterns to Avoid

❌ **Writing tests after implementation** - Defeats purpose of TDD
❌ **Testing implementation details** - Tests should test behavior
❌ **Flaky tests** - Tests must be deterministic
❌ **Slow tests** - Unit tests should be <100ms
❌ **Tests with shared state** - Each test must be isolated
❌ **Skipping refactor phase** - Code quality degrades
❌ **Too much code in GREEN** - Write minimal code to pass

---

## TDD Benefits

✅ **Prevents regressions** - Changes caught immediately
✅ **Ensures testability** - Code designed to be testable
✅ **Documents behavior** - Tests serve as living documentation
✅ **Reduces bugs** - Issues caught early in development
✅ **Enables refactoring** - Safety net for changes
✅ **Improves design** - Forces thinking about interfaces first

---

**See Also**:
- [TDD Quick Reference](../references/tdd-quick-ref.md) - Quick lookup
- [Principle V: Quality Gates](05-quality-gates.md) - Coverage requirements
- [Glossary: Critical Path](../glossary.md#critical-path) - 100% coverage required
- [Standard Feature Workflow](../workflows/standard-feature.md) - TDD in context
