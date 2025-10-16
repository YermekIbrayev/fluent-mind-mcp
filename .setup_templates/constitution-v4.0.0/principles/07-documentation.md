# Principle VII: Documentation Excellence

**Version**: 4.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Spec-Driven Development](03-spec-driven.md), [Knowledge Management](06-knowledge.md)

---

## Guideline

Documentation is code - it must be reviewed, tested, and maintained.

---

## Documentation Decision Tree

**Diagram**: [View Decision Tree](../diagrams/documentation-tree.mermaid)

**Text Flow**:
```
What changed?
├─ User-Facing Feature? → YES → Specification Required
├─ Architectural Decision? → YES → ADR Required
├─ Public API? → YES → API Docs Required
├─ New Directory? → YES → README.md Required
└─ Internal Code → Optional (use inline comments)
```

---

## Documentation Requirements

### README.md

**Required When:**
- Project root (always)
- Major feature directories
- Public packages/libraries
- New significant modules

**Optional When:**
- Small utility directories (use file-level comments instead)
- Single-file modules

**Must Include:**
- Purpose (what this is)
- Usage (how to use it)
- Prerequisites (dependencies)
- Examples (code samples)
- References (related docs)

### README Structure (Token-Optimized)

**Maximum Length**: 20 lines total

**Required Structure**:
```markdown
# Component/Feature Name

## Purpose (2 lines max)
[Clear, concise description of what this component does and why it exists]

## Quick Start (5 lines max)
```bash
# Installation or setup command
npm install feature-name
# Basic usage example
import { Feature } from './feature';
const result = Feature.process(data);
```

## Architecture (5 lines max)
- Core responsibility: [what it does]
- Key dependencies: [what it needs]
- Main interface: [how to interact]
- Data flow: [input → processing → output]
- Integration points: [where it connects]

## Dependencies (3 lines max)
- Required: package1 (^2.0.0), package2 (^1.5.0)
- Optional: package3 (for feature X)
- Peer: framework (^4.0.0)

## Common Tasks (5 lines max)
- Run tests: `npm test`
- Build: `npm run build`
- Debug: Set DEBUG=feature:* environment variable
- Deploy: See deployment/README.md
- Troubleshooting: Check logs in logs/feature.log
```

**Why 20 Lines?**
- AI can parse entire README in single glance
- Forces clarity and conciseness
- Reduces token consumption by 90%
- Improves comprehension speed
- Additional details go in separate docs

---

### Comment Strategy

**Core Rule**: Document WHY, not WHAT

**Maximum Length**: 2 lines per comment

**When to Comment**:
```python
# Good: Explains business logic
def calculate_discount(user, cart):
    # Premium users get 20% off as per Q3 2024 pricing strategy
    # Stacks with promotional codes but not sale items
    if user.is_premium:
        return cart.total * 0.8
```

```python
# Bad: Explains obvious code
def calculate_discount(user, cart):
    # Check if user is premium
    # If yes, multiply total by 0.8
    if user.is_premium:
        return cart.total * 0.8
```

**Comment Types**:

1. **Business Logic Comments**:
```python
# EU customers exempt from sales tax per VAT regulations
# Rate varies by country, see tax_config.yaml
```

2. **Non-Obvious Implementation**:
```python
# Using binary search here because list is pre-sorted
# Reduces complexity from O(n) to O(log n) for 10k+ items
```

3. **Warning Comments**:
```python
# CRITICAL: Do not change order - payment gateway expects exact sequence
# Changing will cause transaction failures
```

4. **TODO Comments** (with ownership):
```python
# TODO(alice): Implement retry logic by 2024-03-01
# Tracked in JIRA-1234
```

**What NOT to Comment**:
- Variable declarations with clear names
- Simple getters/setters
- Standard library usage
- Self-documenting code
- Implementation details that code expresses

**Comment Placement**:
```python
# Function-level: Above function definition
def process_payment(order):
    # Complex algorithm: Above the complex part
    if order.requires_3d_secure:
        # Line-level: Sparingly, only for warnings
        validate_3d_secure(order)  # MUST complete within 30s SLA
```

---

### Specification

**Required When:**
- User-facing features
- Public APIs
- Production Code features
- Multi-component changes

**Optional When:**
- Internal refactorings
- Infrastructure Code
- Minor improvements

**Not Required:**
- Experimental Code (document learnings instead)
- Documentation-only changes
- Typo fixes

See [Principle III: Spec-Driven](03-spec-driven.md) for full requirements.

---

### Architecture Decision Record (ADR)

**Required When:**
- Decision meets [Architectural Decision](../glossary.md#architectural-decision) criteria
- Affects multiple components
- Costly to reverse
- Impacts system qualities

**Optional When:**
- Implementation details within well-defined scope
- Single-component choices
- Easily reversible decisions

See [Principle VI: Knowledge Management](06-knowledge.md) for ADR format.

---

### API Documentation

**Required When:**
- All public functions
- All public classes
- All public modules
- External APIs

**Optional When:**
- Private/internal code (use inline comments)
- Self-documenting simple functions

**Must Include:**
- Purpose and behavior
- Parameters and types
- Return value and type
- Error conditions
- Examples
- Side effects

---

## Quick Reference Table

| Document Type | Required When | Optional When |
|---------------|--------------|---------------|
| **README.md** | Project root, major feature directories | Small utility directories |
| **Specification** | User-facing features, public APIs, Production Code | Internal refactorings, Infrastructure Code |
| **ADR** | [Architectural Decision](../glossary.md#architectural-decision) criteria met | Implementation details within scope |
| **API Documentation** | All public functions, classes, modules | Private/internal code |

**When in Doubt**: Ask Vibe-Check MCP if documentation is warranted.

---

## Documentation Quality Standards

### Code Examples Must Be Tested
- Examples must actually work
- Include in test suite
- Keep up-to-date with code changes

**Anti-Pattern**: Outdated examples that don't run.

### Links Must Be Valid
- Automated link checking in CI/CD
- No broken internal links
- External links reviewed quarterly

**Anti-Pattern**: Documentation full of 404s.

### Versioning for API Breaking Changes
- Document version changes
- Migration guides for breaking changes
- Deprecation warnings

**Anti-Pattern**: Undocumented breaking changes.

### Screenshots/Diagrams for UI and Architecture
- Visual aids for complex concepts
- Keep synchronized with implementation
- Use diagrams/ directory for Mermaid

**Anti-Pattern**: Diagrams that don't match reality.

### Changelog Maintained
- All releases documented
- Breaking changes highlighted
- Migration guides provided

**Anti-Pattern**: No changelog, users confused by changes.

---

## Documentation Anti-Patterns

❌ **Writing docs after the fact** - Details forgotten
❌ **Copy-paste documentation** - Inconsistencies
❌ **Stale documentation** - Worse than no docs
❌ **No examples** - Users can't understand
❌ **Too much/too little** - Find balance
❌ **Broken links** - Erodes trust
❌ **Undocumented breaking changes** - User frustration

---

## Documentation Benefits

✅ **Faster onboarding** - New team members up to speed quickly
✅ **Reduced support burden** - Self-service answers
✅ **Better API design** - Forced to think through usage
✅ **Knowledge preservation** - Context doesn't disappear
✅ **Easier maintenance** - Future changes informed by past
✅ **Professional image** - Quality documentation = quality project

---

## Documentation Workflow

### During Feature Development

1. **Specification** - Created before coding (see [Principle III](03-spec-driven.md))
2. **Inline Comments** - For [complex logic](../glossary.md#complex-logic)
3. **API Docs** - As public interfaces defined
4. **README** - When new directory created

### After Feature Completion

1. **Review Documentation** - Ensure accuracy
2. **Add Examples** - Real usage scenarios
3. **Test Examples** - Verify they work
4. **Update Changelog** - Record changes
5. **Check Links** - Automated validation

### During Code Review

1. **Verify Docs Exist** - Per decision tree
2. **Check Accuracy** - Matches implementation
3. **Test Examples** - Actually work
4. **Validate Links** - No broken links

---

## Documentation Checklist

Before merging, verify:

**For User-Facing Features:**
- [ ] Specification exists and up-to-date
- [ ] API documentation complete
- [ ] Examples provided and tested
- [ ] README updated
- [ ] Changelog entry added

**For Internal Changes:**
- [ ] Complex logic has comments
- [ ] ADR created if architectural decision
- [ ] Inline documentation adequate

**For All Changes:**
- [ ] Links validated
- [ ] Code examples tested
- [ ] No outdated references

---

**See Also**:
- [Principle III: Spec-Driven](03-spec-driven.md) - Specification requirements
- [Principle VI: Knowledge Management](06-knowledge.md) - ADR format
- [Glossary: Architectural Decision](../glossary.md#architectural-decision) - When ADR needed
- [CI/CD: Documentation Checks](../cicd.md) - Automated validation
