# Quick Fix Flow

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: [Standard Feature Workflow](standard-feature.md), [Planning](../principles/04-planning.md)

---

## When to Use

For trivial tasks:
- ≤2 steps
- <15 minutes
- Single file changes
- No specification needed

---

## Examples

- Fix typo
- Update config value
- Add log statement
- Update dependency version (patch)
- Fix formatting

---

## Flow

### 1. Identify Issue
- Clear, well-defined problem
- Obvious solution
- No architectural impact

### 2. Implement Directly
- No planning required
- Make the change
- Keep it simple

### 3. Verify (if Production Code)
- Run existing tests
- Add test if bug fix (TDD still applies)
- Quick manual verification

### 4. Commit
- Clear commit message
- Reference issue number if applicable

---

## Quality Gates

**Production Code**:
- Tests must pass
- Add test for bug fix
- No security issues

**Infrastructure/Experimental**:
- Verify change works
- Basic validation

---

## When NOT to Use Quick Fix

❌ Don't use if:
- Touches multiple files
- Affects public API
- Requires specification
- Complex logic changes
- Architectural decision needed

**Use [Standard Feature Workflow](standard-feature.md) instead.**

---

**See Also**:
- [Standard Feature Workflow](standard-feature.md) - For non-trivial changes
- [Principle IV: Planning](../principles/04-planning.md) - Complexity guidelines
