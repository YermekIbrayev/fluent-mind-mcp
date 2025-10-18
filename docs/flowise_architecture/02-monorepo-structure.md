# Monorepo Structure

## Workspace Layout

```
Flowise-main/
├── packages/               # All packages
│   ├── server/            # Backend API
│   ├── ui/                # Frontend React app
│   ├── components/        # Node definitions
│   └── api-documentation/ # API docs
├── docker/                # Docker configs
├── package.json           # Root workspace
├── pnpm-workspace.yaml    # Workspace definition
└── turbo.json             # Build orchestration
```

## Package Manager

**Tool**: pnpm with workspaces
**Build**: Turbo for parallel builds

## Workspace Configuration

```json
{
  "workspaces": [
    "packages/*",
    "flowise",
    "ui",
    "components",
    "api-documentation"
  ]
}
```

## Package Dependencies

```
packages/ui (Frontend)
  └─> HTTP API ──> packages/server (Backend)
                      └─> packages/components (Nodes)
                            └─> External LLM APIs
```

## Build Commands

```bash
pnpm install        # Install all dependencies
pnpm build          # Build all packages (Turbo)
pnpm dev            # Run all in dev mode
pnpm start          # Start server
pnpm start-worker   # Start queue worker
pnpm test           # Run all tests
pnpm clean          # Clean build artifacts
```

## Turbo Configuration

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "build/**"]
    },
    "dev": {
      "cache": false
    }
  }
}
```

## Entry Points

- **Server CLI**: `packages/server/bin/run`
- **Server Main**: `packages/server/src/index.ts`
- **UI Entry**: `packages/ui/src/index.jsx`
- **Components**: `packages/components/src/index.ts`

## Package: Server

**Purpose**: Backend API and CLI
**Tech**: Express + TypeScript + TypeORM
**Output**: `packages/server/dist/`

**Key Directories**:
- `src/controllers/` - Request handlers
- `src/services/` - Business logic
- `src/routes/` - API routes
- `src/database/entities/` - Data models
- `src/enterprise/` - Enterprise features

## Package: UI

**Purpose**: Frontend application
**Tech**: React + Vite + Material-UI
**Output**: `packages/ui/build/`

**Key Directories**:
- `src/views/` - Page components
- `src/ui-component/` - Reusable components
- `src/store/` - Redux store
- `src/api/` - API client

## Package: Components

**Purpose**: Node library
**Tech**: TypeScript + LangChain
**Output**: `packages/components/dist/`

**Key Directories**:
- `nodes/` - All node types
- `credentials/` - Credential schemas
- `src/` - Shared utilities

## Configuration Files

- `.env` - Environment variables
- `tsconfig.json` - TypeScript config (per package)
- `package.json` - Dependencies (per package)
- `.eslintrc.js` - Linting rules
- `Dockerfile` - Docker build
