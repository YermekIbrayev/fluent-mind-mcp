# Principle VIII: Token-Efficient Architecture

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Planning](04-planning.md), [Documentation](07-documentation.md)

---

## Purpose

Optimize codebase architecture for AI-assisted development by minimizing token consumption while maximizing context relevance.

---

## 8.1 Vertical Slice Architecture

**Requirements**:
- **MUST** organize code by feature, not by technical layer
- **MUST** colocate all related code within feature boundaries
- **MUST** ensure each feature is self-contained and independently comprehensible

**Structure**:
```
feature_name/
  ├── models.py       # Feature-specific models (100 lines max)
  ├── service.py      # Business logic (150 lines max)
  ├── controller.py   # API/HTTP handlers (100 lines max)
  ├── validators.py   # Input validation (50 lines max)
  ├── tests/          # All feature tests
  └── README.md       # Feature documentation (20 lines)
```

**Benefits**:
- 80% reduction in context loading
- Clear ownership
- Faster AI comprehension
- Reduced cross-file dependencies

---

## 8.2 File Size Limits

- **Maximum**: 200 lines per file (enforced by CI/CD)
- **Target**: 100 lines per file (ideal for AI context)
- **Warning**: 150 lines per file (consider splitting)

### Splitting Strategy

When file exceeds limits:
1. Identify logical boundaries
2. Extract related functionality
3. Create focused modules
4. Update imports and tests

---

## 8.3 Module Organization

**Single Responsibility**: Each module one clear purpose

**Explicit Exports**: All modules define `__all__`

**Clear Boundaries**:
- No circular imports
- Dependencies flow downward
- Features depend on shared not each other

---

## 8.4 Context Management Strategy

### Context Hierarchy

1. **Must-have context (20% of window)**: Direct dependencies, interfaces, tests
2. **Should-have context (30% of window)**: Related modules, parent abstractions, configuration
3. **Optional context (50% reserve)**: Documentation, historical decisions, similar features

### Progressive Loading

- Start minimal
- Add progressively
- Reserve 50% for AI operations
- Unload aggressively

---

## Naming Conventions

Use clear, searchable names optimized for AI comprehension. Avoid abbreviations.

---

## Metrics to Track Weekly

- Average lines per file
- Files exceeding 200 lines
- Vertical slice adoption %
- Token consumption per feature
- AI suggestion acceptance rate

---

## Success Indicators

- 50% reduction in tokens per feature
- 2x improvement in AI comprehension
- 30% faster feature development

---

## Exceptions Allowed

- Generated code
- Configuration files
- Legacy interfaces during migration (must document in ADR with remediation timeline)

---

**See Also**:
- [Principle IV: Planning](04-planning.md) - Context budget planning
- [Principle VII: Documentation](07-documentation.md) - README requirements
- [Quick Ref: File Limits](../quick-refs/file-limits.md)
- [Quick Ref: Architecture](../quick-refs/architecture.md)
