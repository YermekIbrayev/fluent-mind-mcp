"""Acceptance tests for User Story 5: Generate AgentFlow V2 from Description.

Tests the complete user journey from the spec:
- AC1: Generate complete flowData structure from natural language description
- AC2: Create chatflow successfully from generated AgentFlow V2 flowData
- AC3: Handle vague/unclear descriptions with reasonable defaults

These tests verify the full stack works together (client + service + MCP tools).

WHY: User Story 5 enables AI assistants to generate complex agent workflows from
natural language, significantly lowering the technical barrier to agent creation.
This is an advanced feature that leverages Flowise's built-in generation capabilities.
"""

import json
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from fluent_mind_mcp.client.exceptions import (
    ConnectionError,
    ValidationError,
)
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig
from fluent_mind_mcp.server import MCPServer


@pytest.fixture
def mock_flowise_client_with_generation():
    """Mock FlowiseClient that simulates AgentFlow V2 generation and chatflow creation."""
    client = AsyncMock()

    # Track created chatflows
    created_chatflows = {}
    chatflow_counter = [0]

    # Mock generate_agentflow_v2 to return realistic AgentFlow V2 structure
    def generate_agentflow_v2_side_effect(description):
        """Generate mock AgentFlow V2 based on description keywords."""
        # Parse description to generate appropriate agent structure
        description_lower = description.lower()

        if "research" in description_lower and "web" in description_lower:
            flow_data = {
                "nodes": [
                    {
                        "id": "webSearch_0",
                        "type": "webSearch",
                        "data": {
                            "name": "webSearch",
                            "description": "Search the web"
                        },
                        "position": {"x": 100.0, "y": 100.0}
                    },
                    {
                        "id": "summarizer_0",
                        "type": "summarizer",
                        "data": {
                            "name": "summarizer",
                            "description": "Summarize results"
                        },
                        "position": {"x": 300.0, "y": 100.0}
                    }
                ],
                "edges": [
                    {
                        "id": "edge_0",
                        "source": "webSearch_0",
                        "target": "summarizer_0"
                    }
                ]
            }
            name = "Research Agent"
            desc = "Agent that searches web and summarizes findings"
        else:
            # Generic agent for other descriptions
            flow_data = {
                "nodes": [
                    {
                        "id": "llm_0",
                        "type": "chatOpenAI",
                        "data": {
                            "name": "llm",
                            "description": "Language model"
                        },
                        "position": {"x": 100.0, "y": 100.0}
                    }
                ],
                "edges": []
            }
            name = "AI Agent"
            desc = "General-purpose AI agent"

        return {
            "flowData": json.dumps(flow_data),
            "name": name,
            "description": desc
        }

    client.generate_agentflow_v2.side_effect = generate_agentflow_v2_side_effect

    # Mock create_chatflow to support creating from generated flowData
    def create_chatflow_side_effect(name, flow_data, type=ChatflowType.AGENTFLOW, deployed=False):
        chatflow_counter[0] += 1
        chatflow_id = f"generated-agent-{chatflow_counter[0]:03d}"
        chatflow = Chatflow(
            id=chatflow_id,
            name=name,
            type=type,
            deployed=deployed,
            flow_data=flow_data,
            created_date=datetime(2025, 10, 16, 15, 0, 0),
            updated_date=datetime(2025, 10, 16, 15, 0, 0),
        )
        created_chatflows[chatflow.id] = chatflow
        return chatflow

    client.create_chatflow.side_effect = create_chatflow_side_effect

    return client


@pytest.fixture
async def mcp_server_with_generation(mock_flowise_client_with_generation):
    """MCP Server fixture with generation-capable mocked client."""
    config = FlowiseConfig(api_url="http://localhost:3000", timeout=30)
    server = MCPServer(config=config)
    # Inject mock client
    server.client = mock_flowise_client_with_generation
    return server


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS5Scenario1GenerateAgentflowV2:
    """AC1: AI assistant generates complete flowData structure from natural language description.

    WHY: This verifies the core generation capability - transforming natural language
    into a complete AgentFlow V2 structure ready for use.
    """

    async def test_generate_from_clear_description(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        GIVEN: Natural language description "research agent that searches web and summarizes"
        WHEN: AI assistant calls generate_agentflow_v2
        THEN: Returns complete flowData with nodes and edges
        """
        result = await mcp_server_with_generation.generate_agentflow_v2(
            description="Create a research agent that searches the web and summarizes findings"
        )

        # Should return generated structure
        assert "flowData" in result
        assert "name" in result
        assert result["name"] == "Research Agent"
        assert "description" in result

        # Verify flowData is valid JSON with nodes and edges
        flow_data = json.loads(result["flowData"])
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) > 0  # Should have at least one node

        # Verify client was called correctly
        mock_flowise_client_with_generation.generate_agentflow_v2.assert_called_once()

    async def test_generated_flowdata_contains_valid_structure(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Natural language agent description
        WHEN: AI assistant generates AgentFlow V2
        THEN: flowData contains valid node structure (id, type, data, position)
        """
        result = await mcp_server_with_generation.generate_agentflow_v2(
            description="Research agent for web search"
        )

        flow_data = json.loads(result["flowData"])
        nodes = flow_data["nodes"]

        # Verify each node has required structure
        assert len(nodes) > 0
        for node in nodes:
            assert "id" in node
            assert "type" in node
            assert "data" in node
            assert "position" in node

    async def test_generated_flowdata_contains_edges(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Description requiring multi-step workflow
        WHEN: AI assistant generates AgentFlow V2
        THEN: flowData contains edges connecting nodes
        """
        result = await mcp_server_with_generation.generate_agentflow_v2(
            description="Research agent that searches web and summarizes findings"
        )

        flow_data = json.loads(result["flowData"])
        edges = flow_data["edges"]

        # Should have edges connecting nodes for multi-step workflow
        assert len(edges) > 0
        for edge in edges:
            assert "source" in edge
            assert "target" in edge

    async def test_generation_completes_within_10_seconds(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Normal Flowise generation response time
        WHEN: AI assistant calls generate_agentflow_v2
        THEN: Operation completes within 10 seconds (performance target)
        """
        import time

        start_time = time.time()
        await mcp_server_with_generation.generate_agentflow_v2(
            description="Customer support agent"
        )
        duration = time.time() - start_time

        assert duration < 10.0, f"generate_agentflow_v2 took {duration}s, expected <10s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS5Scenario2CreateChatflowFromGenerated:
    """AC2: AI assistant creates chatflow successfully from generated AgentFlow V2 flowData.

    WHY: Verifies that generated structures can be immediately used to create functional chatflows
    without manual modification.
    """

    async def test_create_chatflow_from_generated_flowdata(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        GIVEN: Generated AgentFlow V2 flowData from previous generation
        WHEN: AI assistant creates chatflow using generated flowData
        THEN: Chatflow is created successfully with unique ID
        """
        # Step 1: Generate AgentFlow V2
        generated = await mcp_server_with_generation.generate_agentflow_v2(
            description="Research agent for web search"
        )

        # Step 2: Create chatflow from generated flowData
        created = await mcp_server_with_generation.create_chatflow(
            name=generated["name"],
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW,
            deployed=False
        )

        # Should return created chatflow with ID
        assert "id" in created
        assert created["id"].startswith("generated-agent-")
        assert created["name"] == generated["name"]
        assert created["type"] == "AGENTFLOW"

        # Verify both generation and creation were called
        mock_flowise_client_with_generation.generate_agentflow_v2.assert_called()
        mock_flowise_client_with_generation.create_chatflow.assert_called()

    async def test_generated_flowdata_is_valid_for_creation(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Generated AgentFlow V2 structure
        WHEN: Using flowData to create chatflow
        THEN: No validation errors occur during creation
        """
        # Generate
        generated = await mcp_server_with_generation.generate_agentflow_v2(
            description="Customer support agent"
        )

        # Create (should not raise ValidationError)
        created = await mcp_server_with_generation.create_chatflow(
            name="Support Agent",
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW
        )

        assert created["id"] is not None

    async def test_end_to_end_generate_and_create_workflow(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        SCENARIO: Complete workflow from description to deployed chatflow
        GIVEN: User wants research agent
        WHEN: Generate AgentFlow V2 → Create chatflow → Deploy
        THEN: Each step succeeds and chatflow is ready to use
        """
        # Step 1: Generate
        generated = await mcp_server_with_generation.generate_agentflow_v2(
            description="Research agent that searches web and summarizes findings"
        )

        assert "flowData" in generated
        assert generated["name"] == "Research Agent"

        # Step 2: Create chatflow
        created = await mcp_server_with_generation.create_chatflow(
            name=generated["name"],
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW,
            deployed=True  # Deploy immediately
        )

        assert created["id"] is not None
        assert created["deployed"] is True
        assert created["type"] == "AGENTFLOW"

        # Verify full workflow was executed
        mock_flowise_client_with_generation.generate_agentflow_v2.assert_called_once()
        mock_flowise_client_with_generation.create_chatflow.assert_called_once()


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS5Scenario3VagueDescriptionHandling:
    """AC3: System handles vague or unclear descriptions with reasonable defaults.

    WHY: Not all users will provide perfect descriptions - system should handle
    vague inputs gracefully and still produce usable agent structures.
    """

    async def test_generate_from_vague_description(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Vague description with minimal details
        WHEN: AI assistant calls generate_agentflow_v2
        THEN: Returns reasonable agent structure with sensible defaults
        """
        result = await mcp_server_with_generation.generate_agentflow_v2(
            description="Create an agent that helps users"
        )

        # Should still generate something usable
        assert "flowData" in result
        assert "name" in result
        assert result["name"] is not None

        # FlowData should have basic structure
        flow_data = json.loads(result["flowData"])
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) > 0

    async def test_generate_from_minimal_description(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Very short but valid description (>=10 chars)
        WHEN: AI assistant generates AgentFlow V2
        THEN: Returns generic agent with default configuration
        """
        result = await mcp_server_with_generation.generate_agentflow_v2(
            description="simple agent"  # Exactly 12 chars
        )

        assert "flowData" in result
        assert "name" in result

        # Should create basic agent structure
        flow_data = json.loads(result["flowData"])
        assert len(flow_data["nodes"]) > 0

    async def test_vague_description_produces_usable_chatflow(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Vague description that generates basic agent
        WHEN: AI assistant creates chatflow from generated flowData
        THEN: Chatflow creation succeeds
        """
        # Generate from vague description
        generated = await mcp_server_with_generation.generate_agentflow_v2(
            description="An agent to help"
        )

        # Should still be able to create chatflow
        created = await mcp_server_with_generation.create_chatflow(
            name="Helper Agent",
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW
        )

        assert created["id"] is not None

    async def test_description_too_short_validation_error(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        GIVEN: Description shorter than 10 characters
        WHEN: AI assistant calls generate_agentflow_v2
        THEN: Returns ValidationError indicating minimum length requirement
        """
        with pytest.raises(ValidationError) as exc_info:
            await mcp_server_with_generation.generate_agentflow_v2(
                description="agent"  # Only 5 chars
            )

        error_message = str(exc_info.value).lower()
        assert "description" in error_message or "10" in error_message

        # Should not call client
        mock_flowise_client_with_generation.generate_agentflow_v2.assert_not_called()


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS5EdgeCases:
    """Additional edge cases and error scenarios for US5."""

    async def test_generate_when_flowise_unavailable(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        GIVEN: Flowise API is unreachable
        WHEN: AI assistant calls generate_agentflow_v2
        THEN: Returns ConnectionError with clear message
        """
        mock_flowise_client_with_generation.generate_agentflow_v2.side_effect = ConnectionError(
            "Cannot reach Flowise at http://localhost:3000"
        )

        with pytest.raises(ConnectionError) as exc_info:
            await mcp_server_with_generation.generate_agentflow_v2(
                description="Research agent"
            )

        error_message = str(exc_info.value).lower()
        assert any(
            keyword in error_message
            for keyword in ["connection", "reach", "unreachable", "unavailable"]
        )

    async def test_generate_with_very_long_description(
        self, mcp_server_with_generation
    ):
        """
        GIVEN: Very detailed, long description (300+ chars)
        WHEN: AI assistant generates AgentFlow V2
        THEN: Handles long input and generates appropriate structure
        """
        long_description = (
            "Create a comprehensive multi-agent research system that coordinates between "
            "multiple specialized agents: a web search agent for finding relevant information "
            "across multiple search engines, a data extraction agent for parsing and structuring "
            "the found information, a summarization agent for creating concise reports, and a "
            "validation agent for fact-checking against trusted sources before final output."
        )

        result = await mcp_server_with_generation.generate_agentflow_v2(
            description=long_description
        )

        assert "flowData" in result
        assert "name" in result

    async def test_generated_flowdata_passed_to_create_unchanged(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        GIVEN: Generated AgentFlow V2 flowData
        WHEN: Creating chatflow from it
        THEN: flowData is passed to create_chatflow without modification
        """
        # Generate
        generated = await mcp_server_with_generation.generate_agentflow_v2(
            description="Research agent"
        )

        original_flow_data = generated["flowData"]

        # Create
        await mcp_server_with_generation.create_chatflow(
            name="Test",
            flow_data=generated["flowData"]
        )

        # Verify flowData was passed unchanged
        create_call_args = mock_flowise_client_with_generation.create_chatflow.call_args
        assert create_call_args.kwargs["flow_data"] == original_flow_data


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS5SuccessCriteria:
    """Test SC-008: AI assistant can generate and create functional AgentFlow V2 in single interaction.

    WHY: This is the key success metric for US5 - the ability to go from natural language
    description to deployed agent in one seamless workflow.
    """

    async def test_sc_008_generate_and_create_in_single_interaction(
        self, mcp_server_with_generation, mock_flowise_client_with_generation
    ):
        """
        SUCCESS CRITERIA SC-008: AI assistant can generate and create functional
        AgentFlow V2 from natural language description in single interaction.

        GIVEN: User provides natural language description
        WHEN: AI assistant generates AgentFlow V2 and immediately creates chatflow
        THEN: Complete workflow succeeds without manual intervention
        """
        # Single interaction: generate + create
        description = "Create a research agent that searches the web and summarizes findings"

        # Step 1: Generate
        generated = await mcp_server_with_generation.generate_agentflow_v2(
            description=description
        )

        # Step 2: Create from generated (no manual modification)
        created = await mcp_server_with_generation.create_chatflow(
            name=generated["name"],
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW,
            deployed=True
        )

        # SUCCESS: Agent is now deployed and functional
        assert created["id"] is not None
        assert created["deployed"] is True
        assert created["name"] == "Research Agent"

        # Verify complete workflow executed
        mock_flowise_client_with_generation.generate_agentflow_v2.assert_called_once()
        mock_flowise_client_with_generation.create_chatflow.assert_called_once()
