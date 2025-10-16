# Enforcement and Governance

**Version**: 1.0.0 | **Part of**: [Constitution](INDEX.md)

**Related**: [CI/CD](cicd.md), [Team Adaptations](team-adaptations.md)

---

## Principle

The constitution supersedes all other practices.

---

## Enforcement Mechanisms

### 1. Vibe-Check MCP Constitution Storage

**Tools**:
- `reset_constitution` - Update with latest principles
- `check_constitution` - View current principles
- `vibe_check` - Validate compliance during work

### 2. Quality Gates

**See**: [Principle V: Quality Gates](principles/05-quality-gates.md)

- Gates enforced via CI/CD pipeline
- Local pre-commit hooks catch issues early
- Failed gates block PR merge

### 3. PR Review Checklist

**See**: [CI/CD: Code Review Process](cicd.md#code-review-process)

- [ ] Code follows constitution principles
- [ ] Tests exist and pass (TDD for Production Code)
- [ ] No security vulnerabilities (Semgrep clean)
- [ ] Documentation updated
- [ ] Constitution compliance verified

### 4. Automated Checks

**Pre-commit Hooks**:
- Semgrep MCP security scan
- Linting and type checking
- Format checking

**CI/CD Pipeline**:
- Full test suite
- Coverage check (≥80% Production)
- Security diagnostics
- Documentation link validation
- Dependabot for security updates

**See**: [CI/CD and Automation](cicd.md)

---

## Amendment Process

### 1. Proposal

Create amendment document: `.specify/memory/amendments/NNNN_amendment_name.md`

Include:
- Current problem or limitation
- Proposed change
- Impact analysis
- Migration plan

### 2. Validation

- Use **Vibe-Check MCP** to validate proposal
- Check for unintended consequences
- Identify affected principles
- Ensure alignment with core values

### 3. Documentation

- Impact on existing workflows
- Changes to tooling/automation
- Training materials updates
- Migration timeline

### 4. Approval

**Solo Developer**:
- Self-approval with Vibe-Check MCP validation

**Small Team (2-5)**:
- Consensus required (all agree)

**Large Team (6+)**:
- 2/3 majority vote
- Architecture lead approval

**See**: [Team Adaptations](team-adaptations.md)

### 5. Implementation

- Update constitution files
- Update version number (semantic versioning)
- Update tooling/automation
- Announce to team

### 6. Verification

Monitor for 30 days:
- Check for compliance issues
- Gather feedback
- Document lessons learned
- Adjust if needed

---

## Constitution Violations

### Severity Classification

| Severity | Definition | Action |
|----------|-----------|--------|
| **Critical** | Security vulnerability, data integrity risk | Immediate rollback, fix before any other work |
| **High** | TDD skipped, quality gates bypassed | Block merge, require correction |
| **Medium** | Documentation missing, incomplete planning | Address before next sprint |
| **Low** | Minor process deviation | Document, discuss in retrospective |

### Handling Violations

**First Time**:
1. **Educate** - Explain which principle was violated
2. **Document** - Record in Pieces MCP
3. **Correct** - Fix before merge

**Repeated Violations**:
1. Identify root cause (tooling, clarity, intentional)
2. Address systematically
3. Update constitution or tooling

**Pattern Identified**:
1. Analyze pattern
2. Update constitution or tooling
3. Share learnings
4. Track effectiveness (30 days)

---

## Constitution Evolution

### Regular Reviews

**Cadence**:
- **Quarterly** reviews (standard)
- **After major milestones** (releases, large features)
- **Ad-hoc** when issues identified

### Feedback Sources

1. **Execution Logs**: `.plans/` directory analysis
2. **Vibe-Check MCP Learnings**: `vibe_learn` history
3. **Team Retrospectives**: Gather feedback
4. **Industry Research**: Exa AI MCP, Context7 MCP
5. **Community Feedback**: GitHub issues (if open source)

### Evolution Process

1. Identify issues
2. Research solutions (use MCPs)
3. Propose amendments
4. Validate with Vibe-Check MCP
5. Execute amendment process
6. Monitor results (30 days)

---

**Version**: 1.0.0 | **Ratified**: 2025-10-16 | **Last Amended**: 2025-10-16

**Next Review**: 2026-01-16

**Amendment Proposals**: `.specify/memory/amendments/`

---

**See Also**:
- [Principle V: Quality Gates](principles/05-quality-gates.md)
- [CI/CD](cicd.md)
- [Team Adaptations](team-adaptations.md)
- [Principle I: MCP-First](principles/01-mcp-first.md)
