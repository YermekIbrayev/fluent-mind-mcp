# Common Nodes: RAG Components

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Document Loaders

### TextFile
**Name**: `textFile` | **Type**: `Document`

```javascript
{
  "name": "textFile",
  "inputs": {
    "txtFile": "path/to/file.txt",
    "metadata": ""
  }
}
```

### PDFLoader
**Name**: `pdfFile` | **Type**: `Document`

```javascript
{
  "name": "pdfFile",
  "inputs": {
    "pdfFile": "path/to/file.pdf",
    "usage": "perFile",
    "metadata": ""
  }
}
```

## Text Splitters

### RecursiveCharacterTextSplitter
**Name**: `recursiveCharacterTextSplitter` | **Type**: `RecursiveCharacterTextSplitter`

```javascript
{
  "name": "recursiveCharacterTextSplitter",
  "inputs": {
    "chunkSize": 1000,
    "chunkOverlap": 200
  }
}
```

## Embeddings

### OpenAIEmbeddings
**Name**: `openAIEmbeddings` | **Type**: `OpenAIEmbeddings`

```javascript
{
  "name": "openAIEmbeddings",
  "inputs": {
    "modelName": "text-embedding-3-small",
    "stripNewLines": true,
    "batchSize": 512
  }
}
```

### HuggingFaceInferenceEmbeddings
**Name**: `huggingFaceInferenceEmbeddings` | **Type**: `HuggingFaceInferenceEmbeddings`

```javascript
{
  "name": "huggingFaceInferenceEmbeddings",
  "inputs": {
    "modelName": "sentence-transformers/all-MiniLM-L6-v2"
  }
}
```

## Vector Stores

### Pinecone
**Name**: `pinecone` | **Type**: `Pinecone`

```javascript
{
  "name": "pinecone",
  "inputs": {
    "document": "{{textFile_0.data.instance}}",
    "embeddings": "{{openAIEmbeddings_0.data.instance}}",
    "pineconeIndex": "my-index",
    "pineconeNamespace": "",
    "topK": 4
  }
}
```

### Chroma
**Name**: `chroma` | **Type**: `Chroma`

```javascript
{
  "name": "chroma",
  "inputs": {
    "document": "{{textFile_0.data.instance}}",
    "embeddings": "{{openAIEmbeddings_0.data.instance}}",
    "collectionName": "my-collection",
    "topK": 4
  }
}
```

### InMemoryVectorStore
**Name**: `inMemoryVectorStore` | **Type**: `MemoryVectorStore`

```javascript
{
  "name": "inMemoryVectorStore",
  "inputs": {
    "document": "{{textFile_0.data.instance}}",
    "embeddings": "{{openAIEmbeddings_0.data.instance}}"
  }
}
```

## Retrievers

### VectorStoreRetriever
**Name**: `vectorStoreRetriever` | **Type**: `VectorStoreRetriever`

```javascript
{
  "name": "vectorStoreRetriever",
  "inputs": {
    "vectorStore": "{{pinecone_0.data.instance}}",
    "topK": 4
  }
}
```

## See Also

- [03-nodes-llm.md](03-nodes-llm.md) - Chat Models, Prompts
- [04-nodes-agents.md](04-nodes-agents.md) - Memory, Agents, Tools
- [08-flow-examples.md](08-flow-examples.md) - Complete examples
