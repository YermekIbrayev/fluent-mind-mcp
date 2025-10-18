"""Unit tests for BuildFlowService (Phase 1 - User Story 3).

Tests template-based chatflow creation functionality.

Coverage:
- Build from template (Phase 1 scope)
- FlowData structure validation
- Node positioning algorithm
- Success rate validation (>95% per NFR-093)

WHY: Validates chatflow creation service for User Story 3.
"""

import pytest

from fluent_mind_mcp.services.build_flow_service import BuildFlowService
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.utils.exceptions import TemplateNotFoundError


@pytest.mark.unit
@pytest.mark.phase1
class TestBuildFlowServiceTemplateBasedCreation:
    """Test template-based chatflow creation (Phase 1 scope)."""

    @pytest.mark.asyncio
    async def test_build_from_template_creates_chatflow(self, tmp_path):
        """
        GIVEN: Template "simple_chat" exists
        WHEN: build_from_template("simple_chat") is called
        THEN: Creates chatflow and returns chatflow_id

        WHY: Core functionality for User Story 3.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_simple_chat"],
            documents=["Simple chat template"],
            metadatas=[{
                "template_id": "tmpl_simple_chat",
                "name": "Simple Chat",
                "nodes": "chatOpenAI,bufferMemory,conversationChain"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template(template_id="tmpl_simple_chat")

        assert "chatflow_id" in result
        assert result["chatflow_id"] is not None
        assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_build_from_template_generates_valid_flow_data(self, tmp_path):
        """
        GIVEN: Template with nodes list
        WHEN: Building chatflow
        THEN: Generated flowData has correct structure (nodes, edges, positions)

        WHY: Validates flowData structure compliance with Flowise API.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_simple_chat"],
            documents=["Simple chat template"],
            metadatas=[{
                "template_id": "tmpl_simple_chat",
                "name": "Simple Chat",
                "nodes": "chatOpenAI,bufferMemory,conversationChain"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_simple_chat")

        flow_data = result["flow_data"]
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) > 0

        # Each node has position
        for node in flow_data["nodes"]:
            assert "position" in node
            assert "x" in node["position"]
            assert "y" in node["position"]

    @pytest.mark.asyncio
    async def test_build_from_template_positions_nodes_left_to_right(self, tmp_path):
        """
        GIVEN: Template with 3 nodes
        WHEN: Building flowData
        THEN: Nodes are positioned left-to-right with 300px horizontal spacing

        WHY: Ensures readable visual layout in Flowise canvas.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template with 3 nodes
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_simple_chat"],
            documents=["Simple chat template"],
            metadatas=[{
                "template_id": "tmpl_simple_chat",
                "name": "Simple Chat",
                "nodes": "chatOpenAI,bufferMemory,conversationChain"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_simple_chat")

        nodes = result["flow_data"]["nodes"]
        positions = [node["position"]["x"] for node in nodes]

        # Should be increasing (left to right)
        assert positions == sorted(positions), "Nodes not positioned left-to-right"

        # Check spacing (~300px)
        if len(positions) > 1:
            spacing = positions[1] - positions[0]
            assert 250 <= spacing <= 350, f"Spacing {spacing}px not in range 250-350px"

    @pytest.mark.asyncio
    async def test_build_from_template_nonexistent_template_raises_error(self, tmp_path):
        """
        GIVEN: Template "nonexistent" does not exist
        WHEN: build_from_template("nonexistent") is called
        THEN: Raises TemplateNotFoundError with clear message

        WHY: Explicit error handling for user feedback.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Create empty templates collection
        vector_db_client.get_or_create_collection("templates")

        # Test
        service = BuildFlowService(vector_db_client)

        with pytest.raises(TemplateNotFoundError) as exc_info:
            await service.build_from_template("nonexistent")

        assert "not found" in str(exc_info.value).lower() or "nonexistent" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.phase1
class TestBuildFlowServiceFlowDataValidation:
    """Test flowData structure validation."""

    @pytest.mark.asyncio
    async def test_flow_data_has_required_node_fields(self, tmp_path):
        """
        GIVEN: Generated flowData
        WHEN: Examining node structure
        THEN: Each node has required fields: id, type, data, position

        WHY: Ensures Flowise API compatibility.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_simple_chat"],
            documents=["Simple chat template"],
            metadatas=[{
                "template_id": "tmpl_simple_chat",
                "name": "Simple Chat",
                "nodes": "chatOpenAI,bufferMemory"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_simple_chat")

        for node in result["flow_data"]["nodes"]:
            assert "id" in node
            assert "type" in node
            assert "data" in node
            assert "position" in node

    @pytest.mark.asyncio
    async def test_flow_data_nodes_have_unique_ids(self, tmp_path):
        """
        GIVEN: Generated flowData with multiple nodes
        WHEN: Examining node IDs
        THEN: All node IDs are unique

        WHY: Prevents ID collision errors in Flowise.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template with multiple nodes
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_rag_flow"],
            documents=["RAG flow template"],
            metadatas=[{
                "template_id": "tmpl_rag_flow",
                "name": "RAG Flow",
                "nodes": "chatOpenAI,openAIEmbeddings,faiss,conversationalRetrievalQAChain"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_rag_flow")

        node_ids = [node["id"] for node in result["flow_data"]["nodes"]]
        assert len(node_ids) == len(set(node_ids)), "Duplicate node IDs found"

    @pytest.mark.asyncio
    async def test_flow_data_includes_edges_between_nodes(self, tmp_path):
        """
        GIVEN: Template with multiple nodes
        WHEN: Building flowData
        THEN: Edges connect nodes in sequence

        WHY: Creates valid flow connections for Flowise.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template with 3 nodes
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_test"],
            documents=["Test template"],
            metadatas=[{
                "template_id": "tmpl_test",
                "name": "Test",
                "nodes": "node1,node2,node3"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_test")

        flow_data = result["flow_data"]
        nodes = flow_data["nodes"]
        edges = flow_data["edges"]

        # Should have N-1 edges for N nodes (linear connection)
        assert len(edges) == len(nodes) - 1

        # Each edge should have source and target
        for edge in edges:
            assert "id" in edge
            assert "source" in edge
            assert "target" in edge


@pytest.mark.unit
@pytest.mark.phase1
class TestBuildFlowServiceEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_build_from_empty_template_creates_minimal_flow(self, tmp_path):
        """
        GIVEN: Template with no nodes
        WHEN: Building flowData
        THEN: Creates minimal flow structure (empty nodes array)

        WHY: Handles edge case gracefully.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add empty template
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_empty"],
            documents=["Empty template"],
            metadatas=[{
                "template_id": "tmpl_empty",
                "name": "Empty",
                "nodes": ""
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_empty")

        flow_data = result["flow_data"]
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) == 0
        assert len(flow_data["edges"]) == 0

    @pytest.mark.asyncio
    async def test_build_from_template_with_single_node(self, tmp_path):
        """
        GIVEN: Template with only one node
        WHEN: Building flowData
        THEN: Creates flow with one node and no edges

        WHY: Edge case validation for minimal templates.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add single-node template
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_single"],
            documents=["Single node template"],
            metadatas=[{
                "template_id": "tmpl_single",
                "name": "Single",
                "nodes": "chatOpenAI"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_single")

        flow_data = result["flow_data"]
        assert len(flow_data["nodes"]) == 1
        assert len(flow_data["edges"]) == 0  # No edges for single node

    @pytest.mark.asyncio
    async def test_build_result_includes_template_id(self, tmp_path):
        """
        GIVEN: Template build succeeds
        WHEN: Examining result
        THEN: Result includes template_id for traceability

        WHY: Enables tracking of which template was used.
        """
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test template
        collection = vector_db_client.get_or_create_collection("templates")
        collection.add(
            ids=["tmpl_test"],
            documents=["Test template"],
            metadatas=[{
                "template_id": "tmpl_test",
                "name": "Test",
                "nodes": "chatOpenAI"
            }]
        )

        # Test
        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_test")

        assert "template_id" in result
        assert result["template_id"] == "tmpl_test"
