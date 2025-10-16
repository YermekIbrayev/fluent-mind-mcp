# Clean Code

**Category**: Thinking & Planning | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Code planning and design with comprehensive documentation and clean code principles.

---

## Capabilities

- Step-by-step code architecture planning
- Design decision tracking with revisions
- Alternative implementation exploration
- Focus on SOLID principles
- Prioritize readability and maintainability
- Plan for testability from the beginning

---

## When to Use

- Before writing complex code
- Designing new features
- Refactoring existing code
- Planning testable implementations
- Breaking down complex functionality
- Ensuring comprehensive documentation strategy

---

## Planning Aspects

**Architecture & Design**:
- High-level structure and organization
- Component responsibilities
- Module boundaries

**Implementation Details**:
- Function signatures and interfaces
- Data structures
- Error handling approaches

**Quality Considerations**:
- Testing strategies
- Performance considerations
- Comment and documentation strategies

**Clean Code Principles**:
- Single Responsibility Principle
- Clear naming conventions
- Simplicity over cleverness
- Maximum 2 lines per comment (explain WHY, not WHAT)

---

## Key Parameters

- `thought` (required) - Current planning step
- `thoughtNumber` (required) - Current step number
- `totalThoughts` (required) - Estimated total steps
- `nextThoughtNeeded` (required) - Boolean, more planning needed
- `isRevision` (optional) - Revising previous design decision
- `revisesThought` (optional) - Which step being reconsidered
- `branchFromThought` (optional) - Branching for alternative approach
- `branchId` (optional) - Alternative implementation ID

---

## Planning Flow

1. **Architecture**: High-level design considerations
2. **Components**: Break into modular components
3. **Interfaces**: Plan function signatures and APIs
4. **Error Handling**: Consider edge cases
5. **Documentation**: Draft comprehensive comments
6. **Testability**: Ensure code can be tested
7. **Quality**: Apply SOLID and clean code principles
8. **Finalize**: Only complete when planning is thorough

---

## Best Practices

- Document WHY, not WHAT (max 2 lines per comment)
- Follow SOLID principles
- Prioritize readability over cleverness
- Plan for testability from start
- Break complex functionality into smaller modules
- Consider error handling and edge cases
- Only set `nextThoughtNeeded: false` when complete

---

## Related

- [Sequential Thinking](sequential-thinking.md) - For general problem-solving
- [Vibe Check](vibe-check.md) - Validate design decisions
- [Workflows](../workflows.md#feature-development-flow) - Integration in workflows
