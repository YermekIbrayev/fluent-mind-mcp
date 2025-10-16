# Quality Gates Quick Reference

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > References

**Full Details**: [Principle V: Security and Quality Gates](../principles/05-quality-gates.md)

---

## Gates by Work Type

### Production Code (ALL Gates Required)

1. ✓ **Semgrep MCP** - Security scan clean (no high/critical vulnerabilities)
2. ✓ **IDE MCP** - Diagnostics clean (no type/syntax errors)
3. ✓ **Test Suite** - All tests pass (TDD Green)
4. ✓ **Test Coverage** - ≥80% overall, 100% Critical Path
5. ✓ **Vibe-Check MCP** - Approach validated (for new patterns)
6. ✓ **Documentation** - Per [decision tree](../principles/07-documentation.md)
7. ✓ **Code Quality** - Complexity ≤10, nesting ≤3

### Infrastructure Code (Relaxed Gates)

1. ✓ **Semgrep MCP** - High/critical vulnerabilities only
2. ✓ **IDE MCP** - Diagnostics clean
3. ⚠️ **Tests** - Recommended (validate configs)
4. ⚠️ **Links** - Must be valid (if documentation)

### Experimental Code (Minimal Gates)

- No gates required during experimentation
- **Must document learnings** to [Pieces MCP](../principles/06-knowledge.md) before closing
- Cannot merge to main without meeting Production Code standards

---

## Vulnerability Severity Actions

| Severity | CVSS | Action | Timeline |
|----------|------|--------|----------|
| **Critical** | 9.0-10.0 | Block all commits | Fix immediately |
| **High** | 7.0-8.9 | Block affected code | Fix within 7 days |
| **Medium** | 4.0-6.9 | Create GitHub issue | Fix within 30 days |
| **Low** | 0.1-3.9 | Create GitHub issue | Review quarterly |

---

## Code Quality Limits

- **Cyclomatic Complexity**: ≤10 per function
- **Nesting Depth**: ≤3 levels
- **Function Length**: ≤50 lines (guideline)
- **Code Duplication**: No duplicates >6 lines

---

## Coverage Thresholds

- **Production Code**: ≥80% overall
- **Critical Paths**: 100% (security, data, APIs)
- **Unit Tests**: <100ms per test
- **Integration Tests**: <5s per test

---

**See Also**:
- [Principle V: Security and Quality Gates](../principles/05-quality-gates.md) - Full details
- [Glossary: Critical Path](../glossary.md#critical-path) - Definition
- [CI/CD: Quality Gates Flow](../cicd.md#quality-gates-flow) - Pipeline
- [Glossary: Work Type Categories](../glossary.md#work-type-categories) - Classification
