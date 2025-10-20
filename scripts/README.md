# Verification Scripts

Automated quality verification tools for fluent-mind-mcp.

## verify_phases.py

Automated verification script that checks all phases (1-6) meet quality standards.

### Installation

```bash
# Optional: Install tqdm for progress bars
pip install tqdm
```

### Usage

```bash
# Basic verification (text output)
python scripts/verify_phases.py

# JSON output
python scripts/verify_phases.py --json

# Save report to file
python scripts/verify_phases.py --output report.txt

# JSON to file
python scripts/verify_phases.py --json --output report.json
```

### Pass Conditions

The script verifies 6 critical conditions:

1. **No fake tests** - Zero instances of `assert True` (placeholder tests)
2. **No empty tests** - All tests have meaningful assertions
3. **Tests actually testing functionality** - Average ≥2 assertions per test
4. **Target functions implemented** - No `NotImplementedError` in source code
5. **Really works** - All tests passing (100%)
6. **No placeholders/mocks** - Minimal mock usage (≤15 total)

### Output Format

**Text Format** (default):
```
================================================================================
AUTOMATED PHASE VERIFICATION REPORT
================================================================================
Generated: 2025-10-19T19:48:15.372368

✅ Overall Status: PASSED
   Conditions Passed: 6/6

PASS CONDITIONS:

✅ 1. No fake tests
   0 instances of 'assert True' found

...

================================================================================
✅ READY FOR PRODUCTION
================================================================================
```

**JSON Format** (`--json` flag):
```json
{
  "timestamp": "2025-10-19T19:48:15.372368",
  "pass_conditions": {
    "no_fake_tests": {
      "passed": true,
      "fake_tests_found": [],
      "total_count": 0
    },
    ...
  },
  "overall": {
    "all_conditions_passed": true,
    "total_conditions": 6,
    "passed_conditions": 6,
    "ready_for_production": true
  }
}
```

### Exit Codes

- `0` - All conditions passed
- `1` - One or more conditions failed

### Integration with CI/CD

```bash
# In your CI pipeline
python scripts/verify_phases.py --json --output verification.json

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Quality checks passed - deploying to production"
else
    echo "❌ Quality checks failed - blocking deployment"
    exit 1
fi
```

### What Gets Scanned

- **Test Files**: All `test_*.py` files in `tests/` directory
- **Source Files**: All `*.py` files in `src/` directory
- **Test Execution**: Full pytest suite in `tests/` directory

### Performance

- Scanning: ~1-2 seconds (with tqdm progress bars)
- Test Execution: ~70-80 seconds for full suite
- Total Runtime: ~75-85 seconds

### Features

- ✅ Progress bars (with tqdm)
- ✅ Detailed reporting (text or JSON)
- ✅ Exit codes for automation
- ✅ Comprehensive test quality analysis
- ✅ Source code validation
- ✅ Real test execution (not just static analysis)

### Limitations

- Does not verify test coverage percentage
- Does not check for security vulnerabilities
- Does not validate documentation completeness
- Focuses on test quality and implementation status only

### Example Workflow

```bash
# Before committing
python scripts/verify_phases.py

# Before creating PR
python scripts/verify_phases.py --output pr_verification.txt
# Attach pr_verification.txt to PR description

# In CI/CD
python scripts/verify_phases.py --json --output ci_report.json
# Parse ci_report.json for deployment decision
```

### Troubleshooting

**ImportError: No module named 'tqdm'**
- Solution: `pip install tqdm` or run without progress bars

**Tests timing out**
- Default timeout: 180 seconds (3 minutes)
- Check for hanging tests or infinite loops

**High mock usage warning**
- Review mock_files in output
- Consider replacing mocks with real implementations

**Permission denied**
- Make script executable: `chmod +x scripts/verify_phases.py`
- Or run with: `python scripts/verify_phases.py`
