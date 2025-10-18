# Common Nodes: LLM & Prompts

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Chat Models

### ChatOpenAI
**Name**: `chatOpenAI` | **Type**: `ChatOpenAI`

```javascript
{
  "name": "chatOpenAI",
  "version": 8.3,
  "inputs": {
    "modelName": "gpt-4o-mini",
    "temperature": 0.9,
    "maxTokens": "",
    "streaming": true
  },
  "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel", "Runnable"]
}
```

**Models**: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo

### ChatAnthropic
**Name**: `chatAnthropic` | **Type**: `ChatAnthropic`

```javascript
{
  "name": "chatAnthropic",
  "inputs": {
    "modelName": "claude-3-5-sonnet-20241022",
    "temperature": 0.9
  },
  "baseClasses": ["ChatAnthropic", "BaseChatModel", "BaseLanguageModel"]
}
```

### AzureChatOpenAI
**Name**: `azureChatOpenAI` | **Type**: `AzureChatOpenAI`

```javascript
{
  "name": "azureChatOpenAI",
  "inputs": {
    "modelName": "gpt-35-turbo",
    "temperature": 0.9
  }
}
```

### ChatOllama
**Name**: `chatOllama` | **Type**: `ChatOllama`

```javascript
{
  "name": "chatOllama",
  "inputs": {
    "modelName": "llama2",
    "baseUrl": "http://localhost:11434"
  }
}
```

## Prompts

### PromptTemplate
**Name**: `promptTemplate` | **Type**: `PromptTemplate`

```javascript
{
  "name": "promptTemplate",
  "inputs": {
    "template": "What is {topic}?",
    "promptValues": "{\"topic\":\"AI\"}"
  },
  "baseClasses": ["PromptTemplate", "BaseStringPromptTemplate", "BasePromptTemplate"]
}
```

**Variables**: Use `{variableName}` for placeholders

### ChatPromptTemplate
**Name**: `chatPromptTemplate` | **Type**: `ChatPromptTemplate`

```javascript
{
  "name": "chatPromptTemplate",
  "inputs": {
    "systemMessagePrompt": "You are a helpful assistant",
    "humanMessagePrompt": "Answer: {question}"
  }
}
```

## See Also

- [04-nodes-agents.md](04-nodes-agents.md) - Memory, Agents, Tools
- [05-nodes-rag.md](05-nodes-rag.md) - RAG components
- [02-node-structure.md](02-node-structure.md) - Node anatomy
