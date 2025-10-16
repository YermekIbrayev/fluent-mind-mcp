# Constitution Index - AI Navigation Hub

**Version**: 4.0.0 | **Last Updated**: 2025-10-16

This index helps you quickly find the right constitution module for your question.

---

## Quick Navigation by Question

**"What are the TDD requirements?"**
→ [Principle II: Test-First Development](principles/02-tdd.md) or [TDD Quick Reference](references/tdd-quick-ref.md)

**"How do I plan a task?"**
→ [Principle IV: Comprehensive Planning](principles/04-planning.md) or [Planning Quick Reference](references/planning-ref.md)

**"What quality gates apply to my code?"**
→ [Principle V: Security and Quality Gates](principles/05-quality-gates.md) or [Quality Gates Reference](references/quality-gates-ref.md)

**"What does '[term]' mean?"**
→ [Glossary](glossary.md) (definitions for Critical Path, Step, Architectural Decision, etc.)

**"What's the standard development workflow?"**
→ [Standard Feature Workflow](workflows/standard-feature.md)

**"How do I use MCP servers?"**
→ [Principle I: MCP-First Architecture](principles/01-mcp-first.md) or [MCP Servers Reference](references/mcp-servers-ref.md)

**"When do I need a specification?"**
→ [Principle III: Specification-Driven Development](principles/03-spec-driven.md)

**"What documentation is required?"**
→ [Principle VII: Documentation Excellence](principles/07-documentation.md)

**"How do I capture knowledge?"**
→ [Principle VI: Knowledge Management](principles/06-knowledge.md)

**"What are the CI/CD requirements?"**
→ [CI/CD and Automation](cicd.md) or [Token Metrics](cicd.md#token-metrics-track-weekly)

**"How do I amend the constitution?"**
→ [Governance: Amendment Process](governance.md#amendment-process)

**"How do I optimize code for AI/token efficiency?"**
→ [Principle VIII: Token-Efficient Architecture](principles/08-architecture.md) or [Token Optimization Quick Ref](quick-refs/token-optimization.md)

**"What are the file size limits?"**
→ [File Size Limits Quick Ref](quick-refs/file-limits.md) or [Architecture Principle](principles/08-architecture.md#file-size-limits)

**"How should I structure code for AI comprehension?"**
→ [Architecture Quick Ref](quick-refs/architecture.md) or [Naming Conventions Quick Ref](quick-refs/naming.md)

---

## Navigation by Role

**Solo Developer:**
- Start: [Team Adaptations: Solo](team-adaptations.md#solo-developer)
- TDD: [Principle II](principles/02-tdd.md) (self-review with Vibe-Check MCP)
- Planning: [Principle IV](principles/04-planning.md) (simplified for simple tasks)

**Small Team (2-5 people):**
- Start: [Team Adaptations: Small](team-adaptations.md#small-team-2-5-people)
- Review: [CI/CD: Code Review](cicd.md#code-review-process) (1 approver minimum)
- Collaboration: [Governance](governance.md)

**Large Team (6+ people):**
- Start: [Team Adaptations: Large](team-adaptations.md#mediumlarge-team-6-people)
- Review: [CI/CD: Code Review](cicd.md#code-review-process) (2+ approvers)
- Process: [Governance](governance.md) (formal enforcement)

---

## Navigation by Development Phase

**Phase 1: Planning & Specification**
1. [Principle III: Specification-Driven](principles/03-spec-driven.md) - Create specs
2. [Principle IV: Comprehensive Planning](principles/04-planning.md) - Plan based on complexity
3. [Context Budget Planning](principles/04-planning.md#context-budget-planning) - Optimize AI context
4. Use Vibe-Check MCP to validate approach

**Phase 2: Implementation & Testing**
1. [Principle II: Test-First Development](principles/02-tdd.md) - TDD cycle
2. [Standard Feature Workflow: Phase 2](workflows/standard-feature.md#phase-2-implementation--testing)

**Phase 3: Validation & Documentation**
1. [Principle V: Security and Quality Gates](principles/05-quality-gates.md) - Run gates
2. [Principle VII: Documentation](principles/07-documentation.md) - Update docs
3. [Principle VI: Knowledge Management](principles/06-knowledge.md) - Capture learnings

**Phase 4: Review & Completion**
1. [CI/CD: Code Review Process](cicd.md#code-review-process)
2. [Standard Feature Workflow: Phase 4](workflows/standard-feature.md#phase-4-review--completion)

---

## Navigation by Work Type

**Production Code:**
- Quality Gates: [ALL gates required](principles/05-quality-gates.md#production-code-all-gates-required)
- TDD: [Required (no exceptions)](principles/02-tdd.md)
- Documentation: [Required per decision tree](principles/07-documentation.md)

**Infrastructure Code:**
- Quality Gates: [Relaxed gates](principles/05-quality-gates.md#infrastructure-code-relaxed-gates)
- TDD: [Tests recommended](principles/02-tdd.md#work-type-requirements)
- Documentation: [Links must be valid](principles/07-documentation.md)

**Experimental Code:**
- Quality Gates: [Minimal gates](principles/05-quality-gates.md#experimental-code-minimal-gates)
- TDD: [Optional](principles/02-tdd.md#work-type-requirements)
- Documentation: [Must document learnings](principles/06-knowledge.md)

---

## Complete Module List

### Core Principles
1. [Principle I: MCP-First Architecture](principles/01-mcp-first.md)
2. [Principle II: Test-First Development (NON-NEGOTIABLE)](principles/02-tdd.md)
3. [Principle III: Specification-Driven Development](principles/03-spec-driven.md)
4. [Principle IV: Comprehensive Planning](principles/04-planning.md)
5. [Principle V: Security and Quality Gates](principles/05-quality-gates.md)
6. [Principle VI: Knowledge Management and Learning](principles/06-knowledge.md)
7. [Principle VII: Documentation Excellence](principles/07-documentation.md)
8. [Principle VIII: Token-Efficient Architecture](principles/08-architecture.md)

### Workflows
- [Standard Feature Implementation](workflows/standard-feature.md)
- [Quick Fix Flow](workflows/quick-fix.md)
- [Research/Investigation Flow](workflows/research.md)

### References
- [Glossary - Term Definitions](glossary.md)
- [TDD Quick Reference](references/tdd-quick-ref.md)
- [Quality Gates Quick Reference](references/quality-gates-ref.md)
- [Planning Quick Reference](references/planning-ref.md)
- [MCP Servers Reference](references/mcp-servers-ref.md)

### Token Optimization Quick References
- [File Size Limits](quick-refs/file-limits.md)
- [Architecture Patterns](quick-refs/architecture.md)
- [Token Optimization Techniques](quick-refs/token-optimization.md)
- [AI-Friendly Naming Conventions](quick-refs/naming.md)

### Governance & Operations
- [Team Size Adaptations](team-adaptations.md)
- [CI/CD and Automation](cicd.md)
- [Enforcement and Governance](governance.md)

### Visual Aids
- [TDD Cycle Diagram](diagrams/tdd-cycle.mermaid)
- [Expert Review Cycle Diagram](diagrams/expert-review-cycle.mermaid)
- [Documentation Decision Tree](diagrams/documentation-tree.mermaid)
- [Standard Workflow Diagram](diagrams/standard-workflow.mermaid)
- [Quality Gates Flow Diagram](diagrams/quality-gates-flow.mermaid)

---

## How to Use This Index

**For AI Assistants:**
1. User asks a question
2. Load this INDEX.md first (~400 tokens)
3. Find matching question/topic above
4. Load only the linked module (~200-600 tokens)
5. Total: ~600-1,000 tokens vs 4,400 tokens for full constitution

**For Humans:**
1. Use "Quick Navigation by Question" for specific queries
2. Use "Navigation by Role" to find your starting point
3. Use "Navigation by Phase" during development
4. Use "Complete Module List" to browse all modules

**Token Efficiency:**
- Typical query: 70-88% token reduction
- Example: "What are TDD requirements?" loads INDEX + TDD module = 600 tokens vs 4,400 tokens

---

**Backward Compatibility**: See [../constitution.md](../constitution.md) for compressed 70-line version or [../CONSTITUTION-FULL.md](../CONSTITUTION-FULL.md) for full version.
