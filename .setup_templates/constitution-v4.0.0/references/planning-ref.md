# Planning Quick Reference

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > References

**Full Details**: [Principle IV: Comprehensive Planning](../principles/04-planning.md)

---

## Planning Levels (by Complexity)

### Trivial (1-2 steps, <15 min)
- **Planning**: None required
- **Documentation**: Inline TODO comments OK
- **Examples**: Fix typo, update config value

### Simple (3-5 steps, 15-60 min)
- **Planning**: Single file `.plans/NNNN_task.md`
- **Contents**: Goal, steps list, MCP servers, success criteria
- **Examples**: Add logging, update dependency

### Moderate (6-10 steps, 1-4 hours)
- **Planning**: Two documents
  - `01_initial_plan.md` - First understanding
  - `02_revised_plan.md` - Detailed breakdown with MCP mapping
- **Examples**: Refactor module, add feature with tests

### Complex (11+ steps, >4 hours)
- **Planning**: Four documents
  - `01_initial_plan.md` - Initial understanding
  - `02_revised_plan.md` - Detailed step-by-step
  - `03_mcp_usage_plan.md` - MCP integration strategy
  - `04_execution_log.md` - Actual execution + learnings
- **Examples**: New feature with specs, major refactoring

---

## What Counts as a "Step"?

A [step](../glossary.md#step) is:
- Single tool invocation (Read, Write, Bash, Git)
- Produces measurable output/state change
- Can be verified as complete/incomplete
- Execution time: <5 minutes

**Examples of 1 step each:**
- Read a file
- Run tests
- Update spec
- Make architectural decision

---

## Planning Decision Tree

```
Task complexity?
├─ 1-2 steps, <15 min → Trivial (no plan)
├─ 3-5 steps, 15-60 min → Simple (1 file)
├─ 6-10 steps, 1-4 hr → Moderate (2 files)
└─ 11+ steps, >4 hr → Complex (4 files)
```

---

## Benefits of .plans/ System

- **Audit Trail**: Complete decision history
- **Continuous Improvement**: Analyze past executions
- **Knowledge Transfer**: New team members understand context
- **Debugging Aid**: Track down why decisions were made
- **Time Estimation**: Improve estimates from historical data

---

**See Also**:
- [Principle IV: Comprehensive Planning](../principles/04-planning.md) - Full planning workflow
- [Glossary: Step](../glossary.md#step) - Definition
- [Glossary: Trivial Task](../glossary.md#trivial-task) - When no planning needed
