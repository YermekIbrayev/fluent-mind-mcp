"""Pytest configuration for test suite.

This module configures the test environment:
- Unit tests: Isolated from .env file and environment variables
- Integration/Acceptance tests: Load .env file for real Flowise connection
- Phase 1 tests: ChromaDB and embedding fixtures
"""

import os
import sys
import tempfile
import pytest
from dotenv import load_dotenv
from pathlib import Path

# Load .env file at module import time to ensure it's available for module-level skipif checks
# WHY: Integration/acceptance tests use module-level skipif that checks FLOWISE_API_URL
#      at import time, so we must load .env before test collection begins.
load_dotenv()

# Add tests/utilities to path for imports
sys.path.insert(0, str(Path(__file__).parent / "utilities"))


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


# ============================================================================
# Phase 1 Test Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def chromadb_helper():
    """Provide ChromaDB test utilities with automatic cleanup.

    WHY: Simplifies Phase 1 test setup and ensures proper cleanup.
    """
    from chromadb_helpers import ChromaDBTestUtilities

    helper = ChromaDBTestUtilities()
    yield helper
    helper.cleanup()


@pytest.fixture(scope="function")
def test_data_generator():
    """Provide test data generator for Phase 1 tests.

    WHY: Centralizes test data generation for consistency.
    """
    from test_data_generator import TestDataGenerator

    return TestDataGenerator()


@pytest.fixture(scope="function")
def populated_chromadb(chromadb_helper, test_data_generator):
    """Provide ChromaDB pre-populated with test data.

    WHY: Common setup for vector search tests.
    """
    # Reset and create collections
    chromadb_helper.reset_all_collections(["nodes", "templates"])
    chromadb_helper.create_all_collections(["nodes", "templates"])

    # Generate and populate test data
    nodes = test_data_generator.generate_node_descriptions(count=20)
    templates = test_data_generator.generate_flow_templates(count=10)

    node_dicts = [
        {
            "name": node.node_name,
            "label": node.label,
            "description": node.description,
            "category": node.category,
            "version": node.version
        }
        for node in nodes
    ]

    template_dicts = [
        {
            "template_id": template.template_id,
            "name": template.name,
            "description": template.description,
            "nodes": ",".join(template.required_nodes)
        }
        for template in templates
    ]

    chromadb_helper.populate_nodes(node_dicts)
    chromadb_helper.populate_templates(template_dicts)

    yield chromadb_helper


@pytest.fixture(scope="session")
def test_db_path():
    """Provide temporary database path for testing.

    WHY: Isolates test database from production data.
    """
    temp_dir = tempfile.mkdtemp(prefix="chromadb_test_phase1_")
    yield temp_dir
    # Cleanup handled by chromadb_helper fixture
