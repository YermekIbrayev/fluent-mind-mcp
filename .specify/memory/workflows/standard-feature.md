# Standard Feature Implementation Workflow

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: All principles, [Quick Fix Flow](quick-fix.md), [Research Flow](research.md)

---

## Overview

The standard workflow integrates all constitution principles into a repeatable, auditable process with 4 phases.

---

## Phase 1: Planning & Specification

**Purpose**: Define requirements and validate approach before coding.

### Steps

**1. Create Specification** (`/speckit.specify`)
- Define [required elements](../principles/03-spec-driven.md#required-specification-elements)
- See [Principle III](../principles/03-spec-driven.md)

**2. Clarify Ambiguities** (`/speckit.clarify`)
- Identify underspecified areas
- Iterate until clear

**3. Plan Implementation** (based on [complexity](../principles/04-planning.md))
- Trivial: no plan needed
- Simple: 1 file
- Moderate: 2 files
- Complex: 4 files

**4. Validate Approach** (Vibe-Check MCP)
- Catch assumptions
- Validate soundness

**5. Generate Tasks** (`/speckit.tasks`)
- Actionable, dependency-ordered tasks

### Deliverables
- ✅ Specification created and clarified
- ✅ Execution plan (if needed)
- ✅ Approach validated
- ✅ Ready to write tests

---

## Phase 2: Implementation & Testing

**Purpose**: Write code following TDD cycle with incremental validation.

### TDD Cycle (Repeat until feature complete)

**1. Test (RED)** - Write failing tests
- Demonstrate requirement through test
- Test must fail for right reason
- See [Principle II: TDD](../principles/02-tdd.md)

**2. Approve (if needed)** - Get approval for tests
- New patterns/critical paths: Approval required
- Routine tests: Fast-track
- Via User or Vibe-Check MCP

**3. Implement (GREEN)** - Write minimal code
- Just enough to pass test
- No extra features

**4. Refactor** - Improve quality
- While keeping tests green
- Complexity ≤10 per function

### Deliverables
- ✅ All tests passing (GREEN)
- ✅ Code refactored for quality
- ✅ Ready for quality gates

**Note**: If spec gaps found, return to Phase 1 per [Iteration Protocol](../principles/03-spec-driven.md#specification-iteration-protocol)

---

## Phase 3: Validation & Documentation

**Purpose**: Ensure quality standards met and knowledge captured.

### Steps

**1. Run Quality Gates**
- Production: ALL gates (see [Principle V](../principles/05-quality-gates.md))
- Infrastructure: Relaxed gates
- Experimental: Minimal gates

**2. Update Documentation**
- Per [documentation decision tree](../principles/07-documentation.md)
- README if new directory
- API docs if public API
- ADR if architectural decision

**3. Create ADRs** (if applicable)
- For architectural decisions
- See [Principle VI](../principles/06-knowledge.md)

**4. Save Learnings** (Pieces MCP)
- Use `/speckit.analyze` for consistency check
- Capture important decisions
- Document complex problems solved

### Deliverables
- ✅ All quality gates passed
- ✅ Documentation updated
- ✅ Learnings saved to Pieces
- ✅ Ready to commit

---

## Phase 4: Review & Completion

**Purpose**: Finalize changes and verify consistency.

### Steps

**1. Update Execution Log** (if complex)
- Record actual vs planned execution
- Note lessons learned

**2. Save Knowledge** (Pieces MCP)
- Important patterns discovered
- Complex problems solved
- Integration patterns

**3. Commit Changes** (GitHub MCP)
- Only after all gates pass
- Clear commit message

**4. Create PR** (if needed)
- Clear description
- Link to spec/plan

**5. Code Review**
- Per team size requirements
- Constitution compliance check

**6. Execute Analysis** (`/speckit.analyze`)
- Verify cross-artifact consistency
- Ensure spec matches implementation

### Deliverables
- ✅ Code committed
- ✅ PR created and reviewed (if needed)
- ✅ Spec-kit analysis passed
- ✅ Feature complete

---

## Workflow Summary

```
Phase 1: Planning
  Specify → Clarify → Plan → Validate → Tasks

Phase 2: Implementation
  Test (RED) → Approve → Implement (GREEN) → Refactor → Repeat

Phase 3: Validation
  Quality Gates → Document → ADRs → Learn

Phase 4: Completion
  Log → Commit → PR → Review → Analyze → Done
```

---

**See Also**:
- [Quick Fix Flow](quick-fix.md) - For small changes
- [Research/Investigation Flow](research.md) - For exploration
- All 8 Principles referenced throughout
