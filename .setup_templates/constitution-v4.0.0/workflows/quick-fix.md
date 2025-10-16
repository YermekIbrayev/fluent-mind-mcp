# Quick Fix Flow

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: [Standard Feature Workflow](standard-feature.md), [Quality Gates](../principles/05-quality-gates.md)

---

## Purpose

Streamlined workflow for small Infrastructure Code changes and trivial bug fixes.

**Use When:**
- Infrastructure Code fixes
- Small bug fixes (Production Code)
- Configuration updates
- Documentation fixes
- Dependency updates

**Don't Use For:**
- New features (use [Standard Workflow](standard-feature.md))
- Complex refactoring
- Multi-component changes

---

## Quick Fix Workflow

### 1. Identify Issue
- Use IDE MCP `getDiagnostics` for type errors
- Use Semgrep MCP for security issues
- Or manually identified issue

### 2. Test First (if Production Code)
- **Production Code bug**: Write failing test (TDD required)
- **Infrastructure Code**: Validate approach instead
- Skip for documentation-only changes

### 3. Fix
- Implement fix
- Keep change minimal and focused
- One issue per commit

### 4. Verify
- Run applicable tests
- Run relevant [quality gates](../principles/05-quality-gates.md#54-quality-gates-by-work-type):
  - Production: ALL gates
  - Infrastructure: Relaxed gates
- Verify fix resolves issue

### 5. Commit
- Use GitHub MCP with descriptive message
- Format:
  ```
  Fix: [brief description]

  - What was wrong
  - How it was fixed

  [references if applicable]
  ```

### 6. Learn (if mistake made)
- Use Vibe-Check `vibe_learn` if this was a mistake you made
- Document pattern to avoid future recurrence
- Example: `vibe_learn("Forgot to validate user input", "Input Validation", "Added validation check before processing")`

---

## Quality Gates by Type

**Production Code:**
- ✅ Test written and passing
- ✅ All quality gates passed
- ✅ Code reviewed (per team size)

**Infrastructure Code:**
- ✅ Validated locally
- ✅ Semgrep high/critical clean
- ✅ Links valid (if docs)

**Documentation:**
- ✅ Links validated
- ✅ Examples tested (if code examples)
- ✅ Spell check passed

---

## Examples

**Quick Fix for Production Bug:**
```
1. Write failing test demonstrating bug
2. Run test - verify it fails
3. Implement minimal fix
4. Run all tests - all pass
5. Run Semgrep, IDE diagnostics
6. Commit with descriptive message
```

**Quick Fix for Config:**
```
1. Identify config issue
2. Update config file
3. Validate locally (build works)
4. Run Semgrep (high/critical)
5. Commit with description
```

**Quick Fix for Documentation:**
```
1. Fix typo or update docs
2. Validate links
3. Test code examples (if any)
4. Commit with description
```

---

## When to Escalate

**Escalate to Standard Workflow if:**
- Fix touches multiple components
- Requires specification
- Takes >1 hour
- Reveals larger architectural issue
- Needs extensive testing

**Rule of Thumb**: If it feels complex, use [Standard Workflow](standard-feature.md).

---

**See Also**:
- [Standard Feature Workflow](standard-feature.md) - For complex changes
- [Principle II: TDD](../principles/02-tdd.md) - Test requirements
- [Principle V: Quality Gates](../principles/05-quality-gates.md) - Gate requirements
- [Glossary: Trivial Task](../glossary.md#trivial-task) - When minimal planning OK
