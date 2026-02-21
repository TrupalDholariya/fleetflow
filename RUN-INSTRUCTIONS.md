# FleetFlow – Step-by-step run instructions

FleetFlow uses **PostgreSQL** (not Oracle). Prisma ORM does not support Oracle, so the app cannot connect to Oracle Database 21c as-is. You can keep Oracle for other work and run PostgreSQL only for this project.

---

## Choose how to run PostgreSQL

### A) Using Docker (easiest – no PostgreSQL install)

If you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed:

1. Open a terminal and run **once** (creates a PostgreSQL 15 container and database):

   **Windows (PowerShell or CMD):**
   ```bash
   docker run -d --name fleetflow-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fleetflow -p 5432:5432 postgres:15-alpine
   ```

2. Use this in your backend `.env` (see Step 3 below):
   ```env
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fleetflow?schema=public"
   ```

3. When you’re done working, stop the DB:
   ```bash
   docker stop fleetflow-db
   ```
   Start it again later with:
   ```bash
   docker start fleetflow-db
   ```

---

### B) Install PostgreSQL 14+ on your PC

You can have both Oracle and PostgreSQL: Oracle uses port **1521**, PostgreSQL uses **5432**.

1. Download and install from: https://www.postgresql.org/download/windows/
2. During setup, set a password for the `postgres` user and remember it.
3. Create the database (e.g. in pgAdmin or `psql`):
   ```sql
   CREATE DATABASE fleetflow;
   ```
4. In backend `.env` use (replace `YOUR_POSTGRES_PASSWORD` with the password you set):
   ```env
   DATABASE_URL="postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/fleetflow?schema=public"
   ```

---

## Step-by-step: run FleetFlow

### Step 1: Start PostgreSQL

- **Docker:** Run the `docker run` command from section A above (or `docker start fleetflow-db` if you already created the container).
- **Installed PostgreSQL:** Make sure the PostgreSQL service is running (e.g. from Windows Services or from the Start menu).

---

### Step 2: Backend – env and dependencies

1. Open a terminal and go to the backend folder:
   ```bash
   cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\backend
   ```

2. Create your env file:
   ```bash
   copy .env.example .env
   ```

3. Open `backend\.env` in Notepad or VS Code and set:
   - **DATABASE_URL**  
     - Docker: `postgresql://postgres:postgres@localhost:5432/fleetflow?schema=public`  
     - Installed PostgreSQL: `postgresql://postgres:YOUR_PASSWORD@localhost:5432/fleetflow?schema=public`
   - **JWT_SECRET** – any long random string (e.g. `my-secret-key-123`)
   - **PORT** – leave as `3001` if you want the API on 3001

4. Install packages and create DB tables:
   ```bash
   npm install
   npx prisma generate
   npx prisma db push
   npm run db:seed
   ```

5. Start the API (leave this terminal open):
   ```bash
   npm run dev
   ```
   You should see: `FleetFlow API running at http://localhost:3001`.

---

### Step 3: Frontend

1. Open a **new** terminal.

2. Go to the frontend folder:
   ```bash
   cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\frontend
   ```

3. Install and run:
   ```bash
   npm install
   npm run dev
   ```

4. In the browser open: **http://localhost:5173**

---

### Step 4: Log in

Use any of these (password is the same for all):

| Email                     | Password    |
|---------------------------|------------|
| manager@fleetflow.com    | password123 |
| dispatcher@fleetflow.com | password123 |
| safety@fleetflow.com     | password123 |
| finance@fleetflow.com   | password123 |

---

## Summary

| Step | What to do |
|------|------------|
| 1 | Start PostgreSQL (Docker container or installed service). |
| 2 | In `backend`: copy `.env.example` to `.env`, set `DATABASE_URL` and `JWT_SECRET`. |
| 3 | In `backend`: `npm install` → `npx prisma generate` → `npx prisma db push` → `npm run db:seed` → `npm run dev`. |
| 4 | In `frontend`: `npm install` → `npm run dev`. |
| 5 | Open http://localhost:5173 and log in with a seed user. |

---

## Using Oracle instead of PostgreSQL

To use Oracle Database 21c with this app, the backend would need to be changed: Prisma would be replaced with an Oracle-compatible layer (e.g. `oracledb` driver and raw SQL or another ORM that supports Oracle). That would be a separate, larger change. If you want to go that route, say so and we can outline the steps.
