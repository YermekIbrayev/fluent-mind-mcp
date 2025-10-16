# IDE

**Category**: DevTools | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

VS Code diagnostics and code execution for validation and testing.

---

## Capabilities

- `getDiagnostics` - Get language diagnostics (errors, warnings, info)
- `executeCode` - Execute Python code in Jupyter kernel

---

## When to Use

- Checking for type errors before commit
- Validating syntax errors
- Running code in notebook context
- Testing code snippets
- Validating code quality before quality gates

---

## Key Functions

### getDiagnostics

**Purpose**: Get diagnostics for files (type errors, syntax errors, warnings)

**Parameters**:
- `uri` (optional) - File URI to get diagnostics for. If omitted, gets all files

**Returns**: List of diagnostics with:
- File URI
- Severity (error, warning, info)
- Message
- Line/column numbers
- Source (e.g., "typescript", "eslint")

**Example**:
```
getDiagnostics()
Returns: All diagnostics for workspace

getDiagnostics("file:///path/to/file.ts")
Returns: Diagnostics only for that file
```

### executeCode

**Purpose**: Execute Python code in Jupyter kernel

**Parameters**:
- `code` (required) - Python code to execute

**Important**:
- Executes in current Jupyter kernel
- Code persists across calls (shared state)
- Avoid modifying kernel state unless requested
- Previous executions affect future ones until kernel restart

**Example**:
```python
code: "import pandas as pd\ndf = pd.DataFrame({'a': [1,2,3]})\nprint(df)"
Returns: Execution output with DataFrame printed
```

---

## Usage Tips

**Before Committing**:
```
1. getDiagnostics() to check all files
2. Fix any errors or warnings
3. Verify clean before commit
```

**For Notebooks**:
```
1. executeCode with test snippets
2. Verify output
3. Iterate as needed
```

---

## Quality Gates Integration

Part of quality gate validation:
- IDE diagnostics must pass
- No type errors
- No syntax errors
- No unused imports (if configured)

See [Quality Gates](../memory/principles/05-quality-gates.md) for full requirements.

---

## Related

- [GitHub](github.md) - Commit after diagnostics pass
- [Workflows](../workflows.md) - Quality gate integration
