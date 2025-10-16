# Naming Conventions - Quick Reference

## Core Principle
**Optimize for AI comprehension, not brevity**

## Good vs Bad Examples
```python
# ❌ BAD: Requires context
def calc_usr_dsc(u, c, p):
    return u.pts * c.val * p.pct

# ✅ GOOD: Self-documenting
def calculate_user_discount(user: User, cart: Cart, promo: PromoCode) -> Decimal:
    return user.loyalty_points * cart.total_value * promo.discount_percent
```

## Naming Patterns
| Type | Pattern | Example |
|------|---------|---------|
| **Functions** | verb_noun | `validate_email`, `process_payment` |
| **Classes** | NounPhrase | `UserAccount`, `PaymentProcessor` |
| **Variables** | descriptive_noun | `user_email`, `total_amount` |
| **Constants** | UPPER_SNAKE | `MAX_RETRY_COUNT`, `API_TIMEOUT` |
| **Modules** | feature_component | `user_validators`, `payment_service` |

## Directory Names
```
✅ authentication/     # Clear purpose
✅ payment_processing/ # Descriptive
✅ user_management/    # Obvious scope
❌ auth/              # Too abbreviated
❌ proc/              # Unclear
❌ mgmt/              # Ambiguous
```

## AI-Friendly Tips
- Spell out acronyms first use
- Use business terms consistently
- Avoid domain-specific abbreviations
- Include units in names: `timeout_seconds`
- Be specific: `email_address` not `email`

**Test**: Can AI understand without seeing implementation?