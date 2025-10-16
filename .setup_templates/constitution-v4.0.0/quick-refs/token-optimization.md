# Token Optimization - Quick Reference

## Context Budget
- **20%** Must-have (files being edited)
- **30%** Should-have (related context)
- **50%** Reserve (AI working memory)

## Loading Strategy
1. Start with minimal context
2. Add progressively as needed
3. Unload completed work
4. Never exceed 50% before starting

## Quick Wins
```python
# Before: 1000 tokens
"""
This function calculates the discount for a user based on their
membership status. Premium users receive a 20% discount, gold
users receive 15%, and regular users receive no discount.
"""

# After: 200 tokens
def calculate_discount(user):
    # Premium: 20%, Gold: 15%, Regular: 0%
    return DISCOUNT_RATES[user.membership]
```

## File Organization Impact
| Pattern | Token Usage | Comprehension |
|---------|------------|---------------|
| Vertical Slice | -80% | +90% |
| Small Files | -60% | +70% |
| Clear Names | -40% | +50% |
| Good README | -30% | +40% |

## Measurement
```bash
# Track token usage
echo "$(date),$(wc -l < file.py),$(git diff --stat)" >> token_log.csv
```

**Remember**: Every token saved = Faster AI + Lower costs + Better suggestions