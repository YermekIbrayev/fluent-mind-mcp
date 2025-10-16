# File Size Limits - Quick Reference

## Hard Limits
- **200 lines**: Maximum allowed ❌
- **150 lines**: Warning threshold ⚠️
- **100 lines**: Target size ✅

## Check File Sizes
```bash
# List all files >200 lines
find . -name "*.py" -exec wc -l {} + | awk '$1>200 {print}'

# Count average lines
find . -name "*.py" -exec wc -l {} + | awk '{sum+=$1; n++} END {print sum/n}'
```

## Splitting Strategies
1. **By responsibility**: Each class/function group in own file
2. **By feature**: Separate validators, serializers, helpers
3. **By complexity**: Extract complex algorithms
4. **By frequency**: Separate rarely-used code

## Enforcement
- Pre-commit hook warns at 150 lines
- CI/CD fails at 200 lines
- Weekly metrics track progress

**Remember**: Smaller files = Better AI comprehension = Faster development