# SocialFlow — Beginner Full-Stack Social Automation SaaS

Beginner-friendly foundation using Next.js/React/TypeScript/Tailwind, FastAPI, PostgreSQL and REST APIs.

Features: registration/login, JWT auth, protected dashboard, profile settings, social-account CRUD, post CRUD, basic scheduling, validation/error handling.

Intentionally excluded: Meta/WhatsApp APIs, OAuth, WebSockets, multi-tenancy and advanced automation.

## Run

### PostgreSQL
`docker compose up -d db`

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# copy .env.example .env
uvicorn app.main:app --reload
```
API: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
# copy .env.example .env.local
npm run dev
```
Open http://localhost:3000.

## Learning order
1. Models/database → schemas → API routes → JWT → frontend API client → dashboard.
2. Next: Alembic migrations, real OAuth, platform APIs, background scheduler and queues.
