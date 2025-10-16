# Pieces

**Category**: Knowledge Management | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Long-term memory and contextual knowledge capture for projects and breakthroughs.

---

## Capabilities

- `ask_pieces_ltm` - Query historical/contextual information from environment
- `create_pieces_memory` - Create detailed "smart checkpoints" with full context
- Associate files, folders, and external links
- Track workstream summaries
- Capture project breakthroughs and solutions

---

## When to Use

**Capture (create_pieces_memory)**:
- Architectural decisions made
- Complex problems solved
- Implementation patterns discovered
- Security issues and remediations
- Performance optimizations
- Integration patterns
- Major breakthroughs or pivots

**Query (ask_pieces_ltm)**:
- Before starting new work (check for similar solutions)
- When making architectural decisions (learn from past)
- While debugging (find similar past issues)
- Before writing documentation (reuse patterns)

---

## Key Functions

### ask_pieces_ltm

**Purpose**: Retrieve historical/contextual information

**Parameters**:
- `question` (required) - Direct question for Pieces LTM
- `chat_llm` (required) - LLM being used (e.g., "gpt-4o-mini", "claude-sonnet-4")
- `connected_client` (optional) - Client name (Cursor, Claude, etc.)
- `open_files` (optional) - Array of currently open file paths
- `topics` (optional) - Array of topical keywords
- `related_questions` (optional) - Array of supplemental questions
- `application_sources` (optional) - Specific app sources (Chrome, Terminal, etc.)

**Example**:
```
question: "How did we implement authentication in previous projects?"
chat_llm: "claude-sonnet-4"
topics: ["authentication", "JWT", "security"]
Returns: Previous auth implementations and lessons learned
```

### create_pieces_memory

**Purpose**: Create detailed memory/checkpoint

**Parameters**:
- `summary_description` (required) - Concise title (1-2 sentences)
- `summary` (required) - Detailed markdown narrative
- `connected_client` (optional) - Client name
- `files` (optional) - Array of absolute file/folder paths
- `project` (optional) - Absolute path to project root
- `externalLinks` (optional) - Array of GitHub/docs/article URLs

**What to Include in Summary**:
- Background and context
- Problem and solution
- Thought process
- What worked and what didn't
- Why decisions were made
- Code snippets, errors, logs
- Any relevant references

**Example**:
```
summary_description: "Fixed N+1 query bug in user dashboard"
summary: "## Background\n The dashboard was loading slowly...\n\n## Problem\n...\n\n## Solution\n..."
files: ["/path/to/user_controller.py", "/path/to/user_model.py"]
project: "/path/to/project"
externalLinks: ["https://github.com/org/repo/pr/123"]
```

---

## Best Practices

**When Creating Memories**:
- Provide absolute file paths (required for verification)
- Include comprehensive markdown narrative
- Document WHY, not just WHAT
- Add external links (GitHub, docs, articles)
- Capture both successes and failures

**When Querying**:
- Be specific in questions
- Provide context (topics, related questions)
- Include currently open files
- Check before starting similar work

---

## Integration with Workflows

**Feature Development**: Document at completion
**Bug Fixes**: Save solution for future reference
**Architectural Decisions**: Create memory with ADR
**Research Spikes**: Document findings before closing

---

## Related

- [Vibe Check](../thinking/vibe-check.md) - For pattern learning
- [Workflows](../workflows.md#knowledge-capture) - Integration patterns
