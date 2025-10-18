# Variable Resolution Utilities

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

## resolveVariables()

**Location**: `packages/server/src/utils/index.ts:380`

Resolves all variable types in node inputs.

```typescript
async function resolveVariables(
  flowNodeData: INodeData,
  flowNodes: IReactFlowNode[],
  question: string,
  chatHistory: IMessage[],
  flowData: ICommonObject,
  uploadedFilesContent: string,
  availableVariables: IVariable[],
  variableOverrides: IVariableOverride[]
): Promise<INodeData>
```

## Resolution Priority

**Order** (highest to lowest):
1. **Variable Overrides** - API-level overrides
2. **Dynamic Variables** - Runtime values (setVariable nodes)
3. **Database Variables** - Static config
4. **System Variables** - Built-in
5. **Node References** - `{{nodeId.data.instance}}`
6. **Default Values** - Fallback

## System Variables

```typescript
{
  '{{question}}': userInput,
  '{{chat_history}}': chatHistoryText,
  '{{current_date_time}}': new Date().toISOString(),
  '{{file_attachment}}': uploadedFilesContent,
  '{{runtime_messages_length}}': chatHistory.length,
  '{{loop_count}}': loopIteration
}
```

## Node References

**Pattern**: `{{nodeId.data.instance}}`

```typescript
// Configuration
{
  "inputs": {
    "model": "{{chatOpenAI_0.data.instance}}",
    "memory": "{{bufferMemory_0.data.instance}}"
  }
}

// After resolution
{
  "inputs": {
    "model": <ChatOpenAI instance>,
    "memory": <BufferMemory instance>
  }
}
```

## replaceInputsWithConfig()

**Location**: `packages/server/src/utils/index.ts:450`

Applies API-level overrides.

```typescript
function replaceInputsWithConfig(
  flowNodeData: INodeData,
  overrideConfig: IOverrideConfig,
  nodeOverrides: INodeOverrides,
  variableOverrides: IVariableOverride[]
): INodeData
```

### Override Types

```typescript
// Node-specific
nodeOverrides = { "chatOpenAI_0": { "modelName": "gpt-4o" } }

// Global config
overrideConfig = { "systemMessage": "You are helpful" }

// Variable overrides
variableOverrides = [{ name: "api_key", value: "sk-xxx" }]
```

## Dynamic Variables

Set by `setVariable` node:

```typescript
// setVariable output
{ dynamicVariables: { "user_name": "John" } }

// Usage in downstream nodes
"prompt": "Hello {{user_name}}"

// Storage
if (nodeType === 'setVariable') {
  dynamicVariables[key] = result.dynamicVariables[key]
}
```

## Database Variables

```typescript
// Query from database
const variables = await appDataSource.getRepository(Variable)
  .find({ where: { workspaceId } })

// Available as {{variableName}}
const dict = {}
for (const v of variables) dict[v.name] = v.value
```

## Summary

| Type | Priority | Source | Example |
|------|----------|--------|---------|
| Overrides | 1 | API | `nodeOverrides[id]` |
| Dynamic | 2 | setVariable | `{{user_name}}` |
| Database | 3 | Variable entity | `{{api_key}}` |
| System | 4 | Built-in | `{{question}}` |
| Node Refs | 5 | Other nodes | `{{llm_0.data.instance}}` |
| Defaults | 6 | Definition | Fallback |
