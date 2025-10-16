# Principle III: Specification-Driven Development

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Planning](04-planning.md), [Documentation](07-documentation.md)

---

## Mandate

All Production features must have specifications before implementation.

---

## Spec-Kit Workflow

1. `/speckit.specify` - Create or update feature specification
2. `/speckit.clarify` - Identify underspecified areas
3. `/speckit.plan` - Execute implementation planning
4. `/speckit.tasks` - Generate actionable, dependency-ordered tasks
5. `/speckit.implement` - Execute the implementation plan
6. `/speckit.analyze` - Perform cross-artifact consistency check

---

## Required Specification Elements

Every specification must define:

### Purpose
- Why this feature exists
- What problem it solves
- Who benefits

### Acceptance Criteria
- Measurable success conditions
- Clear pass/fail conditions
- User-facing outcomes

### Edge Cases
- Boundary conditions
- Error scenarios
- Exceptional inputs
- Failure modes

### Performance Requirements
- Latency targets
- Throughput expectations
- Resource constraints
- Scalability needs

### Security Considerations
- Authentication requirements
- Authorization rules
- Data protection
- Input validation
- OWASP Top 10 review

### Dependencies
- External services
- Required libraries
- System requirements
- API dependencies

### API Contract
- Input parameters and types
- Output format and types
- Error codes and messages
- Versioning strategy

---

## Specification Iteration Protocol

Development is **iterative**. When implementation reveals spec issues:

### The Process

1. **Pause at Current Checkpoint**
   - Stop at a stable point
   - Don't continue with incomplete understanding

2. **Document Discovery**
   - Record what was learned in execution log
   - Note gaps, ambiguities, or conflicts

3. **Update Specification**
   - Revise spec with new information (`/speckit.specify`)
   - Add discovered requirements

4. **Re-Clarify if Needed**
   - Run `/speckit.clarify` for new ambiguities
   - Ensure full understanding

5. **Regenerate Tasks**
   - Run `/speckit.tasks` to update task list
   - Adjust implementation plan

6. **Resume Implementation**
   - Continue with updated understanding
   - Apply learnings forward

### Commit Message Format

```gitcommit
Update spec NNNN based on implementation findings

- Added edge case for X
- Revised API contract for Y
- Discovered technical constraint Z

spec:NNNN plan:0042
```

**Note**: Use spec/plan references to create traceability.

---

## When Specifications Are Required

### Required (Must Have Spec)
- User-facing features
- Public APIs
- Production Code features
- Multi-component changes
- Architectural changes

### Optional (Spec Recommended)
- Internal refactorings
- Infrastructure Code
- Minor improvements
- Bug fixes (small scope)

### Not Required (No Spec)
- Experimental Code (spike branches)
- Documentation-only changes
- Typo fixes
- Trivial updates

**Decision Rule**: If in doubt, ask Vibe-Check MCP if spec is warranted.

---

## Specification Benefits

✅ **Prevents scope creep** - Clear boundaries defined upfront
✅ **Clarifies requirements** - Shared understanding across team
✅ **Enables accurate planning** - Know what to build
✅ **Reduces rework** - Catch issues before coding
✅ **Provides documentation** - Living record of decisions
✅ **Facilitates review** - Clear criteria for evaluation

---

## Common Specification Anti-Patterns

❌ **Too vague** - "Make it user-friendly" (not measurable)
❌ **Too detailed** - Specifying implementation details
❌ **Ignoring edge cases** - Only happy path considered
❌ **No acceptance criteria** - Can't determine when done
❌ **Outdated specs** - Spec doesn't match reality
❌ **Writing spec during implementation** - Defeats purpose

---

## Specification Quality Checklist

Before implementing, verify spec has:

- [ ] Clear purpose statement
- [ ] Measurable acceptance criteria
- [ ] Edge cases identified
- [ ] Performance requirements defined
- [ ] Security considerations addressed
- [ ] Dependencies documented
- [ ] API contract specified (if applicable)
- [ ] Passed clarification review (`/speckit.clarify`)

---

**See Also**:
- [Principle IV: Planning](04-planning.md) - Planning after specification
- [Principle VII: Documentation](07-documentation.md) - Documentation requirements
- [Standard Feature Workflow](../workflows/standard-feature.md) - Spec in workflow
- [Glossary: Architectural Decision](../glossary.md#architectural-decision) - When ADR needed
