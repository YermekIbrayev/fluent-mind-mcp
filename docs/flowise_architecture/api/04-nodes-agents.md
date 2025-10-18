# Common Nodes: Agents & Tools

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Memory

### BufferMemory
**Name**: `bufferMemory` | **Type**: `BufferMemory`

```javascript
{
  "name": "bufferMemory",
  "inputs": {
    "sessionId": "",
    "memoryKey": "chat_history"
  },
  "baseClasses": ["BufferMemory", "BaseChatMemory", "BaseMemory"]
}
```

### ConversationSummaryMemory
**Name**: `conversationSummaryMemory` | **Type**: `ConversationSummaryMemory`

```javascript
{
  "name": "conversationSummaryMemory",
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}",
    "sessionId": "",
    "memoryKey": "chat_history"
  }
}
```

## Chains

### LLMChain
**Name**: `llmChain` | **Type**: `LLMChain`

```javascript
{
  "name": "llmChain",
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}",
    "prompt": "{{promptTemplate_0.data.instance}}",
    "outputParser": "",
    "chainName": ""
  },
  "baseClasses": ["LLMChain", "BaseChain", "Runnable"]
}
```

### ConversationChain
**Name**: `conversationChain` | **Type**: `ConversationChain`

```javascript
{
  "name": "conversationChain",
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}",
    "memory": "{{bufferMemory_0.data.instance}}",
    "systemMessage": "You are a helpful assistant"
  }
}
```

## Agents

### ConversationalAgent
**Name**: `conversationalAgent` | **Type**: `AgentExecutor`

```javascript
{
  "name": "conversationalAgent",
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}",
    "memory": "{{bufferMemory_0.data.instance}}",
    "tools": [
      "{{calculator_0.data.instance}}",
      "{{serpAPI_0.data.instance}}"
    ],
    "systemMessage": "",
    "maxIterations": ""
  },
  "baseClasses": ["AgentExecutor", "BaseChain", "Runnable"]
}
```

## Tools

### Calculator
**Name**: `calculator` | **Type**: `Calculator`

```javascript
{
  "name": "calculator",
  "inputs": {},
  "baseClasses": ["Calculator", "Tool", "StructuredTool"]
}
```

### SerpAPI
**Name**: `serpAPI` | **Type**: `SerpAPI`

```javascript
{
  "name": "serpAPI",
  "inputParams": [{
    "label": "Connect Credential",
    "name": "credential",
    "type": "credential",
    "credentialNames": ["serpApi"]
  }]
}
```

### WebBrowser
**Name**: `webBrowser` | **Type**: `WebBrowser`

```javascript
{
  "name": "webBrowser",
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}",
    "embeddings": "{{openAIEmbeddings_0.data.instance}}"
  }
}
```

## See Also

- [03-nodes-llm.md](03-nodes-llm.md) - Chat Models, Prompts
- [05-nodes-rag.md](05-nodes-rag.md) - RAG components
- [08-flow-examples.md](08-flow-examples.md) - Complete examples
