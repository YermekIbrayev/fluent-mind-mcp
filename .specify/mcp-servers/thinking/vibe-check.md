# Vibe Check

**Category**: Thinking & Planning | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Metacognitive questioning to identify assumptions and break tunnel vision, preventing cascading errors.

---

## Capabilities

- `vibe_check` - Validate compliance and catch assumptions
- `vibe_learn` - Track common errors and solutions
- `update_constitution` - Add session constitutional rules
- `reset_constitution` - Overwrite session constitutional rules
- `check_constitution` - View current session rules

---

## When to Use

- Before starting complex tasks
- To catch hidden assumptions
- When approaching new problems
- To prevent cascading errors
- After making mistakes (learn patterns)
- Validating adherence to constitution/principles

---

## Key Functions

### vibe_check

**Purpose**: Validate approach and identify hidden assumptions

**Parameters**:
- `goal` (required) - Current goal
- `plan` (required) - Detailed plan
- `progress` (optional) - Progress so far
- `uncertainties` (optional) - Array of uncertainties
- `taskContext` (optional) - Context of current task
- `userPrompt` (optional) - Original user prompt
- `sessionId` (optional) - Session ID for state management

**Returns**: Questions and insights to prevent tunnel vision

**Example**:
```
goal: "Implement authentication system"
plan: "1. Add JWT tokens 2. Create login endpoint 3. Secure routes"
Returns: "Have you considered refresh token rotation? What about rate limiting?"
```

### vibe_learn

**Purpose**: Record mistakes and solutions for pattern recognition

**Parameters**:
- `mistake` (required) - One-sentence description
- `category` (required) - Pattern category
- `solution` (optional) - How it was corrected
- `type` (optional) - "mistake", "preference", or "success"
- `sessionId` (optional) - Session ID

**Categories**:
- Complex Solution Bias
- Feature Creep
- Premature Implementation
- Misalignment
- Overtooling
- Preference
- Success
- Other

**Example**:
```
mistake: "Started coding before writing tests"
category: "Premature Implementation"
solution: "Paused, wrote tests first, then implemented"
```

### Constitution Management

**update_constitution**: Add rule to session
**reset_constitution**: Overwrite all rules for session
**check_constitution**: View current session rules

---

## Usage Pattern

**Before Work**:
```
1. vibe_check with goal and plan
2. Review questions and adjust plan
3. Proceed with confidence
```

**After Mistakes**:
```
1. vibe_learn with mistake details
2. Track patterns over time
3. Avoid repeating same mistakes
```

**During Work**:
```
1. check_constitution for current rules
2. vibe_check if feeling uncertain
3. Course-correct as needed
```

---

## Related

- [Sequential Thinking](sequential-thinking.md) - For problem decomposition
- [Clean Code](clean-code.md) - For code design validation
- [Workflows](../workflows.md) - Integration in all workflows
