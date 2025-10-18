# Layer 2: Circuit Breaker & Workflow Services

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: CircuitBreakerService and SpecDrivenWorkflowService

---

## CircuitBreakerService (circuit_breaker_service.py)

```python
class CircuitBreakerService:
    """
    Service for managing circuit breakers per dependency.

    WHY: Prevents cascading failures, resource waste during outages
    PATTERN: Circuit Breaker (industry-standard for distributed systems)
    STATES: CLOSED (normal), OPEN (blocking), HALF_OPEN (testing recovery)
    """

    def __init__(self, state_persistence_path: str):
        self.circuits: Dict[str, CircuitBreaker] = {
            "flowise_api": CircuitBreaker("flowise_api", failure_threshold=3, timeout_seconds=300),
            "vector_db": CircuitBreaker("vector_db", failure_threshold=3, timeout_seconds=300),
            "embedding_model": CircuitBreaker("embedding_model", failure_threshold=3, timeout_seconds=300)
        }
        self.state_persistence_path = state_persistence_path
        # Load persisted state to survive restarts per NFR-083
        self._load_state()

class CircuitBreaker:
    """
    Circuit breaker for single dependency.

    WHY: Tracks failure count, manages state transitions, provides clear status
    TRANSITIONS:
    - CLOSED → OPEN: After 3 consecutive failures
    - OPEN → HALF_OPEN: After 5-minute timeout
    - HALF_OPEN → CLOSED: On successful test request
    - HALF_OPEN → OPEN: On failed test request
    """

    async def call(self, func: Callable, *args, **kwargs):
        """
        Execute function with circuit breaker protection.

        WHY: Prevents wasted retries, provides transparency
        ERROR HANDLING: Only counts transient errors (network, timeout, 5xx) not validation (4xx)
        """
        # Check if circuit should transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"{self.dependency_name} circuit: OPEN → HALF_OPEN (testing recovery)")
            else:
                time_remaining = self._time_until_retry()
                raise CircuitOpenError(self.dependency_name, time_remaining)

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except (NetworkError, TimeoutError, ServerError) as e:
            self._on_failure(e)
            raise

    def _on_success(self):
        """Reset failure count on successful operation"""
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            logger.info(f"{self.dependency_name} circuit: HALF_OPEN → CLOSED (recovery confirmed)")

    def _on_failure(self, error: Exception):
        """Increment failure count and open circuit if threshold reached"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.circuit_opened_time = datetime.now()
            logger.warning(
                f"{self.dependency_name} circuit: CLOSED → OPEN "
                f"(failure threshold {self.failure_threshold} reached)"
            )
```

---

## SpecDrivenWorkflowService (workflow_service.py)

```python
class SpecDrivenWorkflowService:
    """
    Service for complex chatflow requests requiring human validation.

    WHY: Complex/novel flows need spec → clarify → plan → approve workflow
    INTEGRATION: Uses .specify/commands/* (speckit) for structured phases
    MAX QUESTIONS: 5 per spec clarification phase
    """

    async def analyze_complexity(self, user_request: str) -> ComplexityAnalysis:
        """
        Determine if request needs spec-driven workflow.

        WHY: Routes complex requests to human-validated workflow
        CRITERIA (from spec):
        - >5 nodes or >3 node types
        - Keywords: agent, multi-step, conditional, routing, decision
        - Novel use case (template match confidence <70%)
        - Multiple integrations
        - User explicitly asks for complex/advanced/custom
        PERFORMANCE: <1s per NFR-018
        """
        node_count_estimate = self._estimate_node_count(user_request)
        keywords = self._detect_complexity_keywords(user_request)
        template_match = await self._search_templates(user_request)

        requires_sdd = (
            node_count_estimate > 5 or
            len(keywords) > 0 or
            template_match.confidence < 0.7
        )

        return ComplexityAnalysis(
            requires_spec_driven=requires_sdd,
            confidence_score=self._calculate_confidence(...),
            reasoning=f"Detected {node_count_estimate} nodes, keywords: {keywords}"
        )

    async def execute_workflow(self, user_request: str) -> WorkflowResponse:
        """
        Execute spec-driven workflow phases with user validation.

        WHY: Provides structured approach with quality gates
        PHASES: specify → clarify → plan → tasks → analyze → approve
        HUMAN-IN-THE-LOOP: Clarification answers, design approval
        PERFORMANCE: <2 minutes (excluding user wait time) per NFR-021
        """
        # Phase 1: specify - generate chatflow specification
        spec = await self._run_speckit_specify(user_request)

        # Phase 2: clarify - ask max 5 questions to resolve ambiguities
        clarifications = await self._run_speckit_clarify(spec, max_questions=5)

        # Phase 3: plan - break down into implementation phases
        plan = await self._run_speckit_plan(spec)

        # Phase 4: tasks - generate detailed task breakdown
        tasks = await self._run_speckit_tasks(plan)

        # Phase 5: analyze - validate consistency
        analysis = await self._run_speckit_analyze(spec, plan, tasks)

        # Phase 6: present design for user approval
        design = self._generate_design_summary(spec, plan, tasks)

        return WorkflowResponse(
            design=design,
            awaiting_approval=True,
            token_usage=self._calculate_token_usage()
        )
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 3 Clients →](07-layer3-clients.md)
