# FleetFlow – Modular Fleet & Logistics Management System

A full-stack, real-time fleet management system with role-based access (Fleet Manager, Dispatcher, Safety Officer, Financial Analyst), built for hackathon-grade production use.

## Tech Stack

- **Frontend:** React 18, Vite, TypeScript, TailwindCSS, React Router, Axios
- **Backend:** Node.js, Express, TypeScript, PostgreSQL, Prisma ORM, JWT, RBAC
- **Validation:** Zod (backend), controlled forms + validation (frontend)

## Prerequisites

- Node.js 18+
- PostgreSQL 14+
- npm or pnpm

## Environment Setup

### Backend

1. Copy environment file and set variables:

```bash
cd backend
cp .env.example .env
```

2. Edit `backend/.env`:

- `DATABASE_URL`: PostgreSQL connection string, e.g.  
  `postgresql://USER:PASSWORD@localhost:5432/fleetflow?schema=public`
- `JWT_SECRET`: Strong secret for JWT signing (change in production)
- `PORT`: API port (default `3001`)

### Frontend

Frontend uses Vite proxy to `/api` → `http://localhost:3001`. No env file required for local run.

## Database & Seed

From `backend`:

```bash
npm install
npx prisma generate
npx prisma db push
npm run db:seed
```

Seed creates four users (same password for all: `password123`):

| Email                    | Role              |
|--------------------------|-------------------|
| manager@fleetflow.com    | Fleet Manager     |
| dispatcher@fleetflow.com | Dispatcher        |
| safety@fleetflow.com     | Safety Officer    |
| finance@fleetflow.com   | Financial Analyst |

Plus sample vehicles, drivers, one draft trip, and sample maintenance/fuel/expense logs.

## Run Locally

**Terminal 1 – API**

```bash
cd backend
npm run dev
```

API: http://localhost:3001

**Terminal 2 – Frontend**

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

Log in with any seed user (e.g. `manager@fleetflow.com` / `password123`). Navigation is role-based; each role sees only allowed pages.

## Project Structure

```
/frontend
  /src
    /components    # Reusable UI (Button, Input, Card, Loading, ErrorMessage)
    /pages        # Login, Dashboard, Vehicles, Trips, Maintenance, Fuel, Drivers, Analytics
    /layouts      # AppLayout (sidebar + role-based nav)
    /routes       # React Router + private route
    /services     # API clients (auth, dashboard, vehicles, drivers, trips, etc.)
    /hooks        # useAuth
    /types        # Shared TS types

/backend
  /src
    /controllers  # Request handlers
    /routes       # Express routers (auth, dashboard, vehicles, drivers, trips, maintenance, fuel, expenses, analytics)
    /services     # Business logic
    /middlewares  # auth, RBAC, validate, errorHandler
    /validators   # Zod schemas
    /utils        # prisma, errors
  /prisma
    schema.prisma
    seed.ts
  API.md          # API reference
```

## API Overview

- **Auth:** `POST /api/auth/login`, `POST /api/auth/register`
- **Dashboard:** `GET /api/dashboard/kpis`, `GET /api/dashboard/filters`
- **Vehicles:** CRUD + `GET /api/vehicles/available`
- **Drivers:** CRUD + `GET /api/drivers/available`
- **Trips:** CRUD, lifecycle Draft → Dispatched → Completed / Cancelled
- **Maintenance:** List, create, `POST /api/maintenance/release-vehicle/:vehicleId`
- **Fuel:** List, create
- **Expenses:** List, create
- **Analytics:** `GET /api/analytics/fuel-efficiency`, `vehicle-roi`, `reports-summary`

All protected routes require header: `Authorization: Bearer <JWT>`.

See `backend/API.md` for full API documentation.

## Features Checklist

- Real-time/dynamic data from backend APIs (no static JSON for dashboards/tables)
- Responsive UI (Tailwind), consistent spacing and typography
- Frontend + backend validation (Zod), clear error messages
- Sidebar navigation with role-based menu and breadcrumbs/section headers
- Git-friendly, modular structure (auth, vehicles, trips, analytics, etc.)
- PostgreSQL + Prisma, JWT + RBAC, loading and error states, CSV/PDF export for reports

## License

MIT.
