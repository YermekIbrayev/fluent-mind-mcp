# Flowise Architecture - Project Overview

## What is Flowise?

Flowise is a **visual builder for AI agents and LLM applications** built with a low-code/no-code approach.
It enables users to build AI workflows, chatbots, and agents through a drag-and-drop interface.

**Version**: 3.0.8
**Repository**: FlowiseAI/Flowise
**License**: Apache License Version 2.0

## Core Concept

Flowise allows users to visually create AI workflows by connecting "nodes" that represent:
- LLM models (OpenAI, Anthropic, etc.)
- Vector databases (Pinecone, Chroma, etc.)
- Document loaders
- Memory systems
- Agents and chains
- Tools and utilities

## Architecture Pattern

**Monorepo Structure** using:
- **Package Manager**: pnpm with workspaces
- **Build Tool**: Turbo for parallel builds
- **Pattern**: Multi-package monorepo

## Technology Stack

### Backend
- **Runtime**: Node.js >= 18.15.0
- **Framework**: Express.js
- **Language**: TypeScript
- **ORM**: TypeORM
- **Queue**: BullMQ
- **CLI**: oclif

### Frontend
- **Framework**: React 18
- **UI Library**: Material-UI v5
- **State Management**: Redux Toolkit
- **Build Tool**: Vite
- **Flow Canvas**: ReactFlow (for visual node editor)

### Databases Supported
- PostgreSQL
- MySQL
- SQLite (default)

### Additional Infrastructure
- **Caching**: Redis (optional)
- **Sessions**: Redis/PostgreSQL/MySQL/SQLite
- **Observability**: OpenTelemetry, Prometheus, Winston logging
- **Authentication**: Passport.js (JWT, OAuth2, SAML)

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (UI)                        │
│  React + Material-UI + ReactFlow + Redux                    │
│  (Visual node editor, chat interface, management UI)        │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API / WebSocket / SSE
┌────────────────────────┴────────────────────────────────────┐
│                      Backend (Server)                        │
│  Express + TypeORM + BullMQ + Passport                      │
│  ┌─────────────┬──────────────┬──────────────────────────┐ │
│  │  API Layer  │ Queue Worker │  Enterprise Features     │ │
│  │  (REST/SSE) │   (BullMQ)   │  (RBAC, SSO, Workspace)  │ │
│  └─────────────┴──────────────┴──────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                      Components Package                      │
│  Pluggable Nodes (LLMs, Agents, Tools, Memory, etc.)       │
│  Each node is self-contained with credentials & logic       │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
                  External Services
         (LLM APIs, Vector DBs, Storage, etc.)
```

## Key Components

### 1. **Packages**
- `packages/server` - Backend API server
- `packages/ui` - Frontend React application
- `packages/components` - Node definitions and integrations
- `packages/api-documentation` - API docs

### 2. **Core Concepts**
- **ChatFlow**: A saved flow/workflow configuration
- **Node**: A building block in a flow (LLM, tool, agent, etc.)
- **Credential**: Stored API keys and auth tokens
- **Execution**: Runtime instance of a flow
- **Agent**: Autonomous AI agent with tools
- **Assistant**: OpenAI Assistant integration

### 3. **Execution Model**
1. User creates a flow in UI (drag-and-drop nodes)
2. Flow saved to database as JSON
3. When executed (via API or UI):
   - Flow loaded from database
   - Nodes instantiated in correct order
   - Data flows through connected nodes
   - Results returned to user

## Key Features

- Visual flow builder
- 100+ integrations (LLMs, vector DBs, tools)
- Chat interface for testing flows
- API endpoints for production use
- Credential management
- Document processing and vector storage
- Agent workflows with tool calling
- OpenAI Assistants integration
- Multi-agent orchestration
- Evaluation and testing framework
- Enterprise features (RBAC, SSO, workspaces)

## Deployment Options

1. **npm package**: `npm install -g flowise`
2. **Docker**: Official Docker images
3. **Self-hosted**: Deploy to any Node.js host
4. **Flowise Cloud**: Managed hosting

## API Endpoints

- `/api/v1/chatflows` - Flow management
- `/api/v1/prediction` - Execute flows (chat)
- `/api/v1/credentials` - Credential management
- `/api/v1/assistants` - OpenAI Assistants
- `/api/v1/agentflows` - Agent workflows
- Public API endpoints for embedding

## References

- Documentation: arch/02-project-structure.md
- Backend: arch/03-backend-architecture.md
- Frontend: arch/04-frontend-architecture.md
- Database: arch/05-database-models.md
