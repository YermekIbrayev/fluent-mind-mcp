"""Unit tests for BuildFlowService (T032 - TDD-RED Phase).

Tests for User Story 3: build_flow function.

PURPOSE: Define BuildFlowService API contract (Red phase).
All tests WILL FAIL until BuildFlowService is implemented (T035-T049).

WHY: TDD Red phase - tests define the API contract before implementation.
These tests will FAIL with ImportError/AttributeError until implementation is complete.
"""

import pytest

from fluent_mind_mcp.models.flowdata_models import BuildFlowResponse
from fluent_mind_mcp.utils.exceptions import (
    BuildFlowError,
    ConnectionInferenceError,
    TemplateNotFoundError,
    ValidationError,
)
from tests.unit.phase1.test_builders import EdgeBuilder, FlowDataBuilder, NodeBuilder
from tests.unit.phase1.test_constants import (
    CHARS_PER_TOKEN,
    MAX_ERROR_TOKENS,
    MAX_RESPONSE_TIME_SECONDS,
    MIN_COMPLEX_FLOW_EDGES,
    MIN_SIMPLE_FLOW_EDGES,
    NODE_SPACING_X,
)


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceTemplateBasic:
    """Test basic template-based chatflow creation."""

    @pytest.mark.asyncio
    async def test_build_from_template_basic(self, build_flow_service):
        """Build from valid template_id returns BuildFlowResponse.

        GIVEN: Valid template_id exists in ChromaDB
        WHEN: build_from_template("tmpl_simple_chat") is called
        THEN: Returns BuildFlowResponse with chatflow_id, name, status="success"

        WHY: Core template-based creation (SC-003: <20 token invocation).
        """
        # This will FAIL until implementation exists
        result = await build_flow_service.build_from_template("tmpl_simple_chat")

        assert isinstance(result, BuildFlowResponse)
        assert result.status == "success"
        assert result.chatflow_id is not None
        assert result.name is not None

    @pytest.mark.asyncio
    async def test_build_from_template_with_parameters(self, build_flow_service):
        """Custom parameters (model, temperature) substituted.

        GIVEN: Template with {{model}} and {{temperature}} placeholders
        WHEN: build_from_template(template_id, parameters={"model": "gpt-4", "temperature": 0.7})
        THEN: FlowData has gpt-4 and 0.7 substituted

        WHY: Template customization for different use cases.
        """
        result = await build_flow_service.build_from_template(
            "tmpl_chat",
            parameters={"model": "gpt-4", "temperature": 0.7}
        )

        assert isinstance(result, BuildFlowResponse)
        assert result.status == "success"

    @pytest.mark.asyncio
    async def test_build_from_template_invalid_id(self, build_flow_service):
        """Invalid template_id raises TemplateNotFoundError.

        GIVEN: template_id="nonexistent" does not exist
        WHEN: build_from_template("nonexistent") is called
        THEN: Raises TemplateNotFoundError with message "Template nonexistent not found"

        WHY: Clear error handling for invalid template IDs.
        """
        with pytest.raises(TemplateNotFoundError) as exc_info:
            await build_flow_service.build_from_template("nonexistent")

        assert "not found" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceCustomNodes:
    """Test custom node list creation."""

    @pytest.mark.asyncio
    async def test_build_from_nodes_basic(self, build_flow_service):
        """Build from node list with auto connections.

        GIVEN: nodes=["chatOpenAI", "bufferMemory"], connections="auto"
        WHEN: build_from_nodes(nodes, connections) is called
        THEN: Creates flowData with 2 nodes and automatic connection

        WHY: Custom chatflow creation without templates.
        """
        result = await build_flow_service.build_from_nodes(
            nodes=["chatOpenAI", "bufferMemory"],
            connections="auto"
        )

        assert isinstance(result, BuildFlowResponse)
        assert result.status == "success"

    @pytest.mark.asyncio
    async def test_build_from_nodes_invalid_name(self, build_flow_service):
        """Invalid node name raises ValidationError.

        GIVEN: nodes=["nonexistent_node"]
        WHEN: build_from_nodes(nodes) is called
        THEN: Raises ValidationError with message "Node nonexistent_node not found"

        WHY: Validates node names exist in vector DB.
        """
        with pytest.raises(ValidationError) as exc_info:
            await build_flow_service.build_from_nodes(nodes=["nonexistent_node"])

        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_build_from_nodes_empty_list(self, build_flow_service):
        """Empty nodes list raises ValidationError.

        GIVEN: nodes=[]
        WHEN: build_from_nodes(nodes) is called
        THEN: Raises ValidationError with message "Nodes list cannot be empty"

        WHY: Prevents meaningless chatflow creation.
        """
        with pytest.raises(ValidationError) as exc_info:
            await build_flow_service.build_from_nodes(nodes=[])

        assert "empty" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceTemplateRetrieval:
    """Test template retrieval and validation."""

    @pytest.mark.asyncio
    async def test_template_retrieval(self, build_flow_service):
        """_retrieve_template loads full flowData.

        GIVEN: Template exists with nodes metadata
        WHEN: _retrieve_template("tmpl_123") is called
        THEN: Returns FlowTemplate with template_id, name, nodes list

        WHY: Retrieves template from ChromaDB for building.
        """
        # Access internal method for testing
        template = await build_flow_service._retrieve_template("tmpl_123")

        assert template is not None
        assert hasattr(template, 'template_id')
        assert hasattr(template, 'nodes')

    @pytest.mark.asyncio
    async def test_parameter_substitution(self, build_flow_service):
        """_substitute_parameters replaces {{model}}, {{temperature}}.

        GIVEN: flowData with {{"model": "{{model}}", "temperature": {{temperature}}}}
        WHEN: _substitute_parameters(flowData, {"model": "gpt-4", "temperature": 0.7})
        THEN: Returns flowData with "gpt-4" and 0.7

        WHY: Template parameter customization.
        """
        node_with_params = (NodeBuilder()
                           .with_id("1")
                           .with_data({"model": "{{model}}", "temperature": "{{temperature}}"})
                           .build())
        flow_data = FlowDataBuilder().add_node(node_with_params).build()
        parameters = {"model": "gpt-4", "temperature": 0.7}

        result = build_flow_service._substitute_parameters(flow_data, parameters)

        assert result["nodes"][0]["data"]["model"] == "gpt-4"
        assert result["nodes"][0]["data"]["temperature"] == 0.7

    @pytest.mark.asyncio
    async def test_parameter_validation(self, build_flow_service):
        """Invalid parameter type raises ValidationError.

        GIVEN: parameters={"temperature": "invalid"}  # should be float
        WHEN: _substitute_parameters(flowData, parameters) is called
        THEN: Raises ValidationError with message "Invalid type for temperature"

        WHY: Type safety for template parameters.
        """
        node_with_param = (NodeBuilder()
                          .with_id("1")
                          .with_data({"temperature": "{{temperature}}"})
                          .build())
        flow_data = FlowDataBuilder().add_node(node_with_param).build()
        parameters = {"temperature": "invalid"}

        with pytest.raises(ValidationError):
            build_flow_service._substitute_parameters(flow_data, parameters)


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceConnectionInference:
    """Test automatic connection inference."""

    @pytest.mark.asyncio
    async def test_connection_inference_simple(
        self, build_flow_service, document_loader_node, chat_openai_node, conversation_chain_node
    ):
        """2-3 nodes connected correctly (Input→Processing→Output).

        GIVEN: nodes=[DocumentLoader, ChatOpenAI, ConversationChain]
        WHEN: _infer_connections(nodes) is called
        THEN: Creates edges: DocumentLoader→ChatOpenAI→ConversationChain

        WHY: Simple linear flow connection inference.
        """
        nodes = [document_loader_node, chat_openai_node, conversation_chain_node]

        edges = await build_flow_service._infer_connections(nodes)

        assert len(edges) >= MIN_SIMPLE_FLOW_EDGES
        assert all(isinstance(edge, dict) for edge in edges)

    @pytest.mark.asyncio
    async def test_connection_inference_complex(self, build_flow_service):
        """5+ nodes with memory and tools connected.

        GIVEN: nodes=[DocumentLoader, Embeddings, VectorStore, ChatOpenAI, Memory, Agent]
        WHEN: _infer_connections(nodes) is called
        THEN: Creates edges with proper RAG+memory+tools connections

        WHY: Complex multi-branch flow handling.
        """
        nodes = [
            NodeBuilder().with_id("1").with_name("documentLoader").with_base_classes(["BaseLoader"]).build(),
            NodeBuilder().with_id("2").with_name("embeddings").with_base_classes(["Embeddings"]).build(),
            NodeBuilder().with_id("3").with_name("vectorStore").with_base_classes(["VectorStore"]).build(),
            NodeBuilder().with_id("4").with_name("chatOpenAI").with_base_classes(["BaseChatModel"]).build(),
            NodeBuilder().with_id("5").with_name("memory").with_base_classes(["BaseMemory"]).build(),
            NodeBuilder().with_id("6").with_name("agent").with_base_classes(["BaseAgent"]).build(),
        ]

        edges = await build_flow_service._infer_connections(nodes)

        assert len(edges) >= MIN_COMPLEX_FLOW_EDGES

    @pytest.mark.asyncio
    async def test_connection_inference_validation(self, build_flow_service, agent_node):
        """Missing required inputs raises ConnectionInferenceError.

        GIVEN: nodes=[Agent] (missing required ChatModel input)
        WHEN: _infer_connections(nodes) is called
        THEN: Raises ConnectionInferenceError with message "Agent requires ChatModel"

        WHY: Validates all required inputs are satisfied.
        """
        nodes = [agent_node]

        with pytest.raises(ConnectionInferenceError):
            await build_flow_service._infer_connections(nodes)


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceNodePositioning:
    """Test node positioning algorithm."""

    @pytest.mark.asyncio
    async def test_node_positioning_linear(self, build_flow_service):
        """3 nodes positioned left-to-right with NODE_SPACING_X intervals.

        GIVEN: 3 nodes in sequence
        WHEN: _calculate_positions(nodes, edges) is called
        THEN: Nodes positioned with increasing x coordinates

        WHY: Readable left-to-right layout for Flowise canvas.
        """
        nodes = [
            NodeBuilder().with_id("1").build(),
            NodeBuilder().with_id("2").build(),
            NodeBuilder().with_id("3").build(),
        ]
        edges = [
            EdgeBuilder().from_node("1").to_node("2").build(),
            EdgeBuilder().from_node("2").to_node("3").build(),
        ]

        positions = build_flow_service._calculate_positions(nodes, edges)

        assert positions["1"]["x"] < positions["2"]["x"]
        assert positions["2"]["x"] < positions["3"]["x"]
        assert positions["2"]["x"] - positions["1"]["x"] == NODE_SPACING_X

    @pytest.mark.asyncio
    async def test_node_positioning_multi_row(self, build_flow_service):
        """6+ nodes use multiple rows.

        GIVEN: 6 nodes exceeding single row capacity
        WHEN: _calculate_positions(nodes, edges) is called
        THEN: Uses multiple rows with 200px vertical spacing

        WHY: Prevents horizontal overflow for large flows.
        """
        nodes = [{"id": str(i)} for i in range(1, 7)]
        edges = [{"source": str(i), "target": str(i+1)} for i in range(1, 6)]

        positions = build_flow_service._calculate_positions(nodes, edges)

        # Check that some nodes have different y positions
        y_positions = [pos["y"] for pos in positions.values()]
        assert len(set(y_positions)) > 1  # Multiple rows


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceValidation:
    """Test flowData validation."""

    @pytest.mark.asyncio
    async def test_flowdata_validation(self, build_flow_service):
        """_validate_flowData catches missing nodes/edges/invalid refs.

        GIVEN: flowData with edge referencing non-existent node ID
        WHEN: _validate_flowData(flowData) is called
        THEN: Raises BuildFlowError with message "Edge references unknown node"

        WHY: Pre-submission validation prevents Flowise API errors.
        """
        node = NodeBuilder().with_id("1").build()
        invalid_edge = EdgeBuilder().from_node("1").to_node("999").build()
        flow_data = FlowDataBuilder().add_node(node).add_edge(invalid_edge).build()

        with pytest.raises(BuildFlowError):
            build_flow_service._validate_flowData(flow_data)


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestBuildFlowServiceResponseFormat:
    """Test compact response format."""

    @pytest.mark.asyncio
    async def test_compact_response_format(self, build_flow_service):
        """BuildFlowResponse <30 tokens (chatflow_id, name, status).

        GIVEN: Successful chatflow creation
        WHEN: build_from_template() returns response
        THEN: Response has only: chatflow_id, name, status (excludes flowData)

        WHY: Meets NFR-004 token budget (<30 tokens response).
        """
        result = await build_flow_service.build_from_template("tmpl_simple_chat")

        # Check only required fields present
        result_dict = result.model_dump() if hasattr(result, 'model_dump') else result.__dict__
        assert "chatflow_id" in result_dict
        assert "name" in result_dict
        assert "status" in result_dict
        # flowData should NOT be in response
        assert "flowData" not in result_dict

    @pytest.mark.asyncio
    async def test_error_response_format(self, build_flow_service):
        """Error responses within MAX_ERROR_TOKENS with recovery guidance.

        GIVEN: Template not found error
        WHEN: build_from_template("invalid") fails
        THEN: Error response within token budget with actionable message

        WHY: Actionable error messages within token budget.
        """
        with pytest.raises(TemplateNotFoundError) as exc_info:
            await build_flow_service.build_from_template("invalid")

        error_msg = str(exc_info.value)
        estimated_tokens = len(error_msg) / CHARS_PER_TOKEN
        assert estimated_tokens < MAX_ERROR_TOKENS


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
@pytest.mark.performance
class TestBuildFlowServicePerformance:
    """Test performance requirements."""

    @pytest.mark.asyncio
    async def test_performance_template(self, build_flow_service):
        """Build from template within MAX_RESPONSE_TIME_SECONDS (per NFR-004).

        GIVEN: Standard template with 5 nodes
        WHEN: build_from_template() is called
        THEN: Completes within performance target

        WHY: Meets NFR-004 performance target.
        """
        import time

        start = time.time()
        await build_flow_service.build_from_template("tmpl_simple_chat")
        duration = time.time() - start

        assert duration < MAX_RESPONSE_TIME_SECONDS, \
            f"Should complete in <{MAX_RESPONSE_TIME_SECONDS}s, took {duration:.2f}s"
