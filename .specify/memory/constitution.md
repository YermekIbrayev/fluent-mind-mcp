<!--
# Migration Notice

This constitution has been migrated from a monolithic structure (553 lines) to a modular v4.0.0 architecture.

**Old Structure**: Single file with all principles, workflows, and governance
**New Structure**: Modular files organized by topic for 70-90% token reduction

**Version Change**: Monolithic → 1.0.0 (Modular)
**Migration Date**: 2025-10-16
-->

# Fluent Mind MCP Constitution

**Version**: 1.0.0 | **Ratified**: 2025-10-16 | **Architecture**: Modular v4.0.0

**📖 Main Entry Point**: [INDEX.md](INDEX.md) - Start here for navigation

---

## Quick Links

### For Immediate Reference

**TDD Requirements**: [Principle II](principles/02-tdd.md) - TDD is NON-NEGOTIABLE for Production Code

**Quality Gates**: [Principle V](principles/05-quality-gates.md) - All gates must pass before commit

**Standard Workflow**: [Standard Feature Flow](workflows/standard-feature.md) - 4-phase development process

**Planning Levels**: [Principle IV](principles/04-planning.md) - Trivial → Simple → Moderate → Complex

**MCP Servers**: [Principle I](principles/01-mcp-first.md) - When and how to use MCP servers

---

## Core Principles Summary

1. **[MCP-First Architecture](principles/01-mcp-first.md)** - Leverage MCP servers for accuracy, auditability, and learning
2. **[Test-First Development](principles/02-tdd.md)** (NON-NEGOTIABLE) - RED-GREEN-REFACTOR cycle required for Production Code
3. **[Specification-Driven Development](principles/03-spec-driven.md)** - Specs required before implementation
4. **[Comprehensive Planning](principles/04-planning.md)** - Planning scales with complexity
5. **[Security and Quality Gates](principles/05-quality-gates.md)** - All gates must pass for Production Code
6. **[Knowledge Management](principles/06-knowledge.md)** - Capture and reuse knowledge systematically
7. **[Documentation Excellence](principles/07-documentation.md)** - Documentation is code, must be maintained
8. **[Token-Efficient Architecture](principles/08-architecture.md)** - Vertical slices, file limits, clear boundaries

---

## Complete Navigation

**🗺️ [INDEX.md](INDEX.md)** - Complete navigation hub with:
- Quick navigation by question
- Navigation by role (Solo/Small/Large team)
- Navigation by development phase
- Navigation by work type (Production/Infrastructure/Experimental)
- Complete module list

---

## Why Modular Structure?

**Token Efficiency**:
- Typical query: 70-90% token reduction
- Load only relevant modules instead of entire constitution
- Example: "What are TDD requirements?" = ~500 tokens vs 4,000+ tokens

**Maintainability**:
- Each principle in separate file
- Easier to update and version
- Clear separation of concerns
- Better organization

**AI-Friendly**:
- Load INDEX.md first (~300 tokens)
- Navigate to specific module (~100-400 tokens)
- Total context: ~300-700 tokens vs 4,000+ tokens

---

## Module Organization

```
.specify/memory/
├── INDEX.md                    # Main navigation hub (START HERE)
├── constitution.md            # This file (lightweight entry point)
│
├── principles/                # Core 8 principles (modular)
│   ├── 01-mcp-first.md
│   ├── 02-tdd.md             # NON-NEGOTIABLE
│   ├── 03-spec-driven.md
│   ├── 04-planning.md
│   ├── 05-quality-gates.md
│   ├── 06-knowledge.md
│   ├── 07-documentation.md
│   └── 08-architecture.md
│
├── workflows/                 # Development workflows
│   ├── standard-feature.md   # 4-phase workflow
│   ├── quick-fix.md          # For trivial tasks
│   └── research.md           # Investigation flow
│
├── governance.md              # Enforcement and amendments
├── team-adaptations.md        # Solo/Small/Large team
├── cicd.md                    # Automation and checks
└── glossary.md                # Term definitions
```

---

## Getting Started

### For First-Time Readers
1. Read [INDEX.md](INDEX.md) for complete overview
2. Review your role section: [Team Adaptations](team-adaptations.md)
3. Understand [TDD Requirements](principles/02-tdd.md) (NON-NEGOTIABLE)
4. Learn [Standard Workflow](workflows/standard-feature.md)

### For Quick Reference
1. Open [INDEX.md](INDEX.md)
2. Use "Quick Navigation by Question"
3. Load only the relevant module

### For AI Assistants
1. Always load [INDEX.md](INDEX.md) first
2. Navigate to specific module based on user query
3. Load only relevant content (70-90% token reduction)

---

## Key Requirements at a Glance

### Production Code
- ✅ TDD Required (RED-GREEN-REFACTOR)
- ✅ All Quality Gates Must Pass
- ✅ Test Coverage ≥80% (100% Critical Path)
- ✅ Specification Required
- ✅ Documentation Per Decision Tree

### Infrastructure Code
- ⚠️ Tests Recommended
- ✅ Semgrep High/Critical Only
- ✅ Valid Links

### Experimental Code
- ℹ️ No Gates During Exploration
- ✅ Document Learnings to Pieces MCP
- ❌ Cannot Merge Without Meeting Production Standards

---

## Governance

**Enforcement**: [Governance](governance.md)
- Vibe-Check MCP constitution storage
- Quality gates in CI/CD
- PR review checklist
- Automated checks

**Amendments**: [Amendment Process](governance.md#amendment-process)
- Proposal → Validation → Approval → Implementation → Verification
- Team size determines approval process

**Evolution**: Quarterly reviews + after major milestones

---

**Version**: 1.0.0 | **Ratified**: 2025-10-16 | **Last Amended**: 2025-10-16

**Next Review**: 2026-01-16

**Amendment Proposals**: `.specify/memory/amendments/`

**📖 Full Navigation**: [INDEX.md](INDEX.md)
