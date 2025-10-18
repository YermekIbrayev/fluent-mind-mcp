# Flowise Architecture - Documentation Index

**Version**: 3.0.8 | **Date**: 2025-10-17

## 📚 Available Documentation

### Core Overview
- **[01-overview.md](01-overview.md)** - Project overview, tech stack, high-level architecture
- **[02-monorepo-structure.md](02-monorepo-structure.md)** - Workspace layout, packages, build system

### Backend
- **[backend/01-core-app.md](backend/01-core-app.md)** - App class, initialization, subsystems
- **[backend/02-layered-architecture.md](backend/02-layered-architecture.md)** - Routes→Controllers→Services→Database

### AI Flow Creation
- **[ai/README.md](ai/README.md)** - AI flow execution overview, concepts, patterns
- **[ai/01-flow-creation-workflow.md](ai/01-flow-creation-workflow.md)** - Complete workflow from API to result
- **[ai/02-helper-utilities.md](ai/02-helper-utilities.md)** - Graph, variable, execution utilities

### API & Programmatic Flow Creation
- **[api/README.md](api/README.md)** - Complete guide to creating flows via API (CRUD operations)
- **[api/01-creating-flows-api.md](api/01-creating-flows-api.md)** - REST endpoints and request structure
- **[api/02-node-structure.md](api/02-node-structure.md)** - Node anatomy and critical fields
- **[api/03-nodes-llm.md](api/03-nodes-llm.md)** - Chat models and prompts
- **[api/04-nodes-agents.md](api/04-nodes-agents.md)** - Memory, chains, agents, tools
- **[api/05-nodes-rag.md](api/05-nodes-rag.md)** - Document loaders, embeddings, vector stores
- **[api/06-nodes-overview.md](api/06-nodes-overview.md)** - Node types quick reference
- **[api/07-connecting-nodes.md](api/07-connecting-nodes.md)** - Edge connections and patterns
- **[api/08-flow-examples.md](api/08-flow-examples.md)** - Working examples and helpers
- **[api/09-canvas-overview.md](api/09-canvas-overview.md)** - Visual properties, positioning basics
- **[api/10-canvas-positioning.md](api/10-canvas-positioning.md)** - Layout algorithms
- **[api/11-canvas-patterns.md](api/11-canvas-patterns.md)** - Common visual patterns
- **[api/12-canvas-complete-example.md](api/12-canvas-complete-example.md)** - Full LLM chain example

### Nodes Reference (303+ Nodes)
- **[nodes/README.md](nodes/README.md)** - Complete node documentation index
- **[nodes/chatmodels/](nodes/chatmodels/)** - 35 chat model nodes (OpenAI, Anthropic, etc.)
- **[nodes/tools/](nodes/tools/)** - 41 tool nodes (Calculator, WebBrowser, etc.)
- **[nodes/vectorstores/](nodes/vectorstores/)** - 26 vector store nodes
- **[nodes/documentloaders/](nodes/documentloaders/)** - 42 document loader nodes
- **[nodes/embeddings/](nodes/embeddings/)** - 18 embedding nodes
- **[nodes/retrievers/](nodes/retrievers/)** - 18 retriever nodes
- See [nodes/README.md](nodes/README.md) for all 19 categories

## 🚀 Quick Start Paths

**New Developer** (30 min): `01-overview.md → 02-monorepo-structure.md → backend/01-core-app.md`

**Full Stack Developer** (1 hour): `01-overview → 02-monorepo → backend/* → ai/*`

**API Integration / CRUD Developer** (30 min): `api/README.md → api/01-creating-flows-api.md → api/08-flow-examples.md`

**Flow Builder / Node User** (20 min): `nodes/README.md → nodes/{category}/`

**AI/Flow Developer** (45 min): `01-overview → ai/README.md → ai/01-flow-creation-workflow.md → api/README.md`

**Plugin Developer** (30 min): `01-overview → nodes/README.md → nodes/{category}/*`

## 📊 Quick Reference

**Tech Stack**: Node.js 18+, Express, TypeScript, React 18, Material-UI v5, TypeORM, BullMQ
**Databases**: PostgreSQL, MySQL, SQLite
**Packages**: server (backend), ui (frontend), components (nodes), api-documentation
**Node Types**: 303+ nodes across 19 categories (LLMs, agents, tools, memory, RAG, etc.)

## 🎯 Core Concepts

- **ChatFlow**: Visual workflow composed of connected nodes
- **Node**: Building block (LLM, tool, agent, etc.) with inputs/outputs
- **Edge**: Connection between nodes with type compatibility
- **Credential**: Encrypted API key/token (AES-256-GCM)
- **CRUD**: Create/Read/Update/Delete flows via REST API

## 🏗️ Architecture Principles

1. Plugin Architecture - Self-contained node plugins
2. Layered Design - Routes → Controllers → Services → Database
3. Async by Default - BullMQ background jobs
4. Security First - Encryption, RBAC, auth strategies
5. Multi-tenant - Workspace isolation
6. Cloud Native - Stateless, horizontally scalable

## 📖 External Resources

- **GitHub**: https://github.com/FlowiseAI/Flowise
- **Docs**: https://docs.flowiseai.com
- **Discord**: https://discord.gg/jbaHfsRVBW
- **Contributing**: See CONTRIBUTING.md in project root

## File Size Policy

**Goal**: 100 lines | **Yellow Zone**: 150 lines | **Hard Limit**: 200 lines

All documentation files must respect these limits for maintainability and readability.
