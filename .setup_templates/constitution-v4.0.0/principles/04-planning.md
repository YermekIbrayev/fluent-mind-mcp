# Principle IV: Comprehensive Planning

**Version**: 4.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [Planning Quick Reference](../references/planning-ref.md), [Spec-Driven Development](03-spec-driven.md)

**Prerequisites**: Understand [Step](../glossary.md#step) and [Trivial Task](../glossary.md#trivial-task) definitions

---

## Guideline

Planning requirements scale with task complexity.

---

## Graduated Planning Levels

### Trivial (1-2 steps, <15 min)

**Planning**: None required
**Documentation**: Inline TODO comments acceptable
**Examples**:
- Fix typo in documentation
- Update config value
- Add single log statement
- Rename variable for clarity

**When to Use**: All criteria in [Trivial Task](../glossary.md#trivial-task) met

---

### Simple (3-5 steps, 15-60 min)

**Planning**: Single file `.plans/NNNN_task.md`

**Contents**:
- Goal and approach (1-2 paragraphs)
- Steps (numbered list)
- MCP servers to use
- Success criteria

**Examples**:
- Add logging to module
- Update dependency
- Fix straightforward bug
- Add simple validation

**Template**:
```markdown
# Task NNNN: [Task Name]

## Goal
[What are we trying to achieve?]

## Approach
[How will we do it?]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## MCP Servers
- [Server 1]: [Usage]
- [Server 2]: [Usage]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

---

### Moderate (6-10 steps, 1-4 hours)

**Planning**: Two documents

**01_initial_plan.md**:
- First understanding of task
- High-level approach
- Initial step breakdown
- Known challenges

**02_revised_plan.md**:
- Detailed step-by-step breakdown
- MCP server mapping
- Dependencies identified
- Risk mitigation strategies
- Success criteria refined

**Examples**:
- Refactor module for testability
- Add feature with tests
- Implement API endpoint
- Database schema migration

---

### Complex (11+ steps, >4 hours)

**Planning**: Four documents

**01_initial_plan.md**:
- Initial understanding
- High-level approach
- Expected challenges
- Time estimate

**02_revised_plan.md**:
- Detailed step-by-step breakdown
- Dependencies and prerequisites
- Risk mitigation strategies
- Success criteria
- Verification checkpoints

**03_mcp_usage_plan.md**:
- Which MCP servers for which steps
- Expected inputs and outputs
- Integration points
- Fallback strategies
- Optimization opportunities

**04_execution_log.md**:
- Actual execution details
- MCP inputs and outputs
- Issues encountered and resolutions
- Expected vs actual outcomes
- Time analysis
- Lessons learned (save to Pieces MCP)

**Examples**:
- New feature with specification
- Major refactoring
- Multi-component integration
- Performance optimization

---

## What Counts as a "Step"?

See [Glossary: Step](../glossary.md#step) for full definition.

**Quick Check** - A step is:
- Single tool invocation
- Produces measurable output
- Can be verified complete/incomplete
- Execution time: <5 minutes

**Examples**:
- Read file = 1 step
- Run tests = 1 step
- Update spec = 1 step
- Make architectural decision = 1 step

---

## Planning Decision Tree

```
Estimate steps and time:
├─ 1-2 steps, <15 min → Trivial (no plan)
├─ 3-5 steps, 15-60 min → Simple (1 file)
├─ 6-10 steps, 1-4 hr → Moderate (2 files)
└─ 11+ steps, >4 hr → Complex (4 files)
```

**If uncertain**: Start with Simple plan, upgrade to Moderate/Complex if needed.

---

## Benefits of .plans/ System

### Audit Trail
- Complete history of decision-making
- Understand why choices were made
- Track evolution of understanding

### Continuous Improvement
- Analyze past executions
- Identify patterns and bottlenecks
- Optimize future work

### Knowledge Transfer
- New team members understand context
- Decisions explained with rationale
- Onboarding accelerated

### Debugging Aid
- Track down when/why decisions made
- Reproduce issue context
- Verify assumptions

### Time Estimation
- Improve estimates from historical data
- Calibrate planning accuracy
- Identify underestimated areas

---

## Planning Anti-Patterns

❌ **Over-planning trivial tasks** - Creates overhead
❌ **Under-planning complex tasks** - Leads to confusion
❌ **Not updating plans** - Plans become stale
❌ **Skipping execution logs** - Lose learning value
❌ **No retrospective analysis** - Miss improvement opportunities

---

## Planning Quality Checklist

Before starting implementation, verify:

**Simple Plan** (1 file):
- [ ] Goal clearly stated
- [ ] Steps numbered and specific
- [ ] MCP servers identified
- [ ] Success criteria defined

**Moderate Plan** (2 files):
- [ ] Initial understanding captured
- [ ] Revised plan has detailed steps
- [ ] Dependencies mapped
- [ ] MCP usage clear

**Complex Plan** (4 files):
- [ ] All Moderate criteria met
- [ ] Dedicated MCP usage plan exists
- [ ] Execution log template ready
- [ ] Checkpoints for verification defined

---

## Context Budget Planning

For AI-assisted development, manage context window efficiently by planning what information the AI needs at each stage.

### Context Categories

#### Must-Have Context (20% of window)
Essential information for the current task:
- Files being modified
- Direct dependencies
- Interfaces being implemented
- Tests for current code
- Specifications being followed

#### Should-Have Context (30% of window)
Supporting information that improves quality:
- Related modules in same feature
- Parent classes/abstractions
- Configuration files
- Similar implementations for reference
- Recent execution logs

#### Optional Context (50% reserve)
Nice-to-have for comprehensive understanding:
- Documentation
- Historical decisions (ADRs)
- Similar features in codebase
- External API documentation
- Performance benchmarks

### Planning Context Usage

In your planning documents, explicitly specify context needs:

```markdown
## Context Budget Plan

### Must-Have (20%)
- user/validators.py (current file)
- user/models.py (data structures)
- tests/test_validators.py (test cases)

### Should-Have (30%)
- user/service.py (usage context)
- user/controller.py (API layer)
- config/validation.yaml (rules)

### Reserve (50%)
- Keep for AI's working memory
- Dynamic loading as needed
```

### Context Loading Strategy

1. **Start Minimal**: Load only must-have context
2. **Add Progressively**: Load should-have as needed
3. **Reserve Space**: Keep 50% for AI operations
4. **Unload Aggressively**: Remove context when done

### Context Optimization Tips

**DO:**
- Use vertical slices to reduce cross-file needs
- Load test files with implementation files
- Prioritize interfaces over implementations
- Use summaries for large files

**DON'T:**
- Load entire directories
- Include generated code
- Load all tests for one file change
- Keep historical versions in context

### Measuring Context Efficiency

Track these metrics:
```python
# In execution logs
context_metrics = {
    "files_loaded": 12,
    "total_tokens": 45000,
    "must_have_tokens": 9000,    # Should be ~20%
    "should_have_tokens": 13500,  # Should be ~30%
    "reserve_used": 22500,        # Should be ~50%
    "task_completed": True,
    "context_reloads": 2          # Minimize this
}
```

### Context Budget Templates

Add to planning templates:

**Simple Plan Addition**:
```markdown
## Context Budget
- Must: [list files]
- Should: [list files]
- Reserve: 50%
```

**Moderate/Complex Plan Addition**:
```markdown
## Context Budget Planning

### Initial Load
Must-Have:
- file1.py (why needed)
- file2.py (why needed)

### Progressive Load
Step 3: Add file3.py
Step 5: Replace file1.py with file4.py
Step 8: Clear all except tests
```

---

**See Also**:
- [Planning Quick Reference](../references/planning-ref.md) - Quick lookup
- [Glossary: Step](../glossary.md#step) - What counts as a step
- [Glossary: Trivial Task](../glossary.md#trivial-task) - When no planning needed
- [Principle III: Spec-Driven](03-spec-driven.md) - Specs before planning
