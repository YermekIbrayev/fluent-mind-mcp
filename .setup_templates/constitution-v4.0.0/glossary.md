# Constitution Glossary

**Version**: 4.0.0 | **Part of**: [Constitution](INDEX.md)

Definitions of key terms used throughout the constitution.

---

## Critical Path

**Definition**: Code that directly impacts security, data integrity, or system reliability.

**Criteria** (code is Critical Path when ANY apply):
- Handles authentication or authorization
- Performs data integrity operations (create, update, delete)
- Implements security-sensitive operations (encryption, validation, access control)
- Defines API contracts or public interfaces
- Manages user data or privacy controls

**Examples**:
- Authentication and authorization flows
- Database write operations
- API endpoint implementations
- Payment processing
- User data handling

**Requirement**: 100% test coverage (no exceptions)

**See Also**: [Principle II: Test-First Development](principles/02-tdd.md), [Principle V: Quality Gates](principles/05-quality-gates.md)

---

## Step

**Definition**: A discrete unit of work requiring a tool call, command execution, or decision point.

**Criteria** (counts as 1 step when):
- Requires single tool invocation (Read, Write, Bash, Git, etc.)
- Produces discrete, measurable output or state change
- Can be independently verified as complete/incomplete
- Execution time: <5 minutes

**Examples**:
- Reading a file = 1 step
- Running tests = 1 step
- Updating a spec = 1 step
- Making an architectural decision = 1 step

**Used in**: [Principle IV: Planning](principles/04-planning.md) for determining task complexity

**See Also**: [Planning Quick Reference](references/planning-ref.md)

---

## Architectural Decision

**Definition**: A choice that affects multiple components, is costly to reverse, or impacts system qualities.

**Criteria**:
- Affects multiple components/modules
- Difficult or costly to reverse
- Impacts performance, security, or scalability
- Changes public APIs or contracts

**Examples**:
- Database choice (PostgreSQL vs. MongoDB)
- Framework selection (React vs. Vue)
- API design pattern (REST vs. GraphQL)
- Authentication strategy (JWT vs. sessions)

**Decision Tree**:
```
Is this decision...
  └─ Isolated to one component?
      ├─ YES → Comment/note suffices
      └─ NO → Continue
           └─ Easy to reverse later?
               ├─ YES → Comment/note suffices
               └─ NO → Create ADR
```

**Documentation**: Create ADR in `.specify/memory/decisions/`

**See Also**: [Principle VI: Knowledge Management](principles/06-knowledge.md)

---

## Complex Logic

**Definition**: Code requiring explanation beyond the code itself.

**Criteria**:
- Cyclomatic complexity >5
- Multiple nested conditions (depth >2)
- Non-obvious algorithms
- Business logic that isn't self-documenting

**Example - Before (Complex)**:
```python
def calculate_discount(user, cart, promo):
    discount = 0
    if user.is_premium:
        discount += 0.10
        if cart.total > 100:
            discount += 0.05
    if promo and promo == "SAVE20":
        discount += 0.20
    return min(discount, 0.30)
# Complexity: 7, Test combinations: 128
```

**Example - After (Refactored)**:
```python
def calculate_discount(user, cart, promo):
    strategies = [
        PremiumUserDiscount(),
        HighValueCartDiscount(),
        PromoCodeDiscount(promo)
    ]
    return min(sum(s.apply(user, cart) for s in strategies), 0.30)
# Complexity: 2, Test combinations: 4
```

**When complexity >5**: Refactor using Strategy, Factory, or Command patterns

**See Also**: [Principle II: TDD](principles/02-tdd.md#refactor-phase), [Sequential Thinking MCP](references/mcp-servers-ref.md)

---

## Trivial Task

**Definition**: Work that takes <15 minutes, requires 1-2 steps, has no edge cases.

**Criteria** (qualifies as trivial when ALL true):
- **Time**: <15 minutes from start to completion
- **Steps**: 1-2 discrete steps maximum
- **Risk**: No edge cases, error handling, or validation needed
- **Scope**: Single file OR single small component affected
- **Testing**: No new tests required (or trivial test update)

**Examples**:
- Fix typo in documentation
- Update dependency version
- Add log statement
- Rename variable for clarity

**Planning**: No formal planning required (inline TODOs acceptable)

**See Also**: [Principle IV: Planning](principles/04-planning.md), [Planning Quick Reference](references/planning-ref.md)

---

## Work Type Categories

**Definition**: Classification system for code with different quality gate requirements.

### Production Code
**Description**: Application logic, API implementations, data models, security components

**Quality Gates**: ALL apply
- Semgrep MCP security scan
- IDE MCP diagnostics
- Tests pass (TDD required)
- Coverage ≥80% (100% Critical Path)
- Vibe-Check MCP validation
- Documentation required
- Code quality metrics (complexity ≤10)

**Examples**: User authentication, API endpoints, data models, business logic

### Infrastructure Code
**Description**: Build scripts, CI/CD configs, documentation, configuration files

**Quality Gates**: RELAXED
- Semgrep high/critical only
- IDE diagnostics
- Tests recommended
- Links must be valid (if docs)

**Examples**: GitHub Actions workflows, build scripts, README files, config files

### Experimental Code
**Description**: Prototypes, spikes, proof-of-concepts

**Quality Gates**: MINIMAL
- Must document learnings to Pieces MCP
- Use spike/* branches
- Cannot merge to main without meeting Production standards

**Examples**: Proof of concepts, architecture spikes, exploratory code

**Decision Tree**:
```
Which Work Type?
├─ Production application logic? → Production Code
├─ Build/CI/docs/config? → Infrastructure Code
├─ Prototype/spike/POC? → Experimental Code
└─ Unsure? → Default to Production (safest)
```

**See Also**: [Principle V: Quality Gates](principles/05-quality-gates.md), [Quality Gates Reference](references/quality-gates-ref.md)

---

## Vertical Slice Architecture

**Definition**: Organizing code by feature/functionality rather than technical layers.

**Structure**:
```
feature_name/
├── models.py      # Feature-specific data models
├── service.py     # Business logic
├── controller.py  # API/HTTP handlers
├── validators.py  # Input validation
├── tests/         # All feature tests
└── README.md      # Feature documentation
```

**Benefits**:
- 80% reduction in context loading
- Clear ownership boundaries
- Faster AI comprehension
- Easier testing and maintenance

**See Also**: [Principle VIII: Architecture](principles/08-architecture.md), [Architecture Quick Ref](quick-refs/architecture.md)

---

## Context Budget

**Definition**: Systematic approach to managing AI context window allocation.

**Allocation**:
- **Must-Have (20%)**: Essential files for current task
- **Should-Have (30%)**: Supporting context
- **Reserve (50%)**: AI working memory

**Example**:
```
Task: Fix validation bug
Must-Have: validators.py, test_validators.py (20%)
Should-Have: models.py, service.py (30%)
Reserve: Keep available for AI operations (50%)
```

**See Also**: [Context Budget Planning](principles/04-planning.md#context-budget-planning), [Token Optimization](quick-refs/token-optimization.md)

---

## Token Optimization

**Definition**: Strategies to reduce AI token consumption while maintaining code quality.

**Key Metrics**:
- Average file size: <150 lines (target)
- Files >200 lines: <5% of codebase
- Vertical slice adoption: >80%
- Token reduction: 50% from baseline

**Techniques**:
1. File size limits (200 lines max)
2. Vertical slice architecture
3. Context budget planning
4. AI-friendly naming conventions
5. Concise documentation (20-line READMEs)

**See Also**: [Token Metrics](cicd.md#token-metrics-track-weekly), [All Quick Refs](quick-refs/)

---

## Additional Terms

### TDD (Test-Driven Development)
**Definition**: Development methodology where tests are written before implementation.

**Cycle**: RED (failing test) → GREEN (minimal code) → REFACTOR (improve quality)

**See**: [Principle II: TDD](principles/02-tdd.md), [TDD Quick Reference](references/tdd-quick-ref.md)

### MCP (Model Context Protocol)
**Definition**: Protocol for AI assistants to interact with external tools and servers.

**See**: [Principle I: MCP-First](principles/01-mcp-first.md), [MCP Servers Reference](references/mcp-servers-ref.md)

### ADR (Architecture Decision Record)
**Definition**: Document capturing important architectural decisions.

**Location**: `.specify/memory/decisions/`

**See**: [Principle VI: Knowledge Management](principles/06-knowledge.md), [Architectural Decision](#architectural-decision)

### Cyclomatic Complexity
**Definition**: Metric measuring number of independent paths through code.

**Limit**: ≤10 per function

**See**: [Complex Logic](#complex-logic), [Principle V: Quality Gates](principles/05-quality-gates.md)

---

**Navigation**: [Back to Index](INDEX.md)
