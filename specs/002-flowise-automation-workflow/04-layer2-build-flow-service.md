# Layer 2: Build Flow Service

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: BuildFlowService with connection inference and node positioning

---

## BuildFlowService (build_flow_service.py)

```python
class BuildFlowService:
    """
    Service for creating chatflows from templates or node lists.

    WHY: Encapsulates flowData generation, connection inference, node positioning
    DEPENDENCIES: VectorDatabaseClient, FlowiseApiClient, NodeCatalogService
    """

    async def build_from_template(self,
                                  template_id: str,
                                  **parameters) -> ChatflowResponse:
        """
        Create chatflow from stored template with parameter overrides.

        WHY: Reuses proven patterns, <20 token invocation
        ALGORITHM: Retrieve template → Apply parameters → Create via API
        PERFORMANCE: <10s per NFR-011
        """
        # 1. Retrieve template from vector DB
        template = await self._get_template(template_id)
        if not template:
            raise TemplateNotFoundError(template_id)

        # 2. Apply parameter overrides (model, temperature, etc.)
        flow_data = self._apply_parameters(template.flow_data, parameters)

        # 3. Create chatflow via Flowise API
        chatflow = await self.flowise.create_chatflow(flow_data)

        return ChatflowResponse(
            chatflow_id=chatflow.id,
            name=chatflow.name
        )

    async def build_from_nodes(self,
                              nodes: List[str],
                              connections: str = "auto",
                              **parameters) -> ChatflowResponse:
        """
        Create chatflow from node list with automatic connections.

        WHY: Enables custom flows without manual connection specification
        ALGORITHM: Validate nodes → Infer connections → Position nodes → Create
        CONNECTION INFERENCE: Type-compatible chain (see _infer_connections)
        NODE POSITIONING: Left-to-right flow pattern (see _generate_flow_data)
        PERFORMANCE: <15s per NFR-012
        """
        # 1. Validate all nodes exist in catalog
        await self._validate_nodes_exist(nodes)

        # 2. Infer connections using type-compatible chain algorithm
        if connections == "auto":
            edges = await self._infer_connections(nodes)
        else:
            edges = self._parse_manual_connections(connections)

        # 3. Generate flowData with node positioning
        flow_data = self._generate_flow_data(nodes, edges, parameters)

        # 4. Create chatflow
        chatflow = await self.flowise.create_chatflow(flow_data)
        return ChatflowResponse(chatflow_id=chatflow.id, name=chatflow.name)

    async def _infer_connections(self, nodes: List[str]) -> List[Edge]:
        """
        Infer connections using type-compatible chain with validation.

        WHY: Follows spec clarification for automatic connection logic
        ALGORITHM:
        1. Order nodes by flow pattern heuristics (Input → Processing → Memory → Output)
        2. Connect consecutive nodes where output baseClass matches input baseClass
        3. Validate all required inputs satisfied
        4. Fail safely with IncompatibleNodesError if no valid chain
        """
        # 1. Order nodes by flow pattern
        ordered_nodes = self._order_by_flow_pattern(nodes)

        # 2. Get node metadata for baseClass matching
        node_metadata = {
            n: await self.node_catalog.get_node(n)
            for n in ordered_nodes
        }

        # 3. Connect consecutive compatible nodes
        edges = []
        for i in range(len(ordered_nodes) - 1):
            source = ordered_nodes[i]
            target = ordered_nodes[i + 1]

            if self._is_compatible(node_metadata[source], node_metadata[target]):
                edges.append(Edge(
                    source=source,
                    target=target,
                    sourceHandle="output",
                    targetHandle="input"
                ))

        # 4. Validate all required inputs satisfied
        if not self._all_inputs_satisfied(node_metadata, edges):
            raise IncompatibleNodesError(
                nodes=nodes,
                reason="Cannot create valid chain - missing required connections"
            )

        return edges

    def _generate_flow_data(self,
                           nodes: List[str],
                           edges: List[Edge],
                           parameters: Dict) -> Dict:
        """
        Generate complete flowData with visual positioning.

        WHY: Follows spec clarification for node positioning algorithm
        ALGORITHM:
        1. Assign nodes to columns by connection depth (inputs=0, direct connections=1, etc.)
        2. Space nodes vertically within each column (200px apart)
        3. Space columns horizontally (300px apart)
        RESULT: Left-to-right flow pattern, standard flowchart convention
        """
        # 1. Calculate connection depth for each node
        node_columns = self._calculate_connection_depth(nodes, edges)

        # 2. Position nodes
        positioned_nodes = []
        column_y_offsets = {}  # Track vertical position within each column

        for node_name in nodes:
            column = node_columns[node_name]
            y_offset = column_y_offsets.get(column, 0)

            positioned_nodes.append({
                "id": node_name,
                "type": self._get_node_type(node_name),
                "position": {
                    "x": column * 300,  # 300px horizontal spacing
                    "y": y_offset
                },
                "data": self._get_node_config(node_name, parameters)
            })

            column_y_offsets[column] = y_offset + 200  # 200px vertical spacing

        return {"nodes": positioned_nodes, "edges": [e.dict() for e in edges]}
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 2 Catalog Service →](05-layer2-catalog-service.md)
