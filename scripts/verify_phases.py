#!/usr/bin/env python3
"""
Automated Phase Verification Script

Verifies all phases (1-6) meet quality standards:
1. No fake tests (assert True)
2. No empty tests (meaningful assertions)
3. Tests actually testing functionality
4. Target functions implemented (no NotImplementedError)
5. Really works (tests passing)
6. No placeholders/fake/mock responses

Usage:
    python scripts/verify_phases.py
    python scripts/verify_phases.py --json  # Output as JSON
    python scripts/verify_phases.py --update-tasks  # Update task files
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict

# Try to import tqdm for progress bars, fallback to simple progress
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("💡 Install tqdm for progress bars: pip install tqdm")


class PhaseVerifier:
    """Automated verification of test quality and implementation status."""

    def __init__(self, project_root: Path = None):
        """
        Initialize the verifier.

        WHY: We need a single source of truth for project structure
        to avoid hardcoding paths throughout the script.
        """
        self.project_root = project_root or Path.cwd()
        self.tests_dir = self.project_root / "tests"
        self.src_dir = self.project_root / "src"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "pass_conditions": {},
            "phases": {},
            "overall": {},
            "files_scanned": [],
        }

    def verify_all(self) -> Dict:
        """
        Run all verification checks organized by phase.

        WHY: Single entry point for all verification logic.
        Returns structured results for reporting.
        """
        print("🔍 Starting Phase Verification...\n")

        # First, analyze phases
        self.analyze_phases()

        # Run verification for each phase
        for phase_name in sorted(self.results["phases"].keys()):
            self.verify_phase(phase_name)

        # Overall verification
        print("\n📊 Overall Project Verification\n")

        # Condition 4: Check implementations
        self.verify_implementations()

        # Condition 5: Run tests
        self.verify_tests_pass()

        # Calculate overall status
        self.calculate_overall_status()

        return self.results

    def analyze_phases(self) -> None:
        """
        Analyze and categorize test files by phase.

        WHY: We need to organize verification by phase
        to provide clear progress tracking.
        """
        test_files = list(self.tests_dir.rglob("test_*.py"))

        phases = {
            "Phase 1 (US1-US3)": [],
            "Phase 2 (US4)": [],
            "Phase 3 (US5)": [],
            "Other": []
        }

        for test_file in test_files:
            path_str = str(test_file)
            if 'phase1' in path_str:
                phases["Phase 1 (US1-US3)"].append(test_file)
            elif 'phase2' in path_str:
                # Determine if US4 or US5
                if 'error' in test_file.name.lower() or 'us5' in path_str:
                    phases["Phase 3 (US5)"].append(test_file)
                else:
                    phases["Phase 2 (US4)"].append(test_file)
            else:
                phases["Other"].append(test_file)

        # Store phase info
        for phase_name, files in phases.items():
            if files:  # Only include non-empty phases
                self.results["phases"][phase_name] = {
                    "total_files": len(files),
                    "files": [str(f.relative_to(self.project_root)) for f in files],
                    "checks": {}
                }

    def verify_phase(self, phase_name: str) -> None:
        """
        Verify a single phase.

        WHY: Organize verification by phase for better tracking.
        """
        phase_data = self.results["phases"][phase_name]
        test_files = [self.project_root / f for f in phase_data["files"]]

        print(f"\n{'='*80}")
        print(f"📦 {phase_name}")
        print(f"{'='*80}")
        print(f"Total test files: {len(test_files)}\n")

        # Count tests and assertions
        total_tests = 0
        total_assertions = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
                total_tests += len(re.findall(r'def test_', content))
                total_assertions += len(re.findall(r'assert ', content))

        print(f"Total tests: {total_tests}")
        print(f"Total assertions: {total_assertions}\n")

        # Run checks for this phase
        self.verify_phase_fake_tests(phase_name, test_files)
        self.verify_phase_empty_tests(phase_name, test_files)
        self.verify_phase_assertion_quality(phase_name, test_files)
        self.verify_phase_mocks(phase_name, test_files)

    def verify_phase_fake_tests(self, phase_name: str, test_files: list) -> None:
        """Check for fake tests in a specific phase."""
        fake_tests = []

        iterator = tqdm(test_files, desc="   ✓ Fake tests", unit="files", leave=True) if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                count = 0
                for line in lines:
                    if line.strip().startswith('#'):
                        continue
                    if re.search(r'\bassert\s+True\b', line):
                        count += 1

                if count > 0:
                    fake_tests.append({
                        "file": str(test_file.relative_to(self.project_root)),
                        "count": count
                    })

        passed = len(fake_tests) == 0
        self.results["phases"][phase_name]["checks"]["no_fake_tests"] = {
            "passed": passed,
            "count": sum(ft["count"] for ft in fake_tests)
        }

        if not passed and not HAS_TQDM:
            print(f"   ✓ Fake tests: ❌ {len(fake_tests)} files")

    def verify_phase_empty_tests(self, phase_name: str, test_files: list) -> None:
        """Check for empty tests in a specific phase."""
        empty_tests = []

        iterator = tqdm(test_files, desc="   ✓ Empty tests", unit="files", leave=True) if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                standalone_pass = []
                for i, line in enumerate(lines):
                    if re.match(r'^\s+pass\s*$', line):
                        is_exception_handler = False
                        for j in range(max(0, i-2), i):
                            if 'except' in lines[j] or 'try:' in lines[j]:
                                is_exception_handler = True
                                break
                        if not is_exception_handler:
                            standalone_pass.append(i + 1)

                if standalone_pass:
                    empty_tests.append({
                        "file": str(test_file.relative_to(self.project_root)),
                        "lines": standalone_pass
                    })

        passed = len(empty_tests) == 0
        self.results["phases"][phase_name]["checks"]["no_empty_tests"] = {
            "passed": passed,
            "count": len(empty_tests)
        }

        if not passed and not HAS_TQDM:
            print(f"   ✓ Empty tests: ❌ {len(empty_tests)} files")

    def verify_phase_assertion_quality(self, phase_name: str, test_files: list) -> None:
        """Analyze assertion quality for a specific phase."""
        total_tests = 0
        total_assertions = 0

        iterator = tqdm(test_files, desc="   ✓ Assertion quality", unit="files", leave=True) if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()
                tests = len(re.findall(r'def test_', content))
                assertions = len(re.findall(r'assert ', content))
                total_tests += tests
                total_assertions += assertions

        avg = round(total_assertions / total_tests, 2) if total_tests > 0 else 0
        passed = avg >= 2.0

        self.results["phases"][phase_name]["checks"]["assertion_quality"] = {
            "passed": passed,
            "avg_per_test": avg,
            "total_tests": total_tests,
            "total_assertions": total_assertions
        }

        if not passed and not HAS_TQDM:
            print(f"   ✓ Assertion quality: ⚠️  avg {avg}")

    def verify_phase_mocks(self, phase_name: str, test_files: list) -> None:
        """Check for mock usage in a specific phase."""
        mock_files = []

        iterator = tqdm(test_files, desc="   ✓ Mock usage", unit="files", leave=True) if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()
                in_test_function = False
                mock_count = 0
                lines = content.split('\n')

                for line in lines:
                    if re.match(r'\s*def test_', line):
                        in_test_function = True
                    elif re.match(r'\s*def ', line) and not re.match(r'\s*def test_', line):
                        in_test_function = False
                    elif re.match(r'^class ', line):
                        in_test_function = False

                    if '@patch' in line or '@mock' in line:
                        mock_count += 1
                    elif in_test_function:
                        if 'Mock(' in line or 'MagicMock(' in line:
                            mock_count += 1

                if mock_count > 0:
                    mock_files.append({
                        "file": str(test_file.relative_to(self.project_root)),
                        "count": mock_count
                    })

        total_mocks = sum(mf["count"] for mf in mock_files)
        passed = total_mocks <= 5  # Per-phase threshold

        self.results["phases"][phase_name]["checks"]["minimal_mocks"] = {
            "passed": passed,
            "total_mocks": total_mocks,
            "files_with_mocks": len(mock_files)
        }

        if not passed and not HAS_TQDM:
            print(f"   ✓ Mock usage: ⚠️  {total_mocks} total")

    def verify_no_fake_tests(self) -> None:
        """
        Check for fake tests (assert True).

        WHY: assert True is a placeholder that doesn't test anything.
        Real tests must validate actual behavior.
        """
        print("📋 Checking for fake tests (assert True)...")

        fake_tests = []
        test_files = list(self.tests_dir.rglob("test_*.py"))

        # Create progress bar if tqdm available
        iterator = tqdm(test_files, desc="   Scanning", unit="files") if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()
                # Only count assert True that's not in comments or strings
                lines = content.split('\n')
                count = 0
                for line in lines:
                    # Skip comments
                    if line.strip().startswith('#'):
                        continue
                    # Count assert True (case sensitive)
                    if re.search(r'\bassert\s+True\b', line):
                        count += 1

                if count > 0:
                    fake_tests.append({
                        "file": str(test_file.relative_to(self.project_root)),
                        "count": count
                    })

        passed = len(fake_tests) == 0
        self.results["pass_conditions"]["no_fake_tests"] = {
            "passed": passed,
            "fake_tests_found": fake_tests,
            "total_count": sum(ft["count"] for ft in fake_tests),
        }

        if passed:
            print("   ✅ No fake tests found\n")
        else:
            print(f"   ❌ Found {len(fake_tests)} files with assert True\n")

    def verify_no_empty_tests(self) -> None:
        """
        Check for empty tests (pass statements in test logic).

        WHY: Empty pass statements indicate incomplete or placeholder tests.
        Exception handlers with pass are OK, but test bodies should not be empty.
        """
        print("📋 Checking for empty tests...")

        empty_tests = []
        test_files = list(self.tests_dir.rglob("test_*.py"))

        iterator = tqdm(test_files, desc="   Scanning", unit="files") if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()
                # Count pass statements (excluding exception handlers)
                # This is a heuristic - we look for standalone pass statements
                matches = re.findall(r'^\s+pass\s*$', content, re.MULTILINE)
                # Filter out exception handlers (pass after except:)
                # Simple heuristic: if pass is preceded by except within 2 lines
                lines = content.split('\n')
                standalone_pass = []
                for i, line in enumerate(lines):
                    if re.match(r'^\s+pass\s*$', line):
                        # Check if this is in an exception handler
                        is_exception_handler = False
                        for j in range(max(0, i-2), i):
                            if 'except' in lines[j] or 'try:' in lines[j]:
                                is_exception_handler = True
                                break
                        if not is_exception_handler:
                            standalone_pass.append(i + 1)

                if standalone_pass:
                    empty_tests.append({
                        "file": str(test_file.relative_to(self.project_root)),
                        "lines": standalone_pass
                    })

        passed = len(empty_tests) == 0
        self.results["pass_conditions"]["no_empty_tests"] = {
            "passed": passed,
            "empty_tests_found": empty_tests,
        }

        if passed:
            print("   ✅ No empty tests found\n")
        else:
            print(f"   ❌ Found {len(empty_tests)} files with empty pass statements\n")

    def verify_assertion_quality(self) -> None:
        """
        Analyze assertion quality across all test files.

        WHY: We want to ensure tests have meaningful assertions
        that actually validate behavior.
        """
        print("📋 Analyzing assertion quality...")

        test_files = list(self.tests_dir.rglob("test_*.py"))
        total_tests = 0
        total_assertions = 0

        phase_stats = defaultdict(lambda: {"tests": 0, "assertions": 0, "files": []})

        iterator = tqdm(test_files, desc="   Analyzing", unit="files") if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()

                # Count test functions
                tests = len(re.findall(r'def test_', content))
                # Count assertions
                assertions = len(re.findall(r'assert ', content))

                total_tests += tests
                total_assertions += assertions

                # Determine phase
                if 'phase1' in str(test_file):
                    phase = 'phase1'
                elif 'phase2' in str(test_file):
                    phase = 'phase2'
                else:
                    phase = 'other'

                phase_stats[phase]["tests"] += tests
                phase_stats[phase]["assertions"] += assertions
                phase_stats[phase]["files"].append({
                    "file": str(test_file.relative_to(self.project_root)),
                    "tests": tests,
                    "assertions": assertions,
                    "avg": round(assertions / tests, 2) if tests > 0 else 0
                })

        avg_assertions = round(total_assertions / total_tests, 2) if total_tests > 0 else 0
        passed = avg_assertions >= 2.0  # At least 2 assertions per test on average

        self.results["pass_conditions"]["assertion_quality"] = {
            "passed": passed,
            "total_tests": total_tests,
            "total_assertions": total_assertions,
            "avg_per_test": avg_assertions,
            "by_phase": dict(phase_stats),
        }

        if passed:
            print(f"   ✅ Assertion quality good (avg {avg_assertions} per test)\n")
        else:
            print(f"   ⚠️  Low assertion count (avg {avg_assertions} per test)\n")

    def verify_implementations(self) -> None:
        """
        Check for NotImplementedError in source code.

        WHY: NotImplementedError indicates unfinished implementations.
        Production code should have all features implemented.
        """
        print("📋 Checking for missing implementations...")

        not_implemented = []
        src_files = list(self.src_dir.rglob("*.py"))
        src_files = [f for f in src_files if '__pycache__' not in str(f)]

        iterator = tqdm(src_files, desc="   Scanning", unit="files") if HAS_TQDM else src_files

        for src_file in iterator:
            with open(src_file, 'r') as f:
                content = f.read()
                if 'NotImplementedError' in content:
                    # Count occurrences
                    count = len(re.findall(r'NotImplementedError', content))
                    not_implemented.append({
                        "file": str(src_file.relative_to(self.project_root)),
                        "count": count
                    })

        passed = len(not_implemented) == 0
        self.results["pass_conditions"]["implementations_complete"] = {
            "passed": passed,
            "not_implemented_found": not_implemented,
        }

        if passed:
            print("   ✅ All implementations complete\n")
        else:
            print(f"   ❌ Found NotImplementedError in {len(not_implemented)} files\n")

    def verify_tests_pass(self) -> None:
        """
        Run pytest to verify all tests pass.

        WHY: Tests must actually pass to validate functionality.
        We run pytest and parse the output, categorizing by phase.
        """
        print("📋 Running tests...\n")

        try:
            # Run pytest with streaming output
            process = subprocess.Popen(
                ["python", "-m", "pytest",
                 "tests/",  # Scan all test directories
                 "-v", "--tb=no", "-q"],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Capture output while displaying it
            output_lines = []
            for line in process.stdout:
                print(f"   {line}", end='')
                output_lines.append(line)

            # Wait for completion
            process.wait(timeout=180)
            output = ''.join(output_lines)

            # Extract test counts
            # Look for patterns like "167 passed in 71.93s"
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)
            time_match = re.search(r'in ([\d.]+)s', output)

            passed_count = int(passed_match.group(1)) if passed_match else 0
            failed_count = int(failed_match.group(1)) if failed_match else 0
            execution_time = float(time_match.group(1)) if time_match else 0

            # Categorize failures by phase
            failed_tests_by_phase = self._categorize_test_failures(output)

            all_passed = failed_count == 0 and passed_count > 0

            self.results["pass_conditions"]["tests_pass"] = {
                "passed": all_passed,
                "total_tests": passed_count + failed_count,
                "passed_count": passed_count,
                "failed_count": failed_count,
                "execution_time": execution_time,
                "avg_time_per_test": round(execution_time / (passed_count + failed_count), 2) if (passed_count + failed_count) > 0 else 0,
                "failures_by_phase": failed_tests_by_phase,
            }

            # Display results by phase
            if all_passed:
                print(f"\n   ✅ All {passed_count} tests passing ({execution_time}s)\n")
            else:
                print(f"\n   ❌ {failed_count} tests failing\n")
                self._print_failures_by_phase(failed_tests_by_phase)

        except subprocess.TimeoutExpired:
            print("   ❌ Test execution timed out\n")
            self.results["pass_conditions"]["tests_pass"] = {
                "passed": False,
                "error": "Timeout"
            }
        except Exception as e:
            print(f"   ❌ Error running tests: {e}\n")
            self.results["pass_conditions"]["tests_pass"] = {
                "passed": False,
                "error": str(e)
            }

    def _categorize_test_failures(self, output: str) -> Dict:
        """
        Categorize test failures by phase.

        WHY: We need to know which phase has failing tests
        to provide actionable feedback.
        """
        failures_by_phase = {
            "Phase 1 (US1-US3)": set(),
            "Phase 2 (US4)": set(),
            "Phase 3 (US5)": set(),
            "Other": set()
        }

        # Extract FAILED lines from pytest output
        # Format: FAILED tests/path/to/test.py::TestClass::test_method
        failed_pattern = r'FAILED (tests/[^\s]+::[^\s]+)'
        for match in re.finditer(failed_pattern, output):
            test_name = match.group(1)
            test_path = test_name.split('::')[0]

            # Categorize by phase
            if 'phase1' in test_path:
                failures_by_phase["Phase 1 (US1-US3)"].add(test_name)
            elif 'phase2' in test_path:
                # Check if it's US4 or US5
                if 'error' in test_path.lower() or 'us5' in test_path:
                    failures_by_phase["Phase 3 (US5)"].add(test_name)
                else:
                    failures_by_phase["Phase 2 (US4)"].add(test_name)
            elif 'acceptance' in test_path:
                # Check user story number
                if 'user_story_1' in test_path or 'user_story_2' in test_path or 'user_story_3' in test_path:
                    failures_by_phase["Phase 1 (US1-US3)"].add(test_name)
                elif 'user_story_4' in test_path:
                    failures_by_phase["Phase 2 (US4)"].add(test_name)
                elif 'user_story_5' in test_path:
                    failures_by_phase["Phase 3 (US5)"].add(test_name)
                else:
                    failures_by_phase["Other"].add(test_name)
            else:
                failures_by_phase["Other"].add(test_name)

        # Convert sets to sorted lists and remove empty phases
        return {k: sorted(list(v)) for k, v in failures_by_phase.items() if v}

    def _print_failures_by_phase(self, failures_by_phase: Dict) -> None:
        """
        Print test failures organized by phase.

        WHY: Makes it easy to see which phase needs attention.
        """
        for phase_name, failures in failures_by_phase.items():
            print(f"\n   📦 {phase_name}: {len(failures)} failing")
            for failure in failures:
                print(f"      • {failure}")

    def verify_no_mocks(self) -> None:
        """
        Check for excessive mock usage in tests.

        WHY: Mocks can hide real implementation issues.
        We allow minimal mocking but flag heavy usage.
        We only count actual mock/patch usage in test functions,
        not imports or fixture definitions.
        """
        print("📋 Checking for mock usage...")

        mock_files = []
        test_files = list(self.tests_dir.rglob("test_*.py"))

        iterator = tqdm(test_files, desc="   Scanning", unit="files") if HAS_TQDM else test_files

        for test_file in iterator:
            with open(test_file, 'r') as f:
                content = f.read()

                # Only count mock usage in test function bodies
                # Look for: @patch, @mock, Mock(), MagicMock() inside test functions
                in_test_function = False
                mock_count = 0
                lines = content.split('\n')

                for line in lines:
                    # Check if we're in a test function
                    if re.match(r'\s*def test_', line):
                        in_test_function = True
                    elif re.match(r'\s*def ', line) and not re.match(r'\s*def test_', line):
                        in_test_function = False
                    elif re.match(r'^class ', line):
                        in_test_function = False

                    # Count mocks only in test functions or as decorators
                    if '@patch' in line or '@mock' in line:
                        mock_count += 1
                    elif in_test_function:
                        if 'Mock(' in line or 'MagicMock(' in line:
                            mock_count += 1

                if mock_count > 0:
                    mock_files.append({
                        "file": str(test_file.relative_to(self.project_root)),
                        "count": mock_count
                    })

        total_mocks = sum(mf["count"] for mf in mock_files)
        # Allow up to 15 mocks total (minimal usage threshold)
        passed = total_mocks <= 15

        self.results["pass_conditions"]["minimal_mocks"] = {
            "passed": passed,
            "total_mocks": total_mocks,
            "mock_files": mock_files,
        }

        if passed:
            print(f"   ✅ Minimal mock usage ({total_mocks} total)\n")
        else:
            print(f"   ⚠️  High mock usage ({total_mocks} total)\n")

    def calculate_overall_status(self) -> None:
        """
        Calculate overall pass/fail status from phase results.

        WHY: We need a simple yes/no answer: is the codebase ready?
        """
        # Aggregate phase results
        all_phase_checks_passed = True
        total_phase_checks = 0
        passed_phase_checks = 0

        for _phase_name, phase_data in self.results["phases"].items():
            for _check_name, check_result in phase_data["checks"].items():
                total_phase_checks += 1
                if check_result.get("passed", False):
                    passed_phase_checks += 1
                else:
                    all_phase_checks_passed = False

        # Combine with pass_conditions
        conditions = self.results.get("pass_conditions", {})
        all_conditions_passed = all(c.get("passed", False) for c in conditions.values())

        all_passed = all_phase_checks_passed and all_conditions_passed

        self.results["overall"] = {
            "all_conditions_passed": all_passed,
            "total_conditions": len(conditions) + total_phase_checks,
            "passed_conditions": sum(1 for c in conditions.values() if c.get("passed", False)) + passed_phase_checks,
            "ready_for_production": all_passed,
            "phase_checks": {
                "total": total_phase_checks,
                "passed": passed_phase_checks,
                "all_passed": all_phase_checks_passed
            }
        }

    def generate_report(self, format: str = "text") -> str:
        """
        Generate verification report.

        WHY: Different consumers need different formats.
        Text for humans, JSON for automation.

        Args:
            format: "text" or "json"
        """
        if format == "json":
            return json.dumps(self.results, indent=2)

        # Text format
        lines = []
        lines.append("=" * 80)
        lines.append("AUTOMATED PHASE VERIFICATION REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {self.results['timestamp']}")
        lines.append("")

        # Overall status
        overall = self.results["overall"]
        status_icon = "✅" if overall["all_conditions_passed"] else "❌"
        lines.append(f"{status_icon} Overall Status: {'PASSED' if overall['all_conditions_passed'] else 'FAILED'}")
        lines.append(f"   Conditions Passed: {overall['passed_conditions']}/{overall['total_conditions']}")
        lines.append("")

        # Individual conditions
        lines.append("PASS CONDITIONS:")
        lines.append("")

        conditions = self.results["pass_conditions"]

        # Condition 1: No fake tests
        c1 = conditions.get("no_fake_tests", {})
        icon = "✅" if c1.get("passed") else "❌"
        lines.append(f"{icon} 1. No fake tests")
        if c1.get("passed"):
            lines.append(f"   0 instances of 'assert True' found")
        else:
            lines.append(f"   Found {c1.get('total_count', 0)} fake tests in {len(c1.get('fake_tests_found', []))} files")
        lines.append("")

        # Condition 2: No empty tests
        c2 = conditions.get("no_empty_tests", {})
        icon = "✅" if c2.get("passed") else "❌"
        lines.append(f"{icon} 2. No empty tests")
        if c2.get("passed"):
            lines.append(f"   All tests have meaningful assertions")
        else:
            lines.append(f"   Found empty pass statements in {len(c2.get('empty_tests_found', []))} files")
        lines.append("")

        # Condition 3: Assertion quality
        c3 = conditions.get("assertion_quality", {})
        icon = "✅" if c3.get("passed") else "⚠️ "
        lines.append(f"{icon} 3. Tests actually testing functionality")
        lines.append(f"   Total assertions: {c3.get('total_assertions', 0)}")
        lines.append(f"   Total tests: {c3.get('total_tests', 0)}")
        lines.append(f"   Avg per test: {c3.get('avg_per_test', 0)}")
        lines.append("")

        # Condition 4: Implementations complete
        c4 = conditions.get("implementations_complete", {})
        icon = "✅" if c4.get("passed") else "❌"
        lines.append(f"{icon} 4. Target functions implemented")
        if c4.get("passed"):
            lines.append(f"   0 NotImplementedError found in source code")
        else:
            lines.append(f"   Found NotImplementedError in {len(c4.get('not_implemented_found', []))} files")
        lines.append("")

        # Condition 5: Tests pass
        c5 = conditions.get("tests_pass", {})
        icon = "✅" if c5.get("passed") else "❌"
        lines.append(f"{icon} 5. Really works (tests passing)")
        if c5.get("passed"):
            lines.append(f"   {c5.get('passed_count', 0)}/{c5.get('total_tests', 0)} tests passing")
            lines.append(f"   Execution time: {c5.get('execution_time', 0)}s")
            lines.append(f"   Avg per test: {c5.get('avg_time_per_test', 0)}s")
        else:
            lines.append(f"   {c5.get('failed_count', 0)} tests failing")
            failures_by_phase = c5.get("failures_by_phase", {})
            if failures_by_phase:
                lines.append("")
                lines.append("   Failures by phase:")
                for phase_name, failures in failures_by_phase.items():
                    lines.append(f"   📦 {phase_name}: {len(failures)} failing")
                    for failure in failures[:5]:  # Show first 5
                        lines.append(f"      • {failure}")
                    if len(failures) > 5:
                        lines.append(f"      ... and {len(failures) - 5} more")
        lines.append("")

        # Condition 6: Minimal mocks
        c6 = conditions.get("minimal_mocks", {})
        icon = "✅" if c6.get("passed") else "⚠️ "
        lines.append(f"{icon} 6. No placeholders/fake/mock responses")
        lines.append(f"   Total mocks: {c6.get('total_mocks', 0)}")
        if c6.get("total_mocks", 0) > 0:
            lines.append(f"   Files with mocks: {len(c6.get('mock_files', []))}")
        lines.append("")

        # Production readiness
        lines.append("=" * 80)
        if overall["all_conditions_passed"]:
            lines.append("✅ READY FOR PRODUCTION")
        else:
            lines.append("❌ NOT READY FOR PRODUCTION")
        lines.append("=" * 80)

        return "\n".join(lines)


def main():
    """Main entry point for the verification script."""
    parser = argparse.ArgumentParser(
        description="Automated phase verification for fluent-mind-mcp"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--update-tasks",
        action="store_true",
        help="Update task files with verification results"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Save report to file"
    )

    args = parser.parse_args()

    # Run verification
    verifier = PhaseVerifier()
    results = verifier.verify_all()

    # Generate report
    format_type = "json" if args.json else "text"
    report = verifier.generate_report(format=format_type)

    # Output report
    if args.output:
        args.output.write_text(report)
        print(f"\n📄 Report saved to: {args.output}")
    else:
        print("\n" + report)

    # Update task files if requested
    if args.update_tasks:
        print("\n📝 Updating task files...")
        # TODO: Implement task file update logic
        print("   (Task file update not yet implemented)")

    # Exit with appropriate code
    sys.exit(0 if results["overall"]["all_conditions_passed"] else 1)


if __name__ == "__main__":
    main()
