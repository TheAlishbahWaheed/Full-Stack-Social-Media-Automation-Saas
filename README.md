# SocialFlow — Advanced Social Media Command Center

A polished full-stack social content management SaaS built with **Next.js 15 + TypeScript + Tailwind**, **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **JWT authentication**.

## What is improved

- Modern responsive SaaS dashboard with persistent sidebar and command-center layout.
- JWT-protected authentication with stronger password validation.
- Post composer with platform selection, character counter and scheduling.
- Full post lifecycle: draft → scheduled → published.
- Search and status filters for the content library.
- Edit, duplicate, publish and delete actions.
- Upcoming scheduled-content queue.
- Workspace analytics: total, drafts, scheduled, published and connected accounts.
- Social account CRUD with duplicate protection.
- Profile settings and protected routes.
- API validation and consistent frontend error handling.
- Lightweight development migration for the new post/account fields.
- Health endpoint and versioned API metadata.

## Important platform integration note

The current account connection layer is a **workspace-level account registry**. It does not claim to publish to Instagram, Facebook, LinkedIn, X or TikTok without OAuth credentials and approved platform API access.

To turn this into a production automation platform, add OAuth adapters for each platform, encrypted token storage, refresh-token rotation, a background job queue (for example Celery/RQ/Arq), retry policies, rate-limit handling, and a scheduler/worker process.

## Run locally

### 1. Start PostgreSQL

```bash
docker compose up -d db
```

### 2. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
copy .env.example .env.local   # Windows
# cp .env.example .env.local   # macOS/Linux

npm run dev
```

Open http://localhost:3000.

## Verification

- Backend Python modules compile successfully with `python -m compileall -q app`.
- Frontend TypeScript passes `tsc --noEmit`.
- `next build` requires the matching Next.js SWC binary; if it is not already cached, run `npm install` on a machine with internet access before building.

## Production roadmap

1. OAuth 2.0 for each social platform.
2. Encrypt OAuth access/refresh tokens at rest.
3. Add Alembic migrations instead of the lightweight development migration.
4. Add Redis + a worker for reliable scheduled publishing.
5. Add media uploads and object storage.
6. Add team workspaces, roles and permissions.
7. Add audit logs, rate limits, observability and automated tests.
