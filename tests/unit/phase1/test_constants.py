"""Test constants for Phase 1 tests.

Centralized constants for test assertions to improve maintainability.

WHY: Replacing magic numbers with named constants improves code readability
and makes it easier to update test expectations when requirements change.
"""

# Node positioning constants
NODE_SPACING_X = 300  # Horizontal spacing between nodes in pixels
NODE_SPACING_Y = 200  # Vertical spacing between rows in pixels
INITIAL_NODE_X = 0  # Starting X position for first node
INITIAL_NODE_Y = 0  # Starting Y position for first row

# Performance requirements (from NFR-004)
MAX_RESPONSE_TIME_SECONDS = 10.0  # Maximum time for build_from_template
MAX_WORKFLOW_TIME_SECONDS = 60.0  # Maximum time for complete workflow

# Token budget requirements (from NFR-004 and SC-003, SC-005)
MAX_INVOCATION_TOKENS = 20  # Maximum tokens for tool invocation
MAX_RESPONSE_TOKENS = 30  # Maximum tokens for response
MAX_ERROR_TOKENS = 50  # Maximum tokens for error messages
MAX_WORKFLOW_TOKENS = 150  # Maximum tokens for complete workflow

# Connection inference expectations
MIN_SIMPLE_FLOW_EDGES = 2  # Minimum edges for 3-node simple flow
MIN_COMPLEX_FLOW_EDGES = 5  # Minimum edges for 6+ node complex flow
MIN_RAG_FLOW_EDGES = 7  # Minimum edges for multi-branch RAG flow

# Character to token approximation ratio
CHARS_PER_TOKEN = 4  # Approximate: 1 token ≈ 4 characters
