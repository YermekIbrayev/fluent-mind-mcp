# Principle V: Security and Quality Gates

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Quality Gates Reference](../references/quality-gates-ref.md), [TDD](02-tdd.md)

**Prerequisites**: Understand [Work Type Categories](../glossary.md#work-type-categories)

---

## Mandate

Before committing Production Code, all applicable gates must pass.

---

## 5.1 Security Scanning (Semgrep MCP)

**Purpose**: Prevent security vulnerabilities from entering the codebase.

### Pre-Commit Requirements
- No high or critical vulnerabilities
- Medium vulnerabilities tracked and addressed
- No known security anti-patterns
- Dependency vulnerability check

### Vulnerability Severity Handling

| Severity | CVSS Score | Action | Timeline |
|----------|-----------|---------|----------|
| **Critical** | 9.0-10.0 | Block all commits immediately | Fix before any other work |
| **High** | 7.0-8.9 | Block commits in affected areas | Must fix within 7 days |
| **Medium** | 4.0-6.9 | Create GitHub issue, label `security-medium` | Address within 30 days |
| **Low** | 0.1-3.9 | Create GitHub issue, label `security-low` | Review quarterly |

### Integration Points
- **Pre-commit hooks**: Fast scan on changed files
- **CI/CD pipeline**: Full repository scan
- **Pull request checks**: Block merge if high/critical found

---

## 5.2 Test Coverage Requirements

**Purpose**: Ensure code is thoroughly tested to prevent regressions.

### Coverage Thresholds
- **Production Code**: ≥80% overall coverage (minimum)
- **Critical Paths**: 100% coverage (no exceptions)
- **Integration Tests**: <5s per test
- **Unit Tests**: <100ms per test

See [Glossary: Critical Path](../glossary.md#critical-path) for definition.

### Test Quality Standards
- All tests must **pass** (no flaky tests)
- No skipped tests in Production Code
- Test names must be **descriptive**
- Tests must be **isolated** (no shared state)
- Coverage must include **edge cases**

### Work Type Requirements
- **Production Code**: Full coverage requirements apply
- **Infrastructure Code**: Tests recommended but not required
- **Experimental Code**: Tests optional

---

## 5.3 Code Quality Metrics

**Purpose**: Maintain code readability, maintainability, and performance.

### IDE MCP Diagnostics
- No type errors
- No syntax errors
- No unused imports/variables
- Linting rules enforced

### Complexity Limits
- **Cyclomatic complexity**: ≤10 per function
- **Nesting depth**: ≤3 levels
- **Function length**: ≤50 lines (guideline)
- **Code duplication**: No duplicates >6 lines

When complexity >5, consider refactoring using Strategy, Factory, or Command patterns.

See [Glossary: Complex Logic](../glossary.md#complex-logic) for examples.

### Documentation Requirements
- All public APIs documented
- [Complex logic](../glossary.md#complex-logic) has explanatory comments
- [Critical paths](../glossary.md#critical-path) have inline documentation

See [Principle VII: Documentation](07-documentation.md) for full requirements.

### Vibe-Check Validation (for new patterns)
- Approach is sound
- No hidden assumptions
- No tunnel vision

---

## 5.4 Quality Gates by Work Type

### Production Code (All Gates Required)

1. ✓ **Semgrep MCP Security Scan** - No high/critical vulnerabilities
2. ✓ **IDE MCP Diagnostics** - All checks pass
3. ✓ **Test Suite (TDD Green)** - All tests pass, coverage ≥80%
4. ✓ **Vibe-Check MCP Validation** - For new patterns/approaches
5. ✓ **Code Quality Metrics** - Complexity ≤10, no duplication
6. ✓ **Documentation** - Per [decision tree](07-documentation.md)
7. ✓ **Test Coverage** - ≥80% overall, 100% Critical Path

**No exceptions** - All gates must pass for Production Code.

---

### Infrastructure Code (Relaxed Gates)

1. ✓ **Semgrep MCP Security Scan** - High/critical only
2. ✓ **IDE MCP Diagnostics** - All checks pass
3. ⚠️ **Tests** - Recommended (validate configs, test scripts)
4. ⚠️ **Links** - Must be valid (if documentation)

**Rationale**: Infrastructure code has lower risk, relaxed requirements appropriate.

---

### Experimental Code (Minimal Gates)

- **No gates required** during experimentation
- Run locally for feedback (optional)
- **Must document learnings** to Pieces MCP before closing
- **Cannot merge to main** without meeting Production Code standards

**Rationale**: Encourage experimentation without bureaucracy, but require documentation.

---

## CI/CD Enforcement

**Pre-commit hooks**:
- Run gates locally before commit
- Fast feedback loop
- Catch issues early

**CI/CD pipeline**:
- Validates on server before merge
- Full test suite execution
- Security scan complete repository
- Failed gates **block PR merge**

See [CI/CD and Automation](../cicd.md) for pipeline details.

---

## Quality Gate Anti-Patterns

❌ **Skipping gates for "quick fixes"** - Technical debt accumulates
❌ **Ignoring medium vulnerabilities** - Become high over time
❌ **Accepting flaky tests** - Erodes confidence in test suite
❌ **Disabling pre-commit hooks** - Pushes problems to CI/CD
❌ **"Will fix later" mentality** - Later never comes

---

## Quality Gate Benefits

✅ **Prevent vulnerabilities** - Catch security issues early
✅ **Maintain code health** - Consistent quality standards
✅ **Enable safe iteration** - Confidence in changes
✅ **Reduce technical debt** - Issues caught before merge
✅ **Faster debugging** - Well-tested code easier to debug
✅ **Team confidence** - Trust in codebase quality

---

**See Also**:
- [Quality Gates Reference](../references/quality-gates-ref.md) - Quick lookup
- [Principle II: TDD](02-tdd.md) - Test coverage requirements
- [Glossary: Critical Path](../glossary.md#critical-path) - 100% coverage required
- [Glossary: Work Type Categories](../glossary.md#work-type-categories) - Classification
- [CI/CD: Quality Gates Flow](../cicd.md#quality-gates-flow) - Pipeline diagram
