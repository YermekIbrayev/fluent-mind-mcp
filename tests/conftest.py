"""Pytest configuration for test suite.

This module configures the test environment:
- Unit tests: Isolated from .env file and environment variables
- Integration/Acceptance tests: Load .env file for real Flowise connection
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Load .env file at module import time to ensure it's available for module-level skipif checks
# WHY: Integration/acceptance tests use module-level skipif that checks FLOWISE_API_URL
#      at import time, so we must load .env before test collection begins.
load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def isolate_unit_tests_from_env(request):
    """Clear Flowise environment variables for unit tests only.

    WHY: Unit tests need isolation from .env and environment variables,
    but integration/acceptance tests need them. Using function scope ensures
    env vars are only cleared for the specific unit test, not globally.
    """
    # Check if this is a unit test
    test_path = str(request.node.fspath)
    is_unit_test = "unit" in test_path and not ("integration" in test_path or "acceptance" in test_path)

    if is_unit_test:
        # Store and clear environment variables for this unit test only
        original_env = {}
        flowise_vars = [
            "FLOWISE_API_URL",
            "FLOWISE_API_KEY",
            "FLOWISE_TIMEOUT",
            "FLOWISE_MAX_CONNECTIONS",
            "LOG_LEVEL",
        ]

        for var in flowise_vars:
            if var in os.environ:
                original_env[var] = os.environ[var]
                del os.environ[var]

        yield

        # Restore original values after this test
        for var, value in original_env.items():
            os.environ[var] = value
    else:
        # For integration/acceptance tests, don't modify environment
        yield
