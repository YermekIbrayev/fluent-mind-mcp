# Team Size Adaptations

**Version**: 3.0.0 | **Part of**: [Constitution](INDEX.md)

**Related**: [CI/CD: Code Review](cicd.md#code-review-process), [Governance](governance.md)

---

## Principle

Enforcement scales with team size - appropriate oversight without bureaucracy.

---

## Solo Developer

### Review Process
- **Self-review** with MCP assistance
- Use Vibe-Check MCP to validate approach
- Use Sequential Thinking MCP for complex decisions
- PR process **optional** (can commit directly after gates pass)

### Planning
- Simplified for simple/moderate tasks
- Use [Planning Quick Reference](references/planning-ref.md)
- Complex tasks still need full planning

### Quality Gates
- **All gates still apply** for Production Code
- See [Quality Gates Reference](references/quality-gates-ref.md)
- Semgrep, IDE, tests, coverage all required

### Focus Areas
- Good commit messages (for future self)
- Documentation (you'll forget context)
- Knowledge management (Pieces MCP essential)
- Execution logs for complex tasks (learn from yourself)

### Benefits
- Fast iteration
- No approval overhead
- Deep ownership

### Risks
- Tunnel vision (use Vibe-Check MCP)
- No external validation (ask AI for review)
- Knowledge silos (document everything)

---

## Small Team (2-5 people)

### Review Process
- **Peer review required** (1 approver minimum)
- PR process **recommended** for Production Code
- Can skip for trivial Infrastructure Code
- Rotate code review responsibilities

### Planning
- Share planning approach across team
- Use consistent `.plans/` structure
- Review each other's execution logs

### Quality Gates
- All gates apply for Production Code
- CI/CD enforces automatically
- Team responsible for gate compliance

### Collaboration
- **Weekly sync** on quality metrics and learnings
- Share Pieces MCP findings
- Discuss ADRs together
- Retrospectives to improve process

### Focus Areas
- Shared responsibility for constitution compliance
- Knowledge sharing (don't silo)
- Consistent patterns
- Team learning

### Benefits
- Peer learning
- Shared ownership
- Fast feedback
- Manageable overhead

### Risks
- Inconsistent application (document standards)
- Review bottlenecks (rotate reviewers)
- Skipping process for speed (resist)

---

## Medium/Large Team (6+ people)

### Review Process
- **Formal code review** (2+ approvers for Production Code)
- PR process **mandatory** for all code
- Dedicated reviewers for security/architecture changes
- Security changes require security team approval

### Planning
- Formal planning for all non-trivial tasks
- Execution logs required for complex tasks
- Monthly review of planning accuracy

### Quality Gates
- Constitution compliance **tracked and reported**
- Monthly metrics dashboard
- Gate failures analyzed for patterns

### Governance
- **Formal onboarding process** for new contributors
- Constitution training required
- Monthly review of metrics and process improvements
- Dedicated roles:
  - Security champion (Semgrep enforcement)
  - Architecture lead (ADR oversight)
  - Quality lead (metrics tracking)

### Focus Areas
- Consistent enforcement
- Scalable processes
- Documentation excellence
- Team coordination

### Benefits
- High quality standards
- Diverse perspectives
- Clear accountability
- Professional process

### Risks
- Bureaucracy (keep lean)
- Slow iteration (optimize pipeline)
- Process over progress (balance)

---

## Comparison Table

| Aspect | Solo | Small (2-5) | Large (6+) |
|--------|------|-------------|-----------|
| **Approvers** | Self (+ MCP) | 1 peer | 2+ peers |
| **PR Process** | Optional | Recommended | Mandatory |
| **Planning** | Simplified | Shared | Formal |
| **Review Speed** | Immediate | <24 hours | <48 hours |
| **Governance** | Self | Consensus | Formal |
| **Training** | Self-study | Peer learning | Formal onboarding |
| **Metrics** | Personal | Weekly sync | Monthly dashboard |

---

## Scaling Guidance

### Growing from Solo to Small
- Establish PR process
- Document patterns and conventions
- Set up code review rotation
- Weekly syncs to align

### Growing from Small to Large
- Formalize review process (2+ approvers)
- Add dedicated roles (security, architecture, quality)
- Implement metrics tracking
- Create onboarding program
- Monthly governance reviews

### Maintaining at Scale
- Keep process lean (resist bureaucracy)
- Automate enforcement (CI/CD)
- Regular process reviews (quarterly)
- Listen to team feedback

---

## Common Pitfalls by Size

**Solo:**
❌ Skipping documentation (you'll forget)
❌ No external validation (use Vibe-Check MCP)
❌ Inconsistent process

**Small:**
❌ Informal processes that don't scale
❌ Knowledge silos
❌ Inconsistent enforcement

**Large:**
❌ Too much bureaucracy
❌ Slow iteration
❌ Process fatigue

---

**See Also**:
- [CI/CD: Code Review Process](cicd.md#code-review-process) - Review requirements
- [Governance: Amendment Process](governance.md#amendment-process) - Team-size dependent approval
- [Principle I: MCP-First](principles/01-mcp-first.md) - MCP for solo/small teams
