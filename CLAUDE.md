# fluent-mind-mcp Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-10-17

## Active Technologies
- Python 3.12+ (existing Flowise MCP Server codebase compatibility) + ChromaDB (local vector DB), sentence-transformers (all-MiniLM-L6-v2 embeddings), existing Flowise MCP Server, httpx (Flowise API client) (002-flowise-automation-workflow)
- Python 3.12+ + ChromaDB, sentence-transformers (all-MiniLM-L6-v2), existing Flowise MCP Server, httpx (002-flowise-automation-workflow)
- Local ChromaDB (5 collections: nodes, templates, sdd_artifacts, failed_artifacts, sessions) (002-flowise-automation-workflow)

## Project Structure
```
src/
tests/
```

## Commands
cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style
Python 3.12+ (existing Flowise MCP Server codebase compatibility): Follow standard conventions

## Recent Changes
- 002-flowise-automation-workflow: Added Python 3.12+ + ChromaDB, sentence-transformers (all-MiniLM-L6-v2), existing Flowise MCP Server, httpx
- 002-flowise-automation-workflow: Added Python 3.12+ (existing Flowise MCP Server codebase compatibility) + ChromaDB (local vector DB), sentence-transformers (all-MiniLM-L6-v2 embeddings), existing Flowise MCP Server, httpx (Flowise API client)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
