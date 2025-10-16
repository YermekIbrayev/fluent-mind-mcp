# Principle VII: Documentation Excellence

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Knowledge Management](06-knowledge.md), [Token-Efficient Architecture](08-architecture.md)

---

## Guideline

Documentation is code - it must be reviewed, tested, and maintained.

---

## Documentation Decision Tree

```
What changed?
├─ User-Facing Feature? → YES → Specification Required
├─ Architectural Decision? → YES → ADR Required
├─ Public API? → YES → API Docs Required
├─ New Directory? → YES → README.md Required
└─ Internal Code → Optional (use inline comments)
```

---

## README.md Requirements

### Required When
- Project root (always)
- Major feature directories
- Public packages
- New significant modules

### Structure (20 lines max, token-optimized)

**Purpose (2 lines max)**: Clear, concise description

**Quick Start (5 lines max)**: Installation and basic usage

**Architecture (5 lines max)**:
- Core responsibility
- Dependencies
- Interface
- Data flow
- Integration points

**Dependencies (3 lines max)**: Required, optional, peer dependencies

**Common Tasks (5 lines max)**: Run tests, build, debug, deploy, troubleshooting

### Why 20 Lines?
- AI can parse entire README in single glance
- 90% token reduction
- Improved comprehension speed

---

## Comment Strategy

### Core Rule
Document WHY, not WHAT (maximum 2 lines per comment)

### Comment Types

**Business Logic**: Explain domain rules and constraints

**Non-Obvious Implementation**: Complexity justification

**Warning Comments**: Critical do-not-change warnings

**TODO Comments**: With ownership and tracking ID

### What NOT to Comment
- Variable declarations
- Simple getters/setters
- Standard library usage
- Self-documenting code

---

## Documentation Quality Standards

- Code examples must be tested
- Links must be valid (automated checking in CI/CD)
- Versioning for API breaking changes (migration guides)
- Screenshots/diagrams for UI and architecture
- Changelog maintained for all releases

---

**See Also**:
- [Principle VI: Knowledge Management](06-knowledge.md) - ADR format
- [Principle VIII: Token-Efficient Architecture](08-architecture.md) - Token optimization
- [Principle III: Specification-Driven](03-spec-driven.md) - Specification requirements
