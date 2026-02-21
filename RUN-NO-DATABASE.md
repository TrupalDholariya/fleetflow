# FleetFlow – Run without installing a database

The app now uses **SQLite**. Everything is stored in a single file (`backend/prisma/dev.db`). No PostgreSQL, Oracle, or Docker required.

---

## Step-by-step

### 1. Backend

Open a terminal and run:

```powershell
cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\backend
```

Create the env file (only needed for JWT and port; SQLite path is already in `.env.example`):

```powershell
copy .env.example .env
```

Optional: edit `.env` and set `JWT_SECRET` to any string (e.g. `my-secret-123`). You can leave `DATABASE_URL="file:./dev.db"` as is.

Install dependencies and create the database file:

```powershell
npm install
npx prisma generate
npx prisma db push
npm run db:seed
```

Start the API:

```powershell
npm run dev
```

Keep this terminal open. You should see: **FleetFlow API running at http://localhost:3001**.

---

### 2. Frontend

Open a **new** terminal:

```powershell
cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\frontend
npm install
npm run dev
```

---

### 3. Open the app

In your browser go to: **http://localhost:5173**

Log in with any of these (password for all: **password123**):

- manager@fleetflow.com  
- dispatcher@fleetflow.com  
- safety@fleetflow.com  
- finance@fleetflow.com  

---

## Summary

| Step | Where     | Command |
|------|------------|---------|
| 1    | `backend`  | `copy .env.example .env` |
| 2    | `backend`  | `npm install` |
| 3    | `backend`  | `npx prisma generate` |
| 4    | `backend`  | `npx prisma db push` |
| 5    | `backend`  | `npm run db:seed` |
| 6    | `backend`  | `npm run dev` |
| 7    | **New terminal** → `frontend` | `npm install` then `npm run dev` |
| 8    | Browser    | Open http://localhost:5173 and log in |

No database server to install or start—only Node.js and npm.

---

## Optional: Delay & Fuel Predictions

To use **Delay & Fuel Predictions** in the app:

1. Install Python 3.10+ and run (from `backend/predictors`):
   ```powershell
   pip install -r requirements.txt
   set OWM_API_KEY=your_openweather_key
   uvicorn server:app --port 8000
   ```
2. Keep that terminal open. The Node backend will call http://localhost:8000 when you use the Predictions page.
