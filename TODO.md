# Eisenhower Matrix Todo App Development

## Overview
Create a functional todo app that allows users to input tasks, assign priorities based on the Eisenhower Matrix principles (Urgent/Important), and automatically rank tasks. The app now also supports an extended multi-factor priority scoring model (urgency, importance, impact, value alignment, effort penalty, due date bonus) with runtime-adjustable weights.

## Development Tasks

### Backend Development
- [x] Set up database models for tasks
  - [x] Create Task model with fields: title, description, urgency, importance, created_at, updated_at
  - [x] Add extended fields: impact, value_alignment, effort, due_date, priority_score
  - [x] Add database connection and setup
- [x] Implement CRUD API endpoints
  - [x] POST /tasks - Create new task
  - [x] GET /tasks - List all tasks with ranking
  - [x] PUT /tasks/{id} - Update task
  - [x] DELETE /tasks/{id} - Delete task
- [x] Add task prioritization logic
  - [x] Implement multi-factor scoring algorithm (weighted + effort penalty + due soon bonus)
  - [x] Automatic ranking system
- [x] Eisenhower Matrix classification endpoint
  - [x] GET /tasks/matrix - Return tasks grouped by quadrant
- [x] Runtime configuration endpoints
  - [x] GET /config/priority - View active weights & parameters
  - [x] PUT /config/priority - Override selected weights
  - [x] DELETE /config/priority - Reset overrides
- [ ] Introduce proper database migrations (Alembic)
- [ ] Data migration script to backfill new fields on existing rows (nullable safeguards)
- [ ] Add server-side validation & normalization (clamp scales 1-10, non-negative effort)
- [ ] Add pagination & filtering to GET /tasks
- [ ] Add search (title/description LIKE)
- [ ] Implement soft delete (deleted_at) or archival endpoint (optional)
- [ ] Add bulk operations (bulk create / bulk update / bulk delete)
- [ ] Add background recalculation task if future scoring becomes heavier
- [ ] Caching layer (memoize score if inputs unchanged) (optional)
- [ ] Add health endpoints: GET /health/liveness, /health/readiness
- [ ] Add OpenAPI tags & improved descriptions/examples
- [ ] Structured logging (request id correlation)
- [ ] Error handling middleware with consistent error envelope
- [ ] Rate limiting or simple abuse protection on config endpoints
- [ ] Input sanitation & length constraints
- [ ] Add seed script for demo data
- [ ] Add export endpoint (CSV / JSON of tasks)
- [ ] Add import endpoint (validate & bulk insert)

### Frontend Development
- [x] Create task input form
  - [x] Task title and description fields
  - [x] Urgency scale input (1-10)
  - [x] Importance scale input (1-10)
  - [x] Added inputs: impact, value alignment, effort, due date
  - [x] Form validation (basic)
- [x] Implement task list display
  - [x] Show tasks ranked by priority score
  - [x] Display urgency and importance values
  - [x] Display extended scoring factors
  - [x] Add edit/delete functionality
- [x] Build Eisenhower Matrix visualization
  - [x] 2x2 grid layout
  - [x] Position tasks based on urgency/importance
  - [x] Interactive (click for details)
  - [x] Color coding for quadrants
- [ ] Inline edit / modal for task updates
- [ ] Client-side validation enhancements (range, required, date logic)
- [ ] Loading skeletons & optimistic UI updates
- [ ] Quadrant filters & quick hide/show toggles
- [ ] Drag-and-drop to move tasks between quadrants (updates urgency/importance)
- [ ] Sort & secondary grouping options (by score, due date)
- [ ] Adjustable weight controls UI (read & update runtime config)
- [ ] Visual explanation tooltip of scoring formula
- [ ] Due soon highlighting (e.g., < 48h)
- [ ] Accessibility audit (ARIA roles, keyboard navigation)
- [ ] Responsive matrix enhancements (mobile stacked view)
- [ ] Dark mode / theme toggle
- [ ] Error boundary component
- [ ] Toast notifications system
- [ ] State management refactor (Context or lightweight store) if complexity grows
- [ ] Add TypeScript (migration) or at least prop-types
- [ ] Unit & integration tests (Jest + React Testing Library)
- [ ] Lighthouse performance & a11y pass

### Integration & Polish
- [x] Connect frontend to backend API
- [x] Add responsive design basics
- [x] Implement basic error handling
- [x] Add loading states
- [ ] Test the complete workflow end-to-end
- [ ] Add contract tests (API schema vs. frontend expectations)
- [ ] Add smoke test script (CI) to start services & hit key endpoints
- [ ] Generate and display OpenAPI docs link in README/UI

### Quality & Testing
- [ ] Backend unit tests coverage (models, scoring, routers edge cases)
- [ ] Backend integration tests (CRUD, matrix, config overrides) - (written but not yet validated in clean run)
- [ ] Add test matrix (Python versions) in CI
- [ ] Frontend component tests
- [ ] Frontend integration (render + API mock) tests
- [ ] End-to-end tests (Playwright / Cypress) for core flows
- [ ] Performance test (large task dataset) to ensure acceptable latency
- [ ] Load test basic (locust / k6) (optional)

### Deployment & DevOps
- [ ] Finalize Docker configuration (multi-stage, production images slim)
- [ ] Add non-root user in containers
- [ ] Add healthcheck in Dockerfile / docker-compose
- [ ] Parameterize scoring weights via .env with documented defaults
- [ ] Provide .env.example
- [ ] Add Makefile or task runner for common commands
- [ ] CI pipeline (GitHub Actions): lint, test, build images, push
- [ ] Dependency scanning (pip + npm audit) in CI
- [ ] Image scanning (Trivy / Grype) (optional)
- [ ] Version tagging & changelog generation
- [ ] Production deployment manifest (e.g., docker-compose.prod or Kubernetes manifests) (optional)
- [ ] Add backup/restore scripts for database
- [ ] Implement Alembic migrations CI safety check
- [ ] Automatic pre-commit hooks (format, lint, type check)

### Documentation
- [ ] Expand README with: setup, run, tests, config table, scoring formula explanation (partially done – refine)
- [ ] API documentation section or link to /docs
- [ ] Architectural overview diagram
- [ ] Data model diagram (task fields & relationships)
- [ ] CONTRIBUTING.md
- [ ] CHANGELOG.md
- [ ] LICENSE file
- [ ] ADRs for key decisions (scoring algorithm, runtime overrides)
- [ ] Add inline code comments where logic is non-obvious

### Security & Observability
- [ ] CORS configuration tighten (allowed origins list)
- [ ] Input size limits & request body limits
- [ ] Rate limiting (config endpoints especially)
- [ ] Authentication / authorization (future: user accounts, per-user tasks)
- [ ] Add logging (structured JSON) & correlation IDs
- [ ] Add metrics (Prometheus / OpenTelemetry) for request latency & scoring counts
- [ ] Add tracing instrumentation (optional)
- [ ] Add Sentry or similar error tracking (optional)
- [ ] Periodic dependency update strategy

### Data & Future Features (Backlog)
- [ ] User accounts & multi-tenancy (per-user task segregation)
- [ ] Tagging / categories for tasks
- [ ] Recurring tasks & auto-generation
- [ ] Notifications/reminders (email/push) for urgent tasks
- [ ] Historical score tracking / trends
- [ ] Analytics dashboard (distribution, average score, quadrant shifts over time)
- [ ] Bulk import from CSV / Trello / Jira (mapping)
- [ ] API keys for external integrations
- [ ] Websocket / SSE for real-time updates
- [ ] Offline-first (frontend caching / service worker)

## Current Status
- [x] Basic project structure created
- [x] Docker setup configured (needs hardening & refinement)
- [x] Backend API endpoints
- [x] Frontend components
- [x] Extended task prioritization logic
- [x] Visual matrix display
- [ ] Stable container runtime (resolving encoding/null-byte issues)  
- [ ] Automated test suite green in clean environment

## Known Issues / Technical Debt
- [ ] Intermittent file encoding/null-byte corruption – add root-cause analysis & guard script CI check
- [ ] Missing migrations (schema drift risk)
- [ ] No authentication (all tasks global)
- [ ] Limited validation (potential inconsistent data)
- [ ] Lack of pagination may cause slow responses with large datasets

## Next Immediate Steps (High Priority)
1. Stabilize backend & frontend runtime (resolve file encoding/null-byte issues)
2. Run & fix backend tests; add coverage gating
3. Implement Alembic migrations & backfill script
4. Add adjustable weights UI & connect to config endpoints
5. Add frontend & backend test automation in CI pipeline

## Stretch Goals (After Stabilization)
- Real-time updates (websocket)
- Drag-and-drop quadrant repositioning
- User accounts & per-user data isolation
- Analytics dashboard & trends

