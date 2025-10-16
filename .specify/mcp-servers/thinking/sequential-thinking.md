# Sequential Thinking

**Category**: Thinking & Planning | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Dynamic problem-solving through flexible, structured thoughts with revision support.

---

## Capabilities

- Break down complex problems into steps
- Support for revision and course correction
- Branch into alternative approaches
- Hypothesis generation and verification
- Iterative refinement until solution found
- Adjustable thought count during process

---

## When to Use

- Complex multi-step problems
- Planning with room for revision
- Problems where scope isn't initially clear
- Tasks needing context over multiple steps
- Situations requiring filtering irrelevant information
- Analysis that might need course correction

---

## Key Parameters

- `thought` (required) - Current thinking step
- `thoughtNumber` (required) - Current step number
- `totalThoughts` (required) - Estimated total (adjustable)
- `nextThoughtNeeded` (required) - Boolean, whether more thinking needed
- `isRevision` (optional) - Boolean, revising previous thought
- `revisesThought` (optional) - Which thought number being reconsidered
- `branchFromThought` (optional) - Branching point thought number
- `branchId` (optional) - Branch identifier
- `needsMoreThoughts` (optional) - Boolean, need to extend thinking

---

## How It Works

**1. Start with estimate**: Begin with initial thought count estimate

**2. Think flexibly**:
- Question previous thoughts
- Revise decisions as understanding deepens
- Branch into alternative approaches
- Express uncertainty

**3. Adjust dynamically**:
- Increase total thoughts if needed
- Decrease if problem simpler than expected

**4. Iterate until done**:
- Generate solution hypothesis
- Verify based on chain of thought
- Repeat until satisfied
- Set `nextThoughtNeeded: false` when complete

---

## Example Flow

```
Thought 1/5: Analyze the problem scope
Thought 2/5: Realize more complexity, adjust to 1/8
Thought 3/8: Propose solution A
Thought 4/8: Question assumption in thought 3 (revision)
Thought 5/8: Branch to explore solution B
Thought 6/8: Compare solutions
Thought 7/8: Select best approach
Thought 8/8: Final verification, done
```

---

## Best Practices

- Start with reasonable estimate, adjust as needed
- Don't hesitate to revise previous thoughts
- Mark revisions with `isRevision: true`
- Use branching for alternative explorations
- Filter irrelevant information at each step
- Only set `nextThoughtNeeded: false` when truly satisfied

---

## Related

- [Clean Code](clean-code.md) - For code-specific planning
- [Vibe Check](vibe-check.md) - For assumption validation
- [Workflows](../workflows.md#feature-development-flow) - Integration in workflows
