# Standard Feature Implementation Workflow

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: All principles, [Quick Fix Flow](quick-fix.md), [Research Flow](research.md)

**Diagram**: [View Standard Workflow](../diagrams/standard-workflow.mermaid)

---

## Overview

The standard workflow integrates all constitution principles into a repeatable, auditable process with 4 phases.

**Phases**:
1. 🔵 **Planning & Specification** - Define requirements
2. 🟡 **Implementation & Testing** - TDD cycle
3. 🟠 **Validation & Documentation** - Quality gates
4. 🟢 **Review & Completion** - Finalize and merge

---

## Phase 1: Planning & Specification

**Purpose**: Define requirements and validate approach before coding.

### Steps

**1. Specify** - Create feature spec
- Use `/speckit.specify`
- Define [required elements](../principles/03-spec-driven.md#required-specification-elements)
- See [Principle III](../principles/03-spec-driven.md)

**2. Clarify** - Identify gaps
- Use `/speckit.clarify`
- Address ambiguities
- Iterate until clear

**3. Plan** - Create execution plan
- Create `.plans/` based on [complexity](../principles/04-planning.md#graduated-planning-levels)
- Trivial: no plan needed
- Simple: 1 file
- Moderate: 2 files
- Complex: 4 files

**4. Validate** - Vibe-Check approach
- Use Vibe-Check MCP
- Catch assumptions
- Validate soundness

### Prerequisites
- Feature request or requirement identified

### Deliverables
- ✅ Specification created and clarified
- ✅ Execution plan (if needed)
- ✅ Approach validated
- ✅ Ready to write tests

---

## Phase 2: Implementation & Testing

**Purpose**: Write code following TDD cycle with incremental validation.

### Steps

**5. Test (RED)** - Write failing tests
- Demonstrate requirement through test
- Test must fail for right reason
- See [Principle II: TDD](../principles/02-tdd.md)

**6. Approve (if needed)** - Get approval for tests
- New patterns/critical paths: Approval required
- Routine tests: Fast-track
- Via User or Vibe-Check MCP
- See [TDD Approval Process](../principles/02-tdd.md#approval-process)

**7. Implement (GREEN)** - Write minimal code
- Just enough to pass test
- No extra features
- Keep it simple

**8. Refactor** - Improve quality
- While keeping tests green
- Reduce [complexity](../glossary.md#complex-logic) ≤10
- Improve readability

**Repeat 5-8** until feature complete

### Prerequisites
- Validated plan from Phase 1

### Deliverables
- ✅ All tests passing (GREEN)
- ✅ Code refactored for quality
- ✅ Complexity ≤10 per function
- ✅ Ready for quality gates

### Note
- For complex logic: Use Sequential Thinking MCP
- If spec gaps found: Return to Phase 1 per [Iteration Protocol](../principles/03-spec-driven.md#specification-iteration-protocol)

---

## Phase 3: Validation & Documentation

**Purpose**: Ensure quality standards met and knowledge captured.

### Steps

**9. Validate** - Run quality gates
- Run all applicable [quality gates](../principles/05-quality-gates.md#54-quality-gates-by-work-type)
- Production: ALL gates
- Infrastructure: Relaxed gates
- Experimental: Minimal gates

**10. Test UI** (if applicable) - Browser testing
- Use Chrome DevTools MCP
- Verify UI functionality
- Test user flows

**11. Log** (if complex) - Complete execution log
- If using 4-document planning
- Record actual execution
- Note deviations from plan
- See [Planning: Complex](../principles/04-planning.md#complex-11-steps-4-hours)

**12. Document** - Update docs
- Per [documentation decision tree](../principles/07-documentation.md#documentation-decision-tree)
- README if new directory
- API docs if public API
- ADR if architectural decision

**13. Learn** - Save insights
- Use Pieces MCP: `create_pieces_memory`
- Important decisions
- Complex problems solved
- Patterns discovered

### Prerequisites
- Refactored code from Phase 2

### Deliverables
- ✅ All quality gates passed
- ✅ UI tested (if applicable)
- ✅ Documentation updated
- ✅ Learnings saved to Pieces
- ✅ Ready to commit

---

## Phase 4: Review & Completion

**Purpose**: Finalize changes and verify consistency.

### Steps

**14. Commit** - Use GitHub MCP
- Only after all gates pass
- Follow [commit message format](../cicd.md#commit-message-format)
- Include spec/plan references if applicable

**15. Create PR** - Submit for review
- Via GitHub MCP
- Clear description
- Link to spec/plan

**16. Code Review** - Peer review
- Per [team size requirements](../team-adaptations.md)
- Solo: Self-review + Vibe-Check
- Small: 1 approver
- Large: 2+ approvers

**17. Analyze** - Consistency check
- Use `/speckit.analyze`
- Verify cross-artifact consistency
- Ensure spec matches implementation

### Prerequisites
- Quality-validated code from Phase 3

### Deliverables
- ✅ Code committed to repository
- ✅ PR created and reviewed
- ✅ Spec-kit analysis passed
- ✅ Feature complete

---

## Workflow Diagram Summary

```
Planning (Phase 1)
  ↓
Specify → Clarify → Plan → Validate
  ↓
Implementation (Phase 2)
  ↓
Test (RED) → Approve → Implement (GREEN) → Refactor → Repeat
  ↓
Validation (Phase 3)
  ↓
Quality Gates → UI Test → Log → Document → Learn
  ↓
Completion (Phase 4)
  ↓
Commit → PR → Review → Analyze → Done
```

---

**See Also**:
- [Quick Fix Flow](quick-fix.md) - For small changes
- [Research/Investigation Flow](research.md) - For exploration
- All 7 Principles referenced throughout
- [Quality Gates Reference](../references/quality-gates-ref.md)
- [TDD Quick Reference](../references/tdd-quick-ref.md)
