"""Unit tests for Connection Inference Algorithm (T033 - TDD-RED Phase).

Tests for automatic node connection logic in User Story 3.

PURPOSE: Comprehensive testing of connection inference algorithm.
All tests WILL FAIL until connection inference is implemented (T038-T042).

WHY: TDD Red phase - defines connection algorithm contract before implementation.
These tests will FAIL with ImportError/AttributeError until implementation is complete.
"""

import pytest

from fluent_mind_mcp.utils.exceptions import ConnectionInferenceError
from tests.unit.phase1.test_builders import NodeBuilder
from tests.unit.phase1.test_constants import MIN_RAG_FLOW_EDGES


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestNodeCategorization:
    """Test node categorization by type."""

    @pytest.mark.asyncio
    async def test_categorize_nodes_input(self, build_flow_service):
        """Document loaders categorized as Input.

        GIVEN: nodes=[{name: "textFile", base_classes: ["Document", "BaseLoader"]}]
        WHEN: _categorize_nodes(nodes) is called
        THEN: Returns {"Input": [textFile node]}

        WHY: Input nodes are entry points for data.
        """
        text_file_node = (NodeBuilder()
                         .with_name("textFile")
                         .with_base_classes(["Document", "BaseLoader"])
                         .build())

        result = build_flow_service._categorize_nodes([text_file_node])

        assert "Input" in result
        assert len(result["Input"]) == 1
        assert result["Input"][0]["name"] == "textFile"

    @pytest.mark.asyncio
    async def test_categorize_nodes_processing(self, build_flow_service, chat_openai_node):
        """Chat models, LLMs categorized as Processing.

        GIVEN: nodes=[{name: "chatOpenAI", base_classes: ["BaseChatModel", "BaseLanguageModel"]}]
        WHEN: _categorize_nodes(nodes) is called
        THEN: Returns {"Processing": [chatOpenAI node]}

        WHY: Processing nodes transform/generate content.
        """
        result = build_flow_service._categorize_nodes([chat_openai_node])

        assert "Processing" in result
        assert len(result["Processing"]) == 1
        assert result["Processing"][0]["name"] == "chatOpenAI"

    @pytest.mark.asyncio
    async def test_categorize_nodes_memory(self, build_flow_service, buffer_memory_node):
        """Memory nodes categorized correctly.

        GIVEN: nodes=[{name: "bufferMemory", base_classes: ["BaseMemory"]}]
        WHEN: _categorize_nodes(nodes) is called
        THEN: Returns {"Memory": [bufferMemory node]}

        WHY: Memory nodes store conversation history.
        """
        result = build_flow_service._categorize_nodes([buffer_memory_node])

        assert "Memory" in result
        assert len(result["Memory"]) == 1
        assert result["Memory"][0]["name"] == "bufferMemory"

    @pytest.mark.asyncio
    async def test_categorize_nodes_tools(self, build_flow_service):
        """Tools categorized correctly.

        GIVEN: nodes=[{name: "calculator", base_classes: ["Tool", "BaseTool"]}]
        WHEN: _categorize_nodes(nodes) is called
        THEN: Returns {"Tools": [calculator node]}

        WHY: Tools provide external functionality to agents.
        """
        calculator_node = (NodeBuilder()
                          .with_name("calculator")
                          .with_base_classes(["Tool", "BaseTool"])
                          .build())

        result = build_flow_service._categorize_nodes([calculator_node])

        assert "Tools" in result
        assert len(result["Tools"]) == 1
        assert result["Tools"][0]["name"] == "calculator"

    @pytest.mark.asyncio
    async def test_categorize_nodes_output(self, build_flow_service, conversation_chain_node):
        """Chains, agents categorized as Output.

        GIVEN: nodes=[{name: "conversationChain", base_classes: ["BaseChain"]}]
        WHEN: _categorize_nodes(nodes) is called
        THEN: Returns {"Output": [conversationChain node]}

        WHY: Output nodes orchestrate final response generation.
        """
        result = build_flow_service._categorize_nodes([conversation_chain_node])

        assert "Output" in result
        assert len(result["Output"]) == 1
        assert result["Output"][0]["name"] == "conversationChain"


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestTopologicalOrdering:
    """Test topological sorting of nodes."""

    @pytest.mark.asyncio
    async def test_topological_ordering(self, build_flow_service):
        """Nodes sorted Input→Tools→Processing→Memory→Output.

        GIVEN: categorized_nodes with all node types
        WHEN: _topological_sort(categorized_nodes) is called
        THEN: Returns nodes ordered by category

        WHY: Ensures correct execution flow in chatflow.
        """
        categorized_nodes = {
            "Input": [NodeBuilder().with_name("loader").build()],
            "Tools": [NodeBuilder().with_name("tool").build()],
            "Processing": [NodeBuilder().with_name("llm").build()],
            "Memory": [NodeBuilder().with_name("memory").build()],
            "Output": [NodeBuilder().with_name("chain").build()],
        }

        result = build_flow_service._topological_sort(categorized_nodes)

        names = [node["name"] for node in result]
        assert names.index("loader") < names.index("tool")
        assert names.index("tool") < names.index("llm")
        assert names.index("llm") < names.index("memory")
        assert names.index("memory") < names.index("chain")


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestTypeCompatibleChaining:
    """Test type-compatible node chaining."""

    @pytest.mark.asyncio
    async def test_type_compatible_chaining(self, build_flow_service):
        """BaseClass matching (output→input compatibility).

        GIVEN: nodes with compatible input/output types
        WHEN: _match_base_classes(nodes) is called
        THEN: Returns compatible node pairs

        WHY: Ensures type-safe connections between nodes.
        """
        chat_model = (NodeBuilder()
                     .with_name("chatOpenAI")
                     .with_outputs(["BaseChatModel"])
                     .with_inputs([])
                     .build())
        agent = (NodeBuilder()
                .with_name("agent")
                .with_outputs([])
                .with_inputs(["BaseChatModel"])
                .build())
        nodes = [chat_model, agent]

        result = build_flow_service._match_base_classes(nodes)

        assert len(result) >= 1
        pair_names = [(pair[0]["name"], pair[1]["name"]) for pair in result]
        assert ("chatOpenAI", "agent") in pair_names


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestConnectionValidation:
    """Test connection validation and edge generation."""

    @pytest.mark.asyncio
    async def test_required_inputs_validation(self, build_flow_service, agent_node):
        """All required inputs satisfied (raise ConnectionInferenceError if not).

        GIVEN: No connections, but agent requires BaseChatModel input
        WHEN: _generate_edges(node_pairs, [node]) is called
        THEN: Raises ConnectionInferenceError indicating missing required input

        WHY: Validates chatflow has all required connections.
        """
        node_pairs = []

        with pytest.raises(ConnectionInferenceError) as exc_info:
            build_flow_service._generate_edges(node_pairs, [agent_node])

        error_msg = str(exc_info.value).lower()
        assert "missing" in error_msg or "required" in error_msg

    @pytest.mark.asyncio
    async def test_edge_generation(self, build_flow_service):
        """Correct source/target node IDs and handles.

        GIVEN: Pair of connected nodes
        WHEN: _generate_edges(node_pairs) is called
        THEN: Returns valid edge with source, target, and handles

        WHY: Creates valid edge objects for Flowise flowData.
        """
        node1 = NodeBuilder().with_id("node1_id").with_name("chatOpenAI").build()
        node2 = NodeBuilder().with_id("node2_id").with_name("agent").build()
        node_pairs = [(node1, node2)]

        result = build_flow_service._generate_edges(node_pairs, [])

        assert len(result) >= 1
        edge = result[0]
        assert edge["source"] == "node1_id"
        assert edge["target"] == "node2_id"
        assert "sourceHandle" in edge
        assert "targetHandle" in edge

    @pytest.mark.asyncio
    async def test_circular_dependency_detection(self, build_flow_service):
        """Detect and reject circular connections.

        GIVEN: Node pairs forming a circular dependency
        WHEN: _generate_edges(node_pairs) is called
        THEN: Raises ConnectionInferenceError about circular dependency

        WHY: Prevents infinite loops in chatflow execution.
        """
        node1 = NodeBuilder().with_id("1").with_name("node1").build()
        node2 = NodeBuilder().with_id("2").with_name("node2").build()
        node3 = NodeBuilder().with_id("3").with_name("node3").build()
        node_pairs = [(node1, node2), (node2, node3), (node3, node1)]

        with pytest.raises(ConnectionInferenceError) as exc_info:
            build_flow_service._generate_edges(node_pairs, [])

        assert "circular" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.phase1
@pytest.mark.us3
class TestComplexFlowInference:
    """Test complex multi-branch flows."""

    @pytest.mark.asyncio
    async def test_disconnected_nodes_detection(self, build_flow_service):
        """Warn about nodes with no connections.

        GIVEN: nodes=[isolated_node, connected_node1, connected_node2]
        WHEN: _infer_connections(nodes) is called
        THEN: Logs warning "Node isolated_node has no connections" but does not fail

        WHY: Alerts user to potentially missing connections without blocking.
        """
        nodes = [
            {"id": "1", "name": "isolated_node", "base_classes": ["BaseLoader"]},
            {"id": "2", "name": "connected_node1", "base_classes": ["BaseChatModel"]},
            {"id": "3", "name": "connected_node2", "base_classes": ["BaseChain"]}
        ]

        # Should not raise, but may log warnings
        result = await build_flow_service._infer_connections(nodes)

        assert isinstance(result, list)  # Should return edges list

    @pytest.mark.asyncio
    async def test_complex_flow_inference(self, build_flow_service):
        """Multi-branch flows (e.g., RAG with multiple retrievers).

        GIVEN: Complex RAG flow with multiple data sources
        WHEN: _infer_connections(nodes) is called
        THEN: Creates appropriate multi-branch connections

        WHY: Handles complex multi-source RAG patterns.
        """
        nodes = [
            NodeBuilder().with_id("1").with_name("loader").with_base_classes(["BaseLoader"]).build(),
            NodeBuilder().with_id("2").with_name("embeddings").with_base_classes(["Embeddings"]).build(),
            NodeBuilder().with_id("3").with_name("vectorStore1").with_base_classes(["VectorStore"]).build(),
            NodeBuilder().with_id("4").with_name("vectorStore2").with_base_classes(["VectorStore"]).build(),
            NodeBuilder().with_id("5").with_name("llm").with_base_classes(["BaseChatModel"]).build(),
            NodeBuilder().with_id("6").with_name("retriever1").with_base_classes(["BaseRetriever"]).build(),
            NodeBuilder().with_id("7").with_name("retriever2").with_base_classes(["BaseRetriever"]).build(),
            NodeBuilder().with_id("8").with_name("qaChain").with_base_classes(["BaseChain"]).build(),
        ]

        result = await build_flow_service._infer_connections(nodes)

        assert len(result) >= MIN_RAG_FLOW_EDGES
        assert all(isinstance(edge, dict) for edge in result)
        assert all("source" in edge and "target" in edge for edge in result)
