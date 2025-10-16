# CI/CD and Automation

**Version**: 4.0.0 | **Part of**: [Constitution](INDEX.md)

**Related**: [Quality Gates](principles/05-quality-gates.md), [Team Adaptations](team-adaptations.md)

**Diagram**: [View Quality Gates Flow](diagrams/quality-gates-flow.mermaid)

---

## Overview

Automated enforcement of quality gates through pre-commit hooks and CI/CD pipeline.

---

## Quality Gates Flow

**Diagram**: [View Quality Gates Flow](diagrams/quality-gates-flow.mermaid)

**Text Summary**:
```
Local Development:
Write Code → Pre-commit Hooks → (Pass?) → Git Commit
                ↓ Fail
            Fix Issues → Loop back

CI/CD Pipeline:
Commit → Create PR → Run Tests → Check Coverage → Security Scan → (All Pass?) → Code Review → Merge
                                                                      ↓ Fail
                                                                  Fix Issues → Loop back
```

---

## Pre-commit Hooks

### Purpose
Catch issues locally before commit - fast feedback loop.

### Install
```bash
pre-commit install
```

Requires `.pre-commit-config.yaml` in project root.

### What Runs
1. **Semgrep MCP scan** - Fast scan on changed files
2. **Linting** - Code style enforcement
3. **Type checking** - Static type validation
4. **Format checking** - Code formatting

### Configuration
Example `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: semgrep-scan
        name: Semgrep Security Scan
        entry: semgrep
        language: system
        pass_filenames: false
      - id: lint
        name: Lint Code
        entry: ruff check
        language: system
      - id: typecheck
        name: Type Check
        entry: mypy
        language: system
```

### Bypass (NOT Recommended)
- Only for Experimental Code on spike/* branches
- Command: `git commit --no-verify`
- Document reason in commit message

---

## CI/CD Pipeline

### Triggers
- On pull request (any branch → main)
- On push to main
- On manual trigger

### Pipeline Steps

**1. Run Full Test Suite**
- All tests must pass
- No flaky tests allowed
- Fail pipeline if any test fails

**2. Check Coverage**
- Production Code: ≥80% overall, 100% Critical Path
- Generate coverage report
- Fail if below threshold

**3. Semgrep Security Scan**
- Full repository scan
- Fail on high/critical vulnerabilities
- Create issues for medium/low

**4. IDE Diagnostics Check**
- No type errors
- No syntax errors
- No unused imports/variables

**5. Validate Documentation Links**
- Check all internal links
- Check external links (if feasible)
- Report broken links

**6. Build Artifacts** (if applicable)
- Build application
- Verify build succeeds
- Store artifacts

**7. Run Integration/E2E Tests** (if applicable)
- Test full system
- Verify integrations
- Performance tests

### Configuration
Example GitHub Actions (`.github/workflows/ci.yml`):
```yaml
name: CI

on: [pull_request, push]

jobs:
  quality-gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Tests
        run: pytest

      - name: Check Coverage
        run: pytest --cov --cov-fail-under=80

      - name: Semgrep Scan
        run: semgrep --config=auto --error

      - name: Type Check
        run: mypy .

      - name: Validate Links
        run: markdown-link-check **/*.md
```

---

## Code Review Process

### Reviewer Qualifications
- Familiar with codebase area being changed
- Has completed 3+ PRs themselves (for team members)
- Understands constitution principles
- For security changes: Security team approval required

### Review Checklist

Code reviewers must verify:

- [ ] Code follows clean code principles and constitution
- [ ] Tests exist and pass (TDD for Production Code)
- [ ] No security vulnerabilities (Semgrep clean or issues tracked)
- [ ] Documentation updated (per [decision tree](principles/07-documentation.md#documentation-decision-tree))
- [ ] Constitution compliance verified (correct [work type](glossary.md#work-type-categories), gates passed)
- [ ] Performance acceptable (no obvious issues)
- [ ] Error handling appropriate
- [ ] Commit messages follow format (reference spec/plan if applicable)

### Approval Requirements

By team size (see [Team Adaptations](team-adaptations.md)):

**Solo Developer:**
- Self-review with Vibe-Check MCP validation
- Can commit directly after gates pass

**Small Team (2-5):**
- 1 peer approval minimum
- PR recommended for Production Code

**Large Team (6+):**
- 2 approvals minimum for Production Code
- 1 must be senior/architect for architectural changes
- Security team approval for security changes

### Review Timeline

- **First review**: Within 24 hours
- **Address feedback**: Within 48 hours
- **Final approval**: Within 72 hours
- **Urgent fixes**: Expedited process (notify team)

**Note**: Times are guidelines, adjust based on team location/size.

---

## Commit Message Format

### Standard Format
```
Brief summary (≤50 chars)

Optional details:
- What was changed
- Why it was changed
- Impact of change

[spec:NNNN plan:0042]  # If applicable
```

### Examples

**Feature with Spec**:
```
Add user authentication endpoint

- Implement JWT-based authentication
- Add login and logout endpoints
- Include rate limiting

spec:0042 plan:0123
```

**Bug Fix**:
```
Fix: Null pointer in user profile

- Add null check before accessing user data
- Add test case for null scenario
```

**Infrastructure**:
```
Update CI/CD pipeline for Python 3.12

- Upgrade GitHub Actions to use Python 3.12
- Update dependency versions
- Verify all tests pass
```

---

## Token Metrics (Track Weekly)

### Purpose
Monitor and optimize codebase for AI-assisted development efficiency.

### Metrics to Track

**1. Average Lines Per File**
- **Target**: <150 lines
- **Measurement**: `find . -name "*.py" -exec wc -l {} + | awk '{sum+=$1; files++} END {print sum/files}'`
- **Action**: Split files exceeding 200 lines

**2. Files Over 200 Lines**
- **Target**: <5% of codebase
- **Measurement**: `find . -name "*.py" -exec wc -l {} + | awk '$1>200 {count++} END {print count}'`
- **Action**: Refactor in next sprint

**3. Vertical Slice Percentage**
- **Target**: 80% of features
- **Measurement**: Count feature directories vs layer directories
- **Action**: Migrate during feature work

**4. Token Consumption Per PR**
- **Target**: 50% reduction from baseline
- **Measurement**: Track via AI platform APIs
- **Action**: Optimize context loading

**5. AI Suggestion Acceptance Rate**
- **Target**: >70%
- **Measurement**: IDE telemetry or manual tracking
- **Action**: Improve naming and structure

### Weekly Metrics Script

Create `scripts/token_metrics.py`:
```python
#!/usr/bin/env python3
"""Weekly token optimization metrics."""

import os
import json
from pathlib import Path
from datetime import datetime

def calculate_metrics():
    metrics = {
        "date": datetime.now().isoformat(),
        "avg_file_size": calculate_avg_file_size(),
        "files_over_200": count_large_files(),
        "vertical_slice_pct": calculate_vertical_percentage(),
        "token_consumption": get_token_consumption(),  # From AI platform
        "ai_acceptance_rate": get_acceptance_rate()    # From IDE
    }
    return metrics

def calculate_avg_file_size():
    """Calculate average lines per Python file."""
    total_lines = 0
    file_count = 0

    for path in Path('.').rglob('*.py'):
        if '.venv' not in str(path):
            with open(path) as f:
                total_lines += len(f.readlines())
                file_count += 1

    return total_lines / file_count if file_count > 0 else 0

def count_large_files():
    """Count files exceeding 200 lines."""
    large_files = []

    for path in Path('.').rglob('*.py'):
        if '.venv' not in str(path):
            with open(path) as f:
                lines = len(f.readlines())
                if lines > 200:
                    large_files.append((str(path), lines))

    return {"count": len(large_files), "files": large_files}

def calculate_vertical_percentage():
    """Calculate percentage of vertical slice adoption."""
    feature_dirs = 0
    layer_dirs = ['models', 'controllers', 'services', 'utils']

    for item in os.listdir('src'):
        path = Path('src') / item
        if path.is_dir():
            if item not in layer_dirs:
                # Check if it's a feature directory
                if any((path / subdir).exists() for subdir in ['models.py', 'service.py']):
                    feature_dirs += 1

    return (feature_dirs / len(os.listdir('src'))) * 100

if __name__ == "__main__":
    metrics = calculate_metrics()

    # Save metrics
    with open('metrics/token_metrics.json', 'a') as f:
        f.write(json.dumps(metrics) + '\n')

    # Display summary
    print(f"Token Optimization Metrics - {metrics['date'][:10]}")
    print(f"Average file size: {metrics['avg_file_size']:.0f} lines")
    print(f"Files >200 lines: {metrics['files_over_200']['count']}")
    print(f"Vertical slice adoption: {metrics['vertical_slice_pct']:.0f}%")
```

### CI/CD Integration

Add to pipeline:
```yaml
- name: Token Metrics Check
  run: |
    python scripts/token_metrics.py
    python scripts/check_file_sizes.py --max-lines 200
```

### Reporting

**Weekly Report Template**:
```markdown
# Token Optimization Report - Week [X]

## Metrics Summary
- Average file size: [X] lines (target: <150)
- Large files: [X] (target: <5%)
- Vertical slices: [X]% (target: 80%)
- Token usage: [X] per PR (target: -50% from baseline)
- AI acceptance: [X]% (target: >70%)

## Actions Taken
- Split [N] large files
- Migrated [N] features to vertical slices
- Optimized [N] README files

## Next Week Focus
- [Specific files to split]
- [Features to migrate]
```

### Success Indicators

**Green** (On Track):
- File size trending down
- Vertical slice adoption increasing
- Token usage decreasing
- AI acceptance increasing

**Yellow** (Needs Attention):
- Metrics flat for 2 weeks
- Some targets not met
- New large files appearing

**Red** (Immediate Action):
- Metrics trending wrong direction
- Multiple targets missed
- Token usage increasing

---

## Automation Anti-Patterns

❌ **Disabling pre-commit hooks** - Pushes problems to CI/CD
❌ **Ignoring CI/CD failures** - "Will fix later"
❌ **Not updating pipeline** - Stale checks
❌ **Manual deployments** - Inconsistent, error-prone
❌ **No rollback plan** - Can't recover from failures

---

## Automation Benefits

✅ **Consistent enforcement** - Same checks every time
✅ **Fast feedback** - Catch issues immediately
✅ **Reduced manual work** - Automated checks
✅ **Higher confidence** - Verified before merge
✅ **Documentation** - CI logs provide audit trail

---

**See Also**:
- [Principle V: Quality Gates](principles/05-quality-gates.md) - Gate requirements
- [Team Adaptations](team-adaptations.md) - Approval requirements by team size
- [Quality Gates Reference](references/quality-gates-ref.md) - Quick lookup
- [Diagram: Quality Gates Flow](diagrams/quality-gates-flow.mermaid) - Visual flow
