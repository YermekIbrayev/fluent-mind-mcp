# Flowise Nodes Documentation - Summary

**Generated**: 2025-10-17 | **Version**: 2.0.0 | **Nodes**: 255 | **Categories**: 19

---

## 📊 Node Statistics by Category

| Category | Count | Location |
|----------|-------|----------|
| Document Loaders | 42 | [documentloaders/](documentloaders/) |
| Tools | 41 | [tools/](tools/) |
| Chat Models | 35 | [chatmodels/](chatmodels/) |
| Vector Stores | 26 | [vectorstores/](vectorstores/) |
| Embeddings | 17 | [embeddings/](embeddings/) |
| Agentflow | 15 | [agentflow/](agentflow/) |
| Retrievers | 14 | [retrievers/](retrievers/) |
| Memory | 12 | [memory/](memory/) |
| Sequential Agents | 11 | [sequentialagents/](sequentialagents/) |
| Cache | 7 | [cache/](cache/) |
| Text Splitters | 6 | [textsplitters/](textsplitters/) |
| Agents | 6 | [agents/](agents/) |
| Utilities | 5 | [utilities/](utilities/) |
| Output Parsers | 4 | [outputparsers/](outputparsers/) |
| Prompts | 4 | [prompts/](prompts/) |
| Response Synthesizer | 4 | [responsesynthesizer/](responsesynthesizer/) |
| Record Manager | 3 | [recordmanager/](recordmanager/) |
| Multi Agents | 2 | [multiagents/](multiagents/) |
| Speech to Text | 1 | [speechtotext/](speechtotext/) |

**Total**: 255 nodes

---

## 📝 File Structure Compliance

**150-Line Maximum Principle** - All files comply:

- ✅ Node docs: 20-90 lines (avg ~50)
- ✅ Category INDEX: 25-53 lines
- ✅ Main README: 139 lines
- ✅ Templates README: 148 lines

**Total Files**: 280+
- 255 node documentation files
- 19 category INDEX.md files
- 1 main README.md
- 3+ JSON templates

---

## 🏗️ Documentation Template

Each node: Header, Overview, Credentials, API Required/Optional Fields, Connections, Template, Use Cases, Source

## 🎯 Popular Nodes

**Chat**: ChatOpenAI, ChatAnthropic, ChatOllama
**Vectors**: Pinecone, Supabase, Qdrant
**Tools**: Calculator, WebBrowser, CustomTool
**Loaders**: PDF, Cheerio, CSV

---

## 🔍 Quick Navigation

**RAG**: documentloaders → textsplitters → embeddings → vectorstores → retrievers → chatmodels
**Agent**: chatmodels → agents → tools
**Multi-Agent**: multiagents / sequentialagents / agentflow
**Data**: documentloaders → textsplitters → utilities

---

## 🔌 API Features (v2.0)

1. **API Required/Optional Fields** - Clear documentation
2. **JSON Templates** - In `templates/` directory
3. **Field Path Notation** - Explicit paths (e.g., `data.inputs.model`)
4. **Connection Syntax** - `"{{nodeId.data.instance}}"`

**Templates**: node-api-request.json, cohere-rerank-retriever.json, tavily-api.json

---

## 🛠️ Generation & Maintenance

**Command**: `node scripts/generate-node-docs.js`
**Source**: `packages/components/nodes/{category}/{NodeName}/{NodeName}.ts`
**Update**: Run script → Review → Commit

---

## 📐 Architecture

**Token Efficient** (≤150 lines) | **Hierarchical** | **Consistent** | **Cross-Referenced** | **Traceable** | **API-First**

---

## ✅ Quality

**Coverage**: 100% (255/255) | **Format**: 100% (≤150 lines) | **Structure**: 100% | **Indexes**: 100% (19/19) | **API Docs**: 100%

---

## 📚 Related Documentation

- [Nodes README](README.md) - Main navigation
- [Templates](templates/) - JSON API templates
- [API Structure](../api/02-node-structure.md) - Node anatomy
- [API Examples](../api/03-common-nodes.md) - Usage examples

---

**Version**: 2.0.0 | **Last Updated**: 2025-10-17 | **Generator**: `scripts/generate-node-docs.js`
