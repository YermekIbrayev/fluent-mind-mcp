"""Test data generator for Phase 1 functional tests.

Generates realistic sample data for:
- Node descriptions (20+ variations)
- Flow templates (10+ patterns)
- Embedding vectors

WHY: Provides consistent, diverse test data for vector search validation.
"""

import random
from typing import List

from fluent_mind_mcp.models.node_models import NodeMetadata
from fluent_mind_mcp.models.template_models import FlowTemplate, TemplateMetadata


class TestDataGenerator:
    """Generate realistic test data for Phase 1 testing."""

    # Semantic categories for diverse node generation
    CATEGORIES = [
        "Chat Models",
        "Memory",
        "Tools",
        "Chains",
        "Agents",
        "Retrievers",
        "Document Loaders",
        "Vector Stores",
        "Text Splitters",
        "Embeddings"
    ]

    NODE_TEMPLATES = [
        # Chat Models
        {
            "name": "chatOpenAI",
            "label": "ChatOpenAI",
            "description": "OpenAI chat model for conversational AI and question answering",
            "category": "Chat Models",
            "base_classes": ["BaseChatModel", "BaseLLM"]
        },
        {
            "name": "chatAnthropic",
            "label": "ChatAnthropic",
            "description": "Anthropic Claude chat model for advanced reasoning and conversation",
            "category": "Chat Models",
            "base_classes": ["BaseChatModel", "BaseLLM"]
        },
        # Memory
        {
            "name": "bufferMemory",
            "label": "Buffer Memory",
            "description": "Stores conversation history in a buffer for context retention",
            "category": "Memory",
            "base_classes": ["BaseMemory"]
        },
        {
            "name": "bufferWindowMemory",
            "label": "Buffer Window Memory",
            "description": "Stores recent conversation messages in a sliding window",
            "category": "Memory",
            "base_classes": ["BaseMemory"]
        },
        # Chains
        {
            "name": "conversationChain",
            "label": "Conversation Chain",
            "description": "Chain for conversational AI with memory and context",
            "category": "Chains",
            "base_classes": ["BaseChain"]
        },
        {
            "name": "conversationalRetrievalQAChain",
            "label": "Conversational Retrieval QA Chain",
            "description": "QA chain with document retrieval and conversation memory",
            "category": "Chains",
            "base_classes": ["BaseChain", "BaseRetrievalQA"]
        },
        # Tools & Agents
        {
            "name": "toolAgent",
            "label": "Tool Agent",
            "description": "Agent that uses tools to accomplish tasks",
            "category": "Agents",
            "base_classes": ["BaseAgent"]
        },
        {
            "name": "retrieverTool",
            "label": "Retriever Tool",
            "description": "Tool for retrieving relevant documents from vector stores",
            "category": "Tools",
            "base_classes": ["BaseTool"]
        },
        # Vector Stores
        {
            "name": "faiss",
            "label": "FAISS Vector Store",
            "description": "Facebook AI Similarity Search vector database for embeddings",
            "category": "Vector Stores",
            "base_classes": ["BaseVectorStore"]
        },
        {
            "name": "memoryVectorStore",
            "label": "In-Memory Vector Store",
            "description": "In-memory vector store for fast retrieval during development",
            "category": "Vector Stores",
            "base_classes": ["BaseVectorStore"]
        },
        # Document Loaders
        {
            "name": "cheerioWebScraper",
            "label": "Cheerio Web Scraper",
            "description": "Scrapes web pages and extracts text content",
            "category": "Document Loaders",
            "base_classes": ["BaseDocumentLoader"]
        },
        {
            "name": "readFile",
            "label": "Read File",
            "description": "Reads text content from local files",
            "category": "Document Loaders",
            "base_classes": ["BaseDocumentLoader"]
        },
        # Embeddings
        {
            "name": "openAIEmbeddings",
            "label": "OpenAI Embeddings",
            "description": "OpenAI embedding model for text vectorization",
            "category": "Embeddings",
            "base_classes": ["BaseEmbeddings"]
        },
        # Text Splitters
        {
            "name": "htmlToMarkdownTextSplitter",
            "label": "HTML to Markdown Text Splitter",
            "description": "Converts HTML to markdown and splits into chunks",
            "category": "Text Splitters",
            "base_classes": ["BaseTextSplitter"]
        },
    ]

    TEMPLATE_PATTERNS = [
        {
            "template_id": "tmpl_simple_chat",
            "name": "Simple Chat",
            "description": "Basic chatbot with conversational memory",
            "tags": ["chatbot", "conversation", "memory"],
            "nodes": ["chatOpenAI", "bufferMemory", "conversationChain"]
        },
        {
            "template_id": "tmpl_rag_flow",
            "name": "RAG Assistant",
            "description": "Retrieval-augmented generation for document QA",
            "tags": ["rag", "qa", "documents", "retrieval"],
            "nodes": ["chatOpenAI", "openAIEmbeddings", "faiss", "conversationalRetrievalQAChain"]
        },
        {
            "template_id": "tmpl_agent_with_tools",
            "name": "Agent with Tools",
            "description": "Agent that can use multiple tools to solve tasks",
            "tags": ["agent", "tools", "autonomous"],
            "nodes": ["chatOpenAI", "toolAgent", "retrieverTool"]
        },
    ]

    @classmethod
    def generate_node_descriptions(cls, count: int = 20) -> List[NodeMetadata]:
        """Generate diverse node metadata for testing.

        Args:
            count: Number of nodes to generate (default 20)

        Returns:
            List of NodeMetadata objects with semantic diversity

        WHY: Provides realistic node data for vector search accuracy testing.
        """
        nodes = []

        # Add all predefined templates
        for template in cls.NODE_TEMPLATES:
            nodes.append(NodeMetadata(
                node_name=template["name"],
                label=template["label"],
                version="1.0.0",
                category=template["category"],
                base_classes=template["base_classes"],
                description=template["description"],
                deprecated=False
            ))

        # Generate additional random nodes if needed
        for i in range(max(0, count - len(nodes))):
            category = random.choice(cls.CATEGORIES)
            nodes.append(NodeMetadata(
                node_name=f"testNode_{i}",
                label=f"Test Node {i}",
                version="1.0.0",
                category=category,
                base_classes=[f"Base{category.replace(' ', '')}"],
                description=f"Test node for {category.lower()} functionality",
                deprecated=False
            ))

        return nodes[:count]

    @classmethod
    def generate_flow_templates(cls, count: int = 10) -> List[FlowTemplate]:
        """Generate flow templates with various complexity levels.

        Args:
            count: Number of templates to generate (default 10)

        Returns:
            List of FlowTemplate objects

        WHY: Provides template data for build_flow service testing.
        """
        templates = []

        for i, pattern in enumerate(cls.TEMPLATE_PATTERNS):
            # Create minimal flowData structure
            flow_data = {
                "nodes": [
                    {
                        "id": f"{node}_{j}",
                        "type": node,
                        "data": {"name": node},
                        "position": {"x": 100 + j * 300, "y": 100}
                    }
                    for j, node in enumerate(pattern["nodes"])
                ],
                "edges": []
            }

            templates.append(FlowTemplate(
                template_id=pattern["template_id"],
                name=pattern["name"],
                description=pattern["description"],
                tags=pattern["tags"],
                flow_data=flow_data,
                metadata=TemplateMetadata(
                    template_id=pattern["template_id"],
                    name=pattern["name"],
                    description=pattern["description"],
                    required_nodes=pattern["nodes"],
                    parameter_count=len(pattern["nodes"])
                )
            ))

        # Generate additional simple templates if needed
        for i in range(max(0, count - len(templates))):
            template_id = f"tmpl_test_{i}"
            templates.append(FlowTemplate(
                template_id=template_id,
                name=f"Test Template {i}",
                description=f"Test template for validation {i}",
                tags=["test"],
                flow_data={"nodes": [], "edges": []},
                metadata=TemplateMetadata(
                    template_id=template_id,
                    name=f"Test Template {i}",
                    description=f"Test template for validation {i}",
                    required_nodes=[],
                    parameter_count=0
                )
            ))

        return templates[:count]

    @classmethod
    def get_test_queries(cls) -> List[tuple[str, List[str]]]:
        """Get test queries with expected node matches.

        Returns:
            List of (query, expected_nodes) tuples for validation

        WHY: Provides ground truth for vector search accuracy testing.
        """
        return [
            ("chatbot that remembers conversation", ["chatOpenAI", "bufferMemory", "conversationChain"]),
            ("search documents using embeddings", ["openAIEmbeddings", "faiss", "conversationalRetrievalQAChain"]),
            ("AI agent with tools", ["toolAgent", "retrieverTool", "chatOpenAI"]),
            ("scrape web pages", ["cheerioWebScraper", "readFile"]),
            ("chat model for conversation", ["chatOpenAI", "chatAnthropic", "conversationChain"]),
        ]

    @classmethod
    def get_template_queries(cls) -> List[tuple[str, List[str]]]:
        """Get template search queries with expected matches.

        Returns:
            List of (query, expected_template_ids) tuples

        WHY: Validates template search functionality.
        """
        return [
            ("simple chatbot", ["tmpl_simple_chat"]),
            ("document question answering", ["tmpl_rag_flow"]),
            ("agent with tools", ["tmpl_agent_with_tools"]),
            ("conversational AI", ["tmpl_simple_chat", "tmpl_rag_flow"]),
        ]
