# Flowise Architecture Documentation

**Version**: 3.0.8 | **Last Updated**: 2025-10-17

Complete architectural documentation for the Flowise project.

## Quick Navigation

### Getting Started
- **[INDEX.md](INDEX.md)** - Complete documentation index with all files and quick start paths
- **[01-overview.md](01-overview.md)** - High-level overview, tech stack, core concepts
- **[02-monorepo-structure.md](02-monorepo-structure.md)** - Monorepo layout, package organization

### Core Systems
- **[backend/](backend/)** - Express server, layered architecture, core app
- **[ai/](ai/)** - AI flow creation and execution workflow
- **[api/](api/)** - **Programmatic flow creation via API (CRUD operations)**
- **[nodes/](nodes/)** - 303+ node specifications (LLMs, tools, agents, RAG, etc.)

### Specialized Topics
- **[frontend/](frontend/)** - React UI, Redux, canvas editor
- **[database/](database/)** - TypeORM entities, schemas, relationships
- **[components/](components/)** - Node system, plugins, integrations
- **[queue/](queue/)** - BullMQ, background jobs, workers
- **[security/](security/)** - Auth strategies, RBAC, encryption
- **[deployment/](deployment/)** - Deployment options, scaling, monitoring

## Reading Paths

### API Integration / CRUD Developer (30-45 min)
```
api/README.md → api/01-creating-flows-api.md → api/08-flow-examples.md
```
**Goal**: Create, read, update, delete flows programmatically via REST API

### Quick Understanding (30 min)
```
01-overview.md → 02-monorepo-structure.md → api/README.md
```
**Goal**: Understand what Flowise is and how to use it via API

### Full Stack Developer (2-3 hours)
```
01-overview → 02-monorepo → backend/* → ai/* → api/*
```
**Goal**: Contribute to core features

### AI/Flow Developer (1 hour)
```
01-overview → ai/README.md → ai/01-flow-creation-workflow.md → api/README.md
```
**Goal**: Understand how flows are created and executed internally

### Plugin/Node Developer (1 hour)
```
01-overview → nodes/README.md → nodes/{category}/*
```
**Goal**: Create custom nodes and integrations

### DevOps/Deployment (1.5 hours)
```
01-overview → deployment/* → queue/* → security/*
```
**Goal**: Deploy and scale Flowise in production

## Key Concepts

- **ChatFlow**: Visual workflow composed of connected nodes (stored as JSON, executed at runtime)
- **Node**: Building block representing LLMs, tools, agents, memory, etc. (plugin with metadata-driven UI)
- **Edge**: Connection between nodes with type compatibility validation
- **Credential**: Encrypted API key/token (AES-256-GCM, decrypted only at runtime)
- **CRUD Operations**: Create, Read, Update, Delete flows via REST API at `/api/v1/chatflows`
- **Execution**: Runtime instance of a flow (synchronous or asynchronous via BullMQ queue)

## Architecture Principles

1. **Plugin Architecture** - Self-contained, metadata-driven node plugins
2. **Layered Design** - Routes → Controllers → Services → Database
3. **Async by Default** - Background jobs via BullMQ for scalability
4. **Security First** - Encryption, auth, RBAC, rate limiting built-in
5. **Multi-tenant Ready** - Workspace isolation for enterprise
6. **Observable** - Logging, metrics, tracing out of the box
7. **Cloud Native** - Stateless design, horizontal scaling, health checks

## Technology Stack

**Backend**: Node.js 18+, Express, TypeScript, TypeORM
**Frontend**: React 18, Material-UI v5, Redux Toolkit, ReactFlow, Vite
**Queue**: BullMQ, Redis
**Database**: PostgreSQL, MySQL, SQLite
**Auth**: Passport.js (JWT, OAuth2, SAML)
**Observability**: Winston, Prometheus, OpenTelemetry
**Storage**: Local filesystem, S3, GCS, Azure Blob

## File Size Policy

**Goal**: 100 lines | **Yellow Zone**: 150 lines | **Hard Limit**: 200 lines

All documentation files must respect these limits for maintainability and readability. See [INDEX.md](INDEX.md) for details.

## License

Apache 2.0 - Part of the Flowise project
