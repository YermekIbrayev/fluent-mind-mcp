# Architecture Patterns - Quick Reference

## Vertical Slice Structure
```
user_auth/
├── models.py      # Data structures (50-100 lines)
├── service.py     # Business logic (100-150 lines)
├── controller.py  # HTTP/API layer (50-100 lines)
├── validators.py  # Input validation (50 lines)
├── tests/         # All related tests
└── README.md      # 20-line overview
```

## Migration Pattern
```python
# FROM: Layer-based (scattered across codebase)
models/user.py         # 500 lines
controllers/auth.py    # 400 lines
services/user_service.py # 600 lines

# TO: Feature-based (colocated)
auth/models.py        # 100 lines
auth/service.py       # 150 lines
auth/controller.py    # 100 lines
```

## Benefits Checklist
- [ ] 80% less context needed
- [ ] Clear ownership boundaries
- [ ] Faster AI comprehension
- [ ] Easier testing
- [ ] Better modularity

## Decision Tree
```
New feature?
├─ YES → Create vertical slice
└─ NO → Modifying existing?
        ├─ YES → Time to refactor?
        │       ├─ YES → Migrate to slice
        │       └─ NO → Follow existing pattern
        └─ NO → Use shared modules

## Quick Commands
```bash
# Create new feature
mkdir -p features/payment/{tests,docs}
touch features/payment/{models,service,controller,validators,README}.md
```

**Rule**: Think features, not layers!