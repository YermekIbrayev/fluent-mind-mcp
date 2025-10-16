# TDD Quick Reference

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > References

**Full Details**: [Principle II: Test-First Development](../principles/02-tdd.md)

---

## The Sacred Cycle

**RED** → **Approve** (if needed) → **GREEN** → **REFACTOR** → Repeat

1. **RED**: Write failing test that demonstrates requirement
2. **Approve**: Get approval for new patterns/critical paths (User or Vibe-Check MCP)
3. **GREEN**: Write minimal code to pass the test
4. **REFACTOR**: Improve code quality while keeping tests green

---

## Approval Requirements

**Approval Required:**
- New test patterns or strategies
- Critical path tests (security, data, APIs)
- Non-obvious scenarios
- First test for new module

**Fast-Track (No Approval):**
- Routine tests following patterns
- Additional test cases
- Refactoring existing tests
- Bug fix tests following patterns

---

## Coverage Requirements

| Code Type | Coverage | Notes |
|-----------|----------|-------|
| **Production Code** | ≥80% overall | 100% for [Critical Path](../glossary.md#critical-path) |
| **Infrastructure Code** | Recommended | Validate configs, test scripts |
| **Experimental Code** | Optional | Document findings instead |

---

## Test Quality Standards

- All tests must **pass** (no flaky tests)
- Unit tests: **<100ms** per test
- Integration tests: **<5s** per test
- Tests must be **isolated** (no shared state)
- Test names must be **descriptive**

---

## Work Type Requirements

**Production Code**: Full TDD required (no exceptions)
**Infrastructure Code**: Tests recommended
**Experimental Code**: Tests optional (document learnings)

---

**See Also**:
- [Principle II: Test-First Development](../principles/02-tdd.md) - Full TDD workflow
- [Glossary: Critical Path](../glossary.md#critical-path) - Definition
- [Quality Gates: Test Coverage](../principles/05-quality-gates.md#52-test-coverage-requirements)
