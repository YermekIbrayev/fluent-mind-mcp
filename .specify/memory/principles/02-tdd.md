# Principle II: Test-First Development (NON-NEGOTIABLE)

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Quality Gates](05-quality-gates.md), [Standard Workflow](../workflows/standard-feature.md)

**Prerequisites**: Understand [Critical Path](../glossary.md#critical-path) definition

---

## Mandate

TDD is **required** for all Production Code - tests before implementation.

---

## The Sacred Cycle (Red-Green-Refactor)

```
RED → Approve (if needed) → GREEN → Verify → REFACTOR → Repeat
```

### Steps

**1. RED - Write Failing Test**
- Demonstrate the requirement through a test
- Test must fail for the right reason
- Defines expected behavior

**2. Approve (if needed for new patterns/critical paths)**
- Get approval via User or Vibe-Check MCP
- Fast-track for routine tests (see below)

**3. GREEN - Write Minimal Code**
- Write just enough code to pass the test
- Don't add extra features
- Focus on making it work

**4. Verify - Confirm Test Passes**
- All tests still green
- Implementation satisfies test

**5. REFACTOR - Improve Quality**
- Improve code quality while keeping tests green
- Reduce complexity, improve readability

**6. Repeat**
- Continue cycle for next functionality

---

## Approval Process

### Approval Required For:
- New test patterns or testing strategies
- Critical path tests (security, data, APIs)
- Non-obvious test scenarios
- First test for new module/feature

### Fast-Track (No Approval) For:
- Routine tests following established patterns
- Additional test cases for existing scenarios
- Refactoring existing tests
- Bug fix tests following patterns

---

## Quality Metrics

| Metric | Requirement | Notes |
|--------|-------------|-------|
| **Test Coverage** | ≥80% overall | 100% for Critical Paths |
| **Unit Tests** | <100ms per test | Isolated, no shared state |
| **Integration Tests** | <5s per test | Can use dependencies |
| **All Tests Pass** | Required | No flaky tests |
| **Test Isolation** | Required | No shared state |

---

## Work Type Requirements

**Production Code**:
- Full TDD required, ≥80% coverage
- RED-GREEN-REFACTOR cycle mandatory

**Infrastructure Code**:
- Tests recommended, best effort coverage
- TDD cycle optional

**Experimental Code**:
- Tests optional during exploration
- Must convert to Production standards before merging to main

---

**See Also**:
- [Principle V: Quality Gates](05-quality-gates.md) - Coverage enforcement
- [Standard Feature Workflow](../workflows/standard-feature.md) - TDD in practice
- [Glossary: Critical Path](../glossary.md#critical-path) - Definition
