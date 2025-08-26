# Eisenhower Matrix Todo App

This is a full-stack application that allows users to create and manage their tasks using the Eisenhower Matrix. The frontend is built with React, and the backend is a FastAPI application. The entire application is containerized using Docker.

## Development Environments

The application is configured to run in three different environments:

- **development**: For local development and testing.
- **staging**: For pre-production testing.
- **production**: For the live application.

The application uses different Dockerfile targets and environment variables for each environment.

### Branching Strategy

The project uses the following branching strategy:

- **main**: The main branch, which reflects the production-ready code.
- **stage**: The staging branch, used for pre-production testing.
- **dev**: The development branch, where new features are developed.

## Getting Started

To run the application, you need to have Docker and Docker Compose installed.

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    ```

2.  **Switch to the desired branch:**

    -   For development: `git checkout dev`
    -   For staging: `git checkout stage`
    -   For production: `git checkout main`

3.  **Create an environment file:**

    Create a `.env` file in the root of the project and copy the contents of the appropriate environment file (`.env.development`, `.env.staging`, or `.env.production`).

4.  **Build and run the application:**

    ```bash
    docker-compose up --build
    ```

The frontend will be available at `http://localhost:3000`, and the backend will be available at `http://localhost:8000`.

## Priority Scoring

Tasks accept the following scoring inputs (1-10 scales unless noted):
- urgency
- importance
- impact (expected positive outcome)
- value_alignment (alignment with your goals/values)
- effort (cost; penalizes score)
- due_date (ISO datetime; boosts score as deadline nears)

Backend scoring formula (conceptual):
1. Normalize positive drivers to 0..1 and compute weighted average.
2. Apply effort penalty: `score *= (1 - effort_penalty * effort_norm)`.
3. Apply due date bonus if within `DUE_SOON_DAYS` window: multiplicative up to `DUE_SOON_MAX_BONUS`.
4. Scale to 0..100.

Environment-configurable weights (defaults shown):
```
WEIGHT_URGENCY=0.30
WEIGHT_IMPORTANCE=0.30
WEIGHT_IMPACT=0.20
WEIGHT_VALUE=0.20
EFFORT_PENALTY=0.15
DUE_SOON_DAYS=5
DUE_SOON_MAX_BONUS=0.15
```
Adjust these in `docker-compose.yml` or deployment environment variables; restart backend for changes.

### Runtime Reconfiguration
You can inspect or adjust the in-memory scoring parameters without restarting the service via the configuration API:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/config/priority` | Current effective priority configuration |
| PUT | `/api/config/priority` | Override one or more parameters (JSON body with any subset) |
| DELETE | `/api/config/priority/overrides` | Clear overrides, revert to environment values |

Example body for PUT:
```json
{
  "weight_urgency": 0.4,
  "weight_importance": 0.35,
  "effort_penalty": 0.2
}
```

Overrides persist only in memory until the backend restarts.
