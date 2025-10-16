# Principle 8: Token-Efficient Architecture

## Purpose
Optimize codebase architecture for AI-assisted development by minimizing token consumption while maximizing context relevance and code comprehension.

## Core Requirements

### 8.1 Vertical Slice Architecture

#### Requirement
- **MUST** organize code by feature, not by technical layer
- **MUST** colocate all related code within feature boundaries
- **MUST** ensure each feature is self-contained and independently comprehensible

#### Structure
```
feature_name/
  ├── models.py       # Feature-specific models (100 lines max)
  ├── service.py      # Business logic (150 lines max)
  ├── controller.py   # API/HTTP handlers (100 lines max)
  ├── validators.py   # Input validation (50 lines max)
  ├── tests/          # All feature tests
  └── README.md       # Feature documentation (20 lines)
```

#### Benefits
- 80% reduction in context loading for feature work
- Clear ownership and boundaries
- Faster AI comprehension
- Reduced cross-file dependencies

### 8.2 File Size Limits

#### Hard Limits
- **Maximum**: 200 lines per file (enforced by CI/CD)
- **Target**: 100 lines per file (ideal for AI context)
- **Warning**: 150 lines per file (consider splitting)

#### Enforcement
```python
# In CI/CD pipeline
def check_file_size(filepath):
    lines = count_lines(filepath)
    if lines > 200:
        raise FileToLargeError(f"{filepath}: {lines} lines (max: 200)")
    elif lines > 150:
        warn(f"{filepath}: {lines} lines (consider splitting)")
```

#### Splitting Strategy
When a file exceeds limits:
1. Identify logical boundaries
2. Extract related functionality
3. Create focused modules
4. Update imports and tests

### 8.3 Module Organization

#### Single Responsibility
Each module **MUST** have one clear purpose:
- ✅ `user/authentication.py` - Only authentication logic
- ❌ `utils/helpers.py` - Mixed concerns

#### Explicit Exports
All modules **MUST** define `__all__`:
```python
# user/authentication.py
__all__ = ['authenticate', 'validate_token', 'refresh_token']

# Only exported items are part of public API
```

#### Clear Boundaries
- No circular imports allowed
- Dependencies flow downward
- Features depend on shared, not on each other
- Shared modules are truly generic

### 8.4 Context Management Strategy

#### Context Hierarchy
For each task, define:
1. **Must-have context** (20% of window)
   - Direct dependencies
   - Interfaces being implemented
   - Tests for current code

2. **Should-have context** (30% of window)
   - Related modules
   - Parent abstractions
   - Configuration

3. **Optional context** (50% reserve)
   - Similar features for reference
   - Documentation
   - Examples

#### Progressive Loading
```yaml
# Task: Fix user validation
Load Order:
  1. user/validators.py (must)
  2. user/models.py (must)
  3. tests/test_validators.py (must)
  4. user/service.py (should)
  5. auth/validators.py (optional - similar logic)
```

## Implementation Guidelines

### Migration Strategy
1. **New features**: Implement as vertical slices immediately
2. **Existing code**: Migrate during modifications
3. **Large files**: Split proactively (highest ROI)
4. **Never**: Big bang refactor

### Naming Conventions
Optimize for AI comprehension:
```python
# Good: Self-documenting
def calculate_user_discount(user: User, cart: Cart, promo: str) -> Decimal:
    """Calculate discount for user's cart with promotional code."""

# Bad: Requires context
def calc_usr_dsc(u, c, p):
    """calc dsc"""
```

### Directory Naming
Use clear, searchable names:
```
✅ authentication/
✅ payment_processing/
✅ inventory_management/
❌ auth/
❌ pay/
❌ inv/
```

## Metrics & Monitoring

### Track Weekly
1. Average lines per file
2. Files exceeding 200 lines
3. Vertical slice adoption %
4. Token consumption per feature
5. AI suggestion acceptance rate

### Success Indicators
- 50% reduction in tokens per feature
- 2x improvement in AI comprehension
- 30% faster feature development
- 60% reduction in API costs

## Exceptions

### Allowed Exceptions
1. **Generated code**: Can exceed limits with approval
2. **Configuration files**: Natural structure takes precedence
3. **Legacy interfaces**: During migration period only

### Exception Process
1. Document in ADR why exception needed
2. Set remediation timeline
3. Track in metrics as technical debt

## Quick Reference

### File Size Limits
- **200 lines**: Hard stop 🛑
- **150 lines**: Warning ⚠️
- **100 lines**: Target 🎯

### Architecture Rules
- **Vertical**: By feature, not layer
- **Small**: 100 lines ideal
- **Focused**: Single responsibility
- **Explicit**: Clear exports

### Token Optimization
- **Colocate**: Related code together
- **Split**: Large files aggressively
- **Name**: For AI comprehension
- **Document**: WHY, not WHAT

## Related Documents
- `.cursorrules` - Project-specific AI hints
- `quick-refs/token-optimization.md` - Optimization techniques
- `quick-refs/architecture.md` - Architecture patterns
- `metrics.py` - Tracking script