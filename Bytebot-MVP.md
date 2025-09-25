# Bytebot MVP Mastery Plan

## Overview
This document captures a comprehensive, English-language roadmap for recreating a minimal viable product of Bytebot while following Karpathy's Philosophy of Mastery. The plan emphasizes building a tightly scoped, end-to-end agent, surfacing bottlenecks through runnable milestones, and extracting durable lessons via executable artifacts. Every phase below expands significantly on the earlier high-level outline, providing detailed goals, deliverables, feedback loops, and reflective practices tailored for a Windows-based automation agent.

## Learning Objectives and Strategy
- **Master Agent Construction Through Practice:** Recreate a simplified Bytebot that can execute desktop automation tasks on Windows, ensuring the agent pipeline—from natural language intent to deterministic action execution—is fully understood.
- **Apply Karpathy’s Loop:** Iterate through cycles of building the smallest working slice, identifying the most painful bottleneck, learning the minimum theory to break through, and codifying the knowledge in code, tests, documentation, and demos.
- **Ruthless Scope Management:** Retain only the agent-critical capabilities (planning, execution, feedback) while postponing non-essential features such as multi-user management, distributed services, or polished UI.
- **Executable Explanations:** Produce code, automated tests, structured notes, and demonstrable recordings for each milestone, ensuring that understanding is explicit and transferrable.
- **Personal Baselines and Improvement Tracking:** Define measurable metrics—task success rate, latency, failure diagnosis quality—to enable longitudinal self-comparison rather than benchmarking against others.

## Phase 0: Scout the Existing System (Week 1)
### 0.1 Deploy the Reference Bytebot Stack
- Spin up the official Bytebot using Docker or Railway to gain a concrete grasp of its architecture. Document every dependency, environment variable, service port, and security consideration encountered during the deployment.
- Run connectivity tests against the core endpoints (e.g., `/tasks`, `/status`) and record response payloads to understand data contracts.
- Deliverables:
  - A reproducible deployment script or PowerShell instructions.
  - Terminal session logs confirming that the API and desktop agent communicate successfully.
  - A short screen recording demonstrating an end-to-end task invocation in the original Bytebot.

### 0.2 Produce a White-Box Architectural Map
- Decompose the system into its primary services: desktop agent, planner/LLM orchestrator, web UI, database, and message brokers.
- Reverse-engineer how data flows between components, including authentication headers, task schemas, and streaming updates.
- Mark which components the MVP will imitate, which will be replaced by simplified modules, and which will be explicitly deferred.
- Deliverables:
  - A detailed diagram (Mermaid or vector graphics) illustrating services, protocols, and event flows.
  - A narrative document annotating each module’s responsibilities and proposed MVP equivalent.

### 0.3 Establish Personal Baselines
- Manually perform a representative desktop automation task (e.g., “Open Notepad, type ‘Hello World’, save to Desktop”) while tracking elapsed time, error rate, and cognitive load.
- Define success metrics for the MVP such as completion time under two minutes, at least 80% task success rate, and meaningful error reporting when failures occur.
- Deliverables:
  - A measurement log with timestamps and qualitative observations.
  - A baseline report summarizing manual performance and target metrics for automation.

## Phase 1: MVP v0 – Minimal Action Replayer (Weeks 2–4)
### 1.1 Build the Desktop Execution Core
- Set up a Windows 10/11 development environment with Python 3.11+, Git, and PowerShell 7. Configure a virtual environment with dependencies limited to automation essentials (`pywinauto`, `uiautomation`, `pyautogui`, `Pillow`).
- Write raw Python scripts to control Notepad: launching processes, focusing windows, injecting keystrokes, and capturing screenshots. Document pitfalls such as UI access permissions, timing constraints, and DPI scaling issues.
- Deliverables:
  - `experiments/notepad_macro.py` demonstrating manual scripting capabilities.
  - `notes/desktop-probe.md` chronicling issues, resolutions, and open questions.

### 1.2 Implement a Scriptable Task Pipeline
- Define data classes for `Action` and `ActionSequence`, capturing command type, parameters, preconditions, and expected outcomes.
- Implement a YAML/JSON loader that converts declarative step lists into executable routines. Support core primitives: `launch_app`, `click`, `type_text`, `save_file`, `capture_screenshot`.
- Introduce logging with timestamps and levels (INFO/WARN/ERROR) to record action start, result, and artifact paths.
- Deliverables:
  - `mvp/agent/actions.py` defining the action schema.
  - `mvp/runtime/pipeline.py` executing sequences with structured logging.
  - Sample task definitions in `templates/` covering Notepad workflows.

### 1.3 Design Tests and Feedback Loops
- Unit Tests: Mock automation backends to validate that each action issues the correct API calls and handles exceptions gracefully.
- Integration Test: Run the Notepad flow on an instrumented Windows VM, capturing logs and screenshots to verify deterministic behavior.
- Feedback: After each test run, review logs to identify race conditions (e.g., window focus delays) and adjust retry logic.
- Deliverables:
  - `tests/test_actions.py` ensuring action serialization/deserialization integrity.
  - `tests/test_pipeline.py` verifying sequential execution and error propagation.
  - Screen recording demonstrating the pipeline completing the Notepad task without manual intervention.

### 1.4 Reflect and Document Learning
- Summarize key insights about desktop automation—window handles, keyboard events, synchronization strategies—in a README section.
- Note unresolved issues and hypotheses for future iterations.
- Deliverables:
  - Updated project README with an “Automation Lessons Learned” subsection.
  - Annotated log excerpts highlighting failure diagnostics.

## Phase 2: MVP v1 – Planning and Task Interfaces (Weeks 5–8)
### 2.1 Expose a Task Intake API and Queue
- Build a lightweight REST interface (FastAPI or Flask) with a `/tasks` endpoint accepting natural language requests or structured action scripts.
- Implement an in-memory task queue ensuring sequential processing, basic prioritization, and state transitions (PENDING → RUNNING → SUCCEEDED/FAILED).
- Deliverables:
  - `mvp/cli/main.py` enabling command-line submission and inspection of tasks.
  - `mvp/api/server.py` handling HTTP requests with validation and JSON responses.
  - Postman or curl scripts verifying the API contract.

### 2.2 Develop a Rule-Based Planner
- Craft a keyword and slot-extraction engine that maps natural language instructions to action templates. For example, detect verbs like “open”, “type”, “save” and objects like “Notepad”, “Desktop”.
- Maintain a library of task templates with parameter placeholders. Use lightweight parsing (regex or spaCy) to fill slots.
- Ensure the planner outputs a normalized `ActionSequence` compatible with the execution pipeline. Provide a `--dry-run` option to preview the generated plan before execution.
- Deliverables:
  - `mvp/planner/rule_based.py` implementing the planner interface.
  - `templates/notepad_write.yaml` demonstrating parameterized scripts.
  - `tests/test_planner.py` covering intent detection and error handling (e.g., missing application).

### 2.3 Implement Feedback and Monitoring Channels
- Design structured logs capturing task ID, action index, status, and artifacts (screenshots, error messages). Store logs under `runtime/logs/<task_id>.log` and screenshots under `runtime/screenshots/<timestamp>.png`.
- Provide a simple dashboard—CLI summary or minimal HTML page—showing task progression and linking to artifacts.
- Deliverables:
  - `mvp/runtime/reporting.py` aggregating logs into human-readable summaries.
  - Demo video walking through the submission of a task and inspection of its outputs.

### 2.4 Targeted Learning Interventions
- When planner rules become unwieldy (e.g., ambiguous language), study intent classification techniques, finite-state machines, and simple natural language understanding methods.
- Document each learning session with references, distilled takeaways, and how the knowledge was applied in code.
- Deliverables:
  - `notes/planner.md` cataloging failure cases, theoretical insights, and subsequent fixes.
  - Commit messages linking theory updates to concrete code changes.

## Phase 3: MVP v2 – LLM-Driven Planning and Multimodal Feedback (Weeks 9–14)
### 3.1 Integrate a Language Model Planner
- Abstract the planner interface to allow swapping implementations. Introduce `LLMPlanner` that calls an API (OpenAI, Anthropic, or self-hosted) with carefully engineered prompts describing available actions and constraints.
- Implement guardrails such as output validation, schema enforcement, and maximum step limits to prevent runaway plans.
- Deliverables:
  - `mvp/planner/base.py` defining the planner contract.
  - `mvp/planner/llm.py` wrapping the chosen LLM provider.
  - Prompt templates stored under `prompts/` with comments explaining context windows and safety measures.

### 3.2 Add Environment Understanding
- Incorporate screenshot analysis or OCR to provide the planner with situational awareness. Start with template or pixel matching before escalating to OCR libraries like Tesseract.
- Feed summarized observations (e.g., window titles, button labels) back into the planner to enable conditional logic.
- Deliverables:
  - `mvp/vision/ocr.py` or `mvp/vision/template_match.py` implementing perception utilities.
  - Integration tests ensuring perception outputs are deterministic on sample screenshots.

### 3.3 Enhance Error Recovery and Control Flow
- Allow the runner to detect failure patterns (e.g., window not found) and request planner revisions or retries with back-off strategies.
- Implement rollback or cleanup actions when tasks fail (closing stray windows, deleting incomplete files).
- Deliverables:
  - `mvp/runtime/recovery.py` defining retry heuristics and recovery suggestions.
  - Test scenarios simulating transient failures to validate recovery logic.

### 3.4 Build an Automated Evaluation Harness
- Curate a suite of benchmark tasks spanning text editing, web browsing, and file manipulation. Automate repeated execution to generate success metrics, average step counts, and regression detections.
- Visualize results over time to measure improvements from rule-based to LLM-driven planners.
- Deliverables:
  - `scripts/run_benchmark.py` executing the benchmark set and emitting JSON reports.
  - `reports/weekly.md` summarizing metrics, lessons, and next steps for each iteration.

### 3.5 Externalize Knowledge Through Teaching
- After each major bottleneck is overcome, produce a blog post, recorded walkthrough, or internal tech talk to articulate the problem, solution, and trade-offs. Emphasize explaining concepts in your own words to expose gaps and reinforce understanding.
- Deliverables:
  - `docs/executable-notes/` containing narrative explanations with code snippets and diagrams.
  - Links to videos or slide decks if applicable.

## Phase 4: Extension and Comparative Analysis (Ongoing)
### 4.1 Align with Advanced Bytebot Capabilities
- Systematically compare the MVP with the full Bytebot feature set (multi-session handling, MCP, security sandboxing). Prioritize the next capabilities to port based on observed deficiencies or ambition.
- Design experiments to insert your modules into Bytebot or to plug Bytebot components into your MVP, validating interoperability and identifying integration challenges.
- Deliverables:
  - A capability gap matrix mapping current vs. target features.
  - Experiment logs documenting integration attempts and findings.

### 4.2 Maintain Longitudinal Progress Tracking
- Keep a changelog enumerating each iteration’s improvements, regressions, and unresolved issues.
- Periodically revisit baseline metrics to quantify progress, noting how success rates and latency improve across versions.
- Deliverables:
  - `CHANGELOG.md` with dated entries for major milestones.
  - Quarterly retrospective notes analyzing trends and setting new goals.

## Meta Practices Embedded Throughout
- **Tight Feedback Cycles:** Every feature branch must include automated tests and, when relevant, toy benchmarks to provide immediate signal on correctness and performance.
- **Dependency Discipline:** Implement minimal viable versions of components yourself before adopting third-party libraries, ensuring foundational understanding of planner logic, execution control, and perception.
- **Executable Artifacts:** For each milestone, produce the quartet of deliverables—code, tests, explanatory notes, and demos—so that knowledge is preserved in runnable form.
- **Reflective Documentation:** Use READMEs, notebooks, or recorded summaries to teach the learned material back to yourself, converting tacit intuition into explicit knowledge.
- **Scope Guardrails:** Continually reassess feature creep. If a module cannot be validated with closed-form tests in the current iteration, defer it and focus on finishable MVP slices.

## Expected Outcomes
By following this expanded plan, you will:
- Acquire hands-on mastery over agent design, from deterministic rule-based planners to LLM-guided orchestration.
- Develop a pragmatic understanding of Windows desktop automation, including synchronization, perception, and error recovery challenges.
- Establish a repeatable learning loop where experimentation drives theory acquisition, and teaching solidifies insights.
- Produce a robust body of executable documentation that can be reused in future projects or shared with collaborators, accelerating your growth as an agent engineer.

