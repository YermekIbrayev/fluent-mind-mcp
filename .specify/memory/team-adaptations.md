# Team Size Adaptations

**Version**: 1.0.0 | **Part of**: [Constitution](INDEX.md)

**Related**: [Governance](governance.md), [CI/CD](cicd.md)

---

## Solo Developer

**Approval Process**:
- Self-approval with Vibe-Check MCP validation
- Use `vibe_check` before major decisions
- Document rationale thoroughly

**Code Review**:
- Self-review using constitution checklist
- Vibe-Check MCP for validation
- Pieces MCP for knowledge capture

**TDD**:
- Full TDD still required for Production Code
- Fast-track routine tests
- Approval via Vibe-Check MCP for new patterns

**Planning**:
- Simplified for simple tasks
- Still required for complex work
- Use execution logs for learning

**Amendment Process**:
- Self-approval with Vibe-Check validation
- Document decision thoroughly
- Update immediately

---

## Small Team (2-5 people)

**Approval Process**:
- Consensus required (all team members agree)
- Discuss in team sync
- Document decision

**Code Review**:
- 1 approver minimum
- Constitution compliance check
- Security review for sensitive changes

**TDD**:
- Approval from team member for critical paths
- Fast-track for routine tests
- Pair programming encouraged for complex logic

**Planning**:
- Standard planning levels apply
- Share execution logs
- Team retrospectives for improvement

**Amendment Process**:
- Team discussion required
- Consensus for approval
- Migration plan execution together

---

## Large Team (6+ people)

**Approval Process**:
- Formal proposal review
- 2/3 majority vote
- Architecture lead approval
- Announcement to all team members

**Code Review**:
- 2+ approvers required
- Security team review for sensitive code
- Architecture review for major changes
- Constitution compliance verification

**TDD**:
- Formal approval process for new patterns
- Test review in code review
- Test coverage tracked in CI/CD

**Planning**:
- Full planning levels enforced
- Execution logs required for complex work
- Regular retrospectives
- Knowledge sharing sessions

**Amendment Process**:
- RFC (Request for Comments) process
- Team-wide discussion
- 2/3 majority + architecture lead approval
- Formal announcement and training
- Rollout plan with timeline

---

## Scaling Considerations

### Communication

**Solo**: Notes and Pieces MCP
**Small**: Slack/chat + weekly sync
**Large**: Formal documentation + meetings

### Documentation

**Solo**: ADRs optional for simple decisions
**Small**: ADRs for major decisions
**Large**: Comprehensive ADRs + RFCs

### Automation

**Solo**: Pre-commit hooks recommended
**Small**: Pre-commit hooks + basic CI/CD
**Large**: Full CI/CD pipeline + automation

---

**See Also**:
- [Governance](governance.md) - Amendment process details
- [CI/CD](cicd.md) - Automated checks
- [Principle II: TDD](principles/02-tdd.md) - Approval process
