# Enforcement and Governance

**Version**: 3.0.0 | **Part of**: [Constitution](INDEX.md)

**Related**: [CI/CD: Code Review](cicd.md#code-review-process), [Team Adaptations](team-adaptations.md)

---

## Principle

The constitution supersedes all other practices.

---

## Enforcement Mechanisms

### 1. Vibe-Check MCP Constitution Storage

Store and validate constitution principles during work.

**Tools**:
- `reset_constitution` - Update with latest principles
- `check_constitution` - View current principles
- `vibe_check` - Validate compliance during work

**Usage**:
```bash
# Before starting work
vibe_check(goal="Implement X", plan="...")

# To check current rules
check_constitution(sessionId="...")
```

### 2. Quality Gates (Applied by Work Type)

**See**: [Principle V: Quality Gates](principles/05-quality-gates.md) for complete gate requirements.

**Gate Enforcement**:
- Gates enforced via CI/CD pipeline
- Local pre-commit hooks catch issues early
- Failed gates block PR merge

### 3. PR Review Checklist

**See**: [CI/CD: Code Review Process](cicd.md#code-review-process) for complete checklist.

**Key Checks**:
- [ ] Code follows constitution principles
- [ ] Tests exist and pass (TDD for Production Code)
- [ ] No security vulnerabilities (Semgrep clean)
- [ ] Documentation updated
- [ ] Constitution compliance verified (correct work type, gates passed)

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

**See**: [CI/CD and Automation](cicd.md) for complete pipeline details.

---

## Amendment Process

To amend this constitution:

### 1. Proposal

Create amendment document:
```bash
.specify/memory/amendments/NNNN_amendment_name.md
```

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

Create full documentation:
- Impact on existing workflows
- Changes to tooling/automation
- Training materials updates
- Migration timeline

### 4. Approval

**Team size determines approval process**:

**Solo Developer:**
- Self-approval with Vibe-Check MCP validation
- Document rationale thoroughly
- Update constitution immediately

**Small Team (2-5):**
- Consensus required (all team members agree)
- Discuss in team sync
- Document decision

**Large Team (6+):**
- Formal proposal review
- 2/3 majority vote
- Architecture lead approval
- Announcement to all team members

**See**: [Team Adaptations](team-adaptations.md) for team-size specific processes.

### 5. Implementation

Execute migration plan:
- Update constitution files
- Update version number
- Update tooling/automation
- Announce to team
- Update training materials

### 6. Verification

Monitor for 30 days:
- Check for compliance issues
- Gather feedback
- Document lessons learned
- Adjust if needed

---

## Constitution Violations

### Early Detection

**Must be caught early**:
- Use **Vibe-Check MCP** regularly during work
- PR reviews must verify constitution compliance
- Violations must be corrected before merge
- Repeated violations require process improvement
- Document violations and corrections for learning

**Detection Points**:
- Pre-commit hooks (automated checks)
- Vibe-Check MCP validation (during work)
- Code review (peer validation)
- CI/CD pipeline (automated validation)

### Handling Violations

**First Time**:
1. **Educate** - Explain which principle was violated and why
2. **Document** - Record violation and correction in Pieces MCP
3. **Correct** - Fix before merge, all gates must pass

**Repeated Violations**:
1. **Identify Root Cause**:
   - Tooling inadequate?
   - Rules unclear?
   - Intentional bypass?
2. **Address Root Cause**:
   - Improve tooling automation
   - Clarify constitution language
   - Provide additional training

**Pattern Identified**:
1. **Analyze Pattern** - Multiple people/multiple times
2. **Update Constitution or Tooling** - Prevent recurrence systematically
3. **Share Learnings** - Team retrospective
4. **Track Effectiveness** - Monitor for 30 days

### Severity Classification

| Severity | Definition | Action |
|----------|-----------|--------|
| **Critical** | Security vulnerability, data integrity risk | Immediate rollback, fix before any other work |
| **High** | TDD skipped, quality gates bypassed | Block merge, require correction |
| **Medium** | Documentation missing, incomplete planning | Address before next sprint |
| **Low** | Minor process deviation | Document, discuss in retrospective |

---

## Constitution Evolution

**The constitution is living - it evolves with rigor and transparency.**

### Regular Reviews

**Cadence**:
- **Quarterly** reviews (standard)
- **After major milestones** (releases, large features)
- **Ad-hoc** when issues identified

**Review Questions**:
- What's working well?
- What's not working?
- What's missing?
- What should change?

### Feedback Sources

**1. Execution Logs**:
- Analyze `.plans/` execution logs
- Identify bottlenecks
- Find repeated issues
- Calculate time estimates accuracy

**2. Vibe-Check MCP Learnings**:
- Query `vibe_learn` history
- Identify mistake patterns
- Extract common pitfalls
- Document solutions

**3. Team Retrospectives**:
- Weekly/monthly team syncs
- Gather subjective feedback
- Discuss pain points
- Propose improvements

**4. Industry Research**:
- Use **Exa AI MCP** for best practices research
- Use **Context7 MCP** for framework documentation
- Study successful projects
- Adopt proven patterns

**5. Community Feedback** (if open source):
- GitHub issues/discussions
- User feedback
- Contributor suggestions
- Real-world usage patterns

### Evolution Process

Each review should:

1. **Identify Issues** - What's not working?
2. **Research Solutions** - Use MCPs to find best practices
3. **Propose Amendments** - Create amendment documents
4. **Validate with Experts** - Use Experts MCP or Vibe-Check MCP
5. **Execute Amendment Process** - Follow steps above
6. **Monitor Results** - Track effectiveness over 30 days

### Version History

Track all changes:
- **CHANGELOG.md** - All amendments and versions
- **Git history** - Constitution file changes
- **Pieces MCP** - Context and rationale for changes

**See**: [CHANGELOG.md](../CHANGELOG.md) for complete version history.

---

## Constitution Updates

**Current Version**: 3.0.0
**Last Updated**: 2025-10-15
**Next Review**: 2026-01-15

**Amendment Proposals**: `.specify/memory/amendments/`

---

**See Also**:
- [Principle V: Quality Gates](principles/05-quality-gates.md) - Gate enforcement details
- [CI/CD: Code Review Process](cicd.md#code-review-process) - Review checklist
- [Team Adaptations](team-adaptations.md) - Approval processes by team size
- [Principle I: MCP-First](principles/01-mcp-first.md) - Vibe-Check MCP usage
