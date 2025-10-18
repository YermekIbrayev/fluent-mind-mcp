# Common Nodes - Overview

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

Quick reference to commonly used node types. Full specifications in category files.

## Documentation Split

Node documentation is organized by category:

1. **[03-nodes-llm.md](03-nodes-llm.md)** - Chat Models & Prompts
2. **[04-nodes-agents.md](04-nodes-agents.md)** - Memory, Chains, Agents, Tools
3. **[05-nodes-rag.md](05-nodes-rag.md)** - Document Loaders, Splitters, Embeddings, Vector Stores

## Node Categories

### Chat Models
- **ChatOpenAI**: GPT-4o, GPT-4o-mini, GPT-3.5-turbo
- **ChatAnthropic**: Claude 3.5 Sonnet
- **AzureChatOpenAI**: Azure OpenAI models
- **ChatOllama**: Local models

### Prompts
- **PromptTemplate**: Basic prompt with variables
- **ChatPromptTemplate**: System + human messages

### Memory
- **BufferMemory**: Simple conversation memory
- **ConversationSummaryMemory**: Summarized history

### Chains
- **LLMChain**: Model + Prompt → Output
- **ConversationChain**: Model + Memory → Conversation

### Agents
- **ConversationalAgent**: Agent with tools and memory

### Tools
- **Calculator**: Math operations
- **SerpAPI**: Google search
- **WebBrowser**: Web scraping

### Document Loaders
- **TextFile**: Load .txt files
- **PDFLoader**: Load PDF documents

### Text Splitters
- **RecursiveCharacterTextSplitter**: Smart chunking

### Embeddings
- **OpenAIEmbeddings**: text-embedding-3-small/large
- **HuggingFaceInferenceEmbeddings**: Open source models

### Vector Stores
- **Pinecone**: Cloud vector database
- **Chroma**: Local/cloud vector database
- **InMemoryVectorStore**: In-memory storage

### Retrievers
- **VectorStoreRetriever**: Query vector stores

## Node Structure Quick Reference

```javascript
{
  "id": "nodeName_0",
  "data": {
    "id": "nodeName_0",
    "name": "nodeName",
    "inputs": {
      // Direct values or {{nodeRef.data.instance}}
    },
    "baseClasses": ["PrimaryType", "BaseType", "..."]
  }
}
```

## Common Patterns

### Chat Model Setup
```javascript
{
  "name": "chatOpenAI",
  "inputs": { "modelName": "gpt-4o-mini", "temperature": 0.7 }
}
```

### Node References
```javascript
{
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}"
  }
}
```

### Tool Arrays
```javascript
{
  "inputs": {
    "tools": [
      "{{calculator_0.data.instance}}",
      "{{serpAPI_0.data.instance}}"
    ]
  }
}
```

## See Also

- [02-node-structure.md](02-node-structure.md) - Node anatomy
- [07-connecting-nodes.md](07-connecting-nodes.md) - Edge connections
- [08-flow-examples.md](08-flow-examples.md) - Complete examples
