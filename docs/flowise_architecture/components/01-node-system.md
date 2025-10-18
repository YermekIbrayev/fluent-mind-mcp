# Node System

**Package**: `packages/components`
**Purpose**: Pluggable node library for AI workflows

## Node Interface

```typescript
interface INode {
  label: string              // Display name
  name: string               // Unique ID
  version: number            // Node version
  type: string               // Node type
  icon: string               // Icon file
  category: string           // Category
  description: string        // Description
  baseClasses: string[]      // Inheritance

  credential?: INodeParams   // Required credential
  inputs: INodeParams[]      // Input parameters
  outputs?: INodeParams[]    // Output parameters

  // Lifecycle methods
  init?(nodeData, input, options): Promise<any>
  run?(nodeData, input, options): Promise<any>
  loadMethods?: { [key: string]: Function }
}
```

## Example Node

```typescript
class ChatOpenAI_ChatModels implements INode {
  constructor() {
    this.label = 'ChatOpenAI'
    this.name = 'chatOpenAI'
    this.version = 8.3
    this.type = 'ChatOpenAI'
    this.icon = 'openai.svg'
    this.category = 'Chat Models'
    this.baseClasses = ['ChatOpenAI', 'BaseChatModel']

    this.credential = {
      label: 'Connect Credential',
      name: 'credential',
      type: 'credential',
      credentialNames: ['openAIApi']
    }

    this.inputs = [
      {
        label: 'Model Name',
        name: 'modelName',
        type: 'asyncOptions',
        loadMethod: 'listModels',
        default: 'gpt-4o-mini'
      },
      {
        label: 'Temperature',
        name: 'temperature',
        type: 'number',
        default: 0.9,
        optional: true
      }
    ]
  }

  async init(nodeData: INodeData) {
    const modelName = nodeData.inputs?.modelName
    const credential = await getCredentialData(nodeData.credential)

    return new ChatOpenAI({
      modelName,
      openAIApiKey: credential.apiKey
    })
  }
}

module.exports = { nodeClass: ChatOpenAI_ChatModels }
```

## Parameter Types

- `string` - Text input
- `number` - Numeric input
- `boolean` - Checkbox
- `password` - Hidden input
- `json` - JSON editor
- `code` - Code editor
- `options` - Static dropdown
- `asyncOptions` - Dynamic dropdown
- `credential` - Credential selector
- `BaseLLM`, `BaseRetriever`, etc. - Node connections

## Node Categories

- Chat Models - LLM chat interfaces
- LLMs - Text completion
- Embeddings - Vector embeddings
- Document Loaders - Load documents
- Agents - Autonomous agents
- Tools - Agent tools
- Memory - Conversation memory
- Chains - Pre-built chains
- Retrievers - Document retrieval
- Vector Stores - Vector databases
- Prompts - Prompt templates
- Output Parsers - Parse LLM output

## Node Lifecycle

1. **Load**: Server scans `nodes/` directory
2. **Cache**: NodesPool caches metadata
3. **Instantiate**: On flow execution
4. **Init**: `node.init()` called
5. **Execute**: Node processes data
6. **Cleanup**: Resources released

## UI Auto-Generation

Frontend reads node metadata to generate:
- Configuration forms
- Connection validation
- Palette display
- Help text
