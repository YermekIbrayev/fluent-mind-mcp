# Research: Technical Decisions

**Feature**: Chatflow Automation System | **Date**: 2025-10-17 | **Status**: Complete

---

## R1: ChromaDB Configuration

**Decision**: ChromaDB PersistentClient with HNSW indexing, cosine similarity, separate collections

**Rationale**: Local persistence via SQLite, excellent <500ms performance for 50-1000 entries, simple API (get_or_create_collection), automatic installation via pip

**Alternatives**: Faiss (complex setup, manual persistence), Pinecone/Weaviate (cloud, not local), pgvector (heavy)

**Config**: `hnsw:space=cosine`, `hnsw:construction_ef=100`, `hnsw:M=16` (defaults good for <1000 entries)

---

## R2: Embedding Model

**Decision**: sentence-transformers/all-MiniLM-L6-v2

**Rationale**: 80MB size, <50ms inference, 384-dim embeddings, 68% semantic similarity score, CPU-friendly, auto-download from Hugging Face

**Alternatives**: OpenAI embeddings (API key required, costs), all-mpnet-base-v2 (768 dims, 3x larger), BGE models (>400MB)

---

## R3: Connection Inference Algorithm

**Decision**: Two-phase: (1) Topological ordering by node category, (2) Type-compatible sequential chaining

**Rationale**: Ensures correct flow (Input → Processing → Memory → Output), matches baseClass compatibility, validates required inputs, deterministic, O(n²) acceptable for 5-10 nodes

**Algorithm**:
1. Categorize nodes by role (Input/Processing/Memory/Output)
2. For each node i, connect to node j where output_baseClass matches input_baseClasses
3. Validate all required inputs satisfied

**Alternatives**: Graph algorithms (Kahn's, DFS - overkill), ML approach (needs training data), manual spec (defeats token efficiency)

---

## R4: Circuit Breaker

**Decision**: Custom lightweight implementation, in-memory state, no external dependencies

**Rationale**: <100 lines code, no library dependencies, suitable for single-process MCP, clear state semantics (CLOSED/OPEN/HALF_OPEN)

**States**: CLOSED (normal) → OPEN (3 failures, 5min timeout) → HALF_OPEN (test request) → CLOSED (success) or OPEN (failure)

**Alternatives**: pybreaker library (adds dependency, more complex), Redis-based (overkill), persistent state (unnecessary for MCP)

---

## R5: Node Positioning

**Decision**: Left-to-right column layout with fixed spacing

**Rationale**: Intuitive reading direction, deterministic (same nodes = same layout), simple math (column * 300px, row * 200px), no overlaps, O(n) complexity

**Algorithm**:
1. Assign columns by connection depth (max_depth_from_inputs)
2. Assign rows within columns (sequential 0, 1, 2...)
3. Position: x = column * 300, y = row * 200

**Alternatives**: Force-directed (non-deterministic, iterative), Sugiyama (complex), grid layout (less intuitive)

---

## R6: Spec-Driven Workflow Integration

**Decision**: Delegate complex chatflows to existing `.specify/commands/speckit.*` workflows via subprocess

**Rationale**: Reuse proven SDD patterns from Feature 001, human-in-the-loop for complex flows, file-based artifacts for auditability, separates concerns

**Complexity Detection**: >5 nodes, keywords (agent/multi-step/conditional), template match <70%, multiple integrations

**Integration**: Create feature directory → write initial spec → run speckit.specify/clarify/plan → generate chatflow from plan

**Alternatives**: Inline implementation (duplicates SDD logic), LLM-only planning (less structured), template-only (insufficient for novel workflows)

---

## Summary

| Area | Decision | Key Benefit |
|------|----------|-------------|
| Vector DB | ChromaDB persistent local | Simple, performant (<500ms) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Lightweight, fast, CPU-friendly |
| Connection | Topological + type matching | Deterministic, O(n²) acceptable |
| Circuit Breaker | Custom lightweight | No dependencies, <100 lines |
| Positioning | Left-to-right columns | Intuitive, O(n), deterministic |
| Complex Workflows | Delegate to Speckit | Reuse proven patterns, human validation |

---

**File Size**: 93 lines | **Status**: ✅ GREEN ZONE
