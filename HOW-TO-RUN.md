# FleetFlow – All steps to run the project

Follow these steps in order. You need **Node.js** installed; no separate database (PostgreSQL/Oracle/Docker) is required.

---

## Prerequisites

- **Node.js 18+** (includes npm)  
  Download: https://nodejs.org (use the LTS version).  
  After installing, **close and reopen** your terminal, then run:
  ```powershell
  node -v
  npm -v
  ```
  You should see version numbers.

---

## Step 1: Backend setup and run

Open a terminal (PowerShell or Command Prompt).

**1.1** Go to the backend folder:
```powershell
cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\backend
```

**1.2** Create the environment file:
```powershell
copy .env.example .env
```
*(Optional: open `.env` and set `JWT_SECRET` to any string. Leave `DATABASE_URL` as is.)*

**1.3** Install dependencies:
```powershell
npm install
```

**1.4** Generate Prisma client and create the database (SQLite file):
```powershell
npx prisma generate
npx prisma db push
```

**1.5** Seed the database (users, sample vehicles, drivers, etc.):
```powershell
npm run db:seed
```

**1.6** Start the API:
```powershell
npm run dev
```
You should see: **FleetFlow API running at http://localhost:3001**.  
**Leave this terminal open.**

---

## Step 2: Frontend setup and run

Open a **new** terminal.

**2.1** Go to the frontend folder:
```powershell
cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\frontend
```

**2.2** Install dependencies:
```powershell
npm install
```

**2.3** Start the frontend:
```powershell
npm run dev
```
You should see a local URL (usually **http://localhost:5173**).  
**Leave this terminal open.**

---

## Step 3: Open the app and log in

1. In your browser, go to: **http://localhost:5173**
2. Log in with any of these accounts (same password for all):

| Email                     | Password     |
|---------------------------|--------------|
| manager@fleetflow.com     | password123  |
| dispatcher@fleetflow.com  | password123  |
| safety@fleetflow.com      | password123  |
| finance@fleetflow.com     | password123  |

3. Use the sidebar to open **Command Center**, **Vehicle Registry**, **Trip Dispatcher**, etc.

---

## Optional: Delay & Fuel Predictions

The **Delay & Fuel Predictions** page needs a small Python service. If you skip this, the rest of the app still works; only that page will show “predictor unavailable”.

**Optional step A:** Install **Python 3.10+** from https://www.python.org/downloads/ (during setup, check “Add Python to PATH”).

**Optional step B:** Open another terminal and run:

```powershell
cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\backend\predictors
pip install -r requirements.txt
uvicorn server:app --port 8000
```

*(Optional: for live weather, get a free API key from https://openweathermap.org/api and run:  
`set OWM_API_KEY=your_key` before the `uvicorn` command, or `set OWM_API_KEY=your_key&& uvicorn server:app --port 8000`.)*

**Optional step C:** Keep that terminal open. In the app, open **Delay & Fuel Predictions** from the sidebar and use the delay and fuel forms.

---

## Quick reference

| # | Where      | What to run |
|---|------------|-------------|
| 1 | Terminal 1 | `cd backend` → `copy .env.example .env` → `npm install` → `npx prisma generate` → `npx prisma db push` → `npm run db:seed` → `npm run dev` |
| 2 | Terminal 2 | `cd frontend` → `npm install` → `npm run dev` |
| 3 | Browser    | Open **http://localhost:5173** → log in with a seed user |
| 4 | (Optional) | Terminal 3: `cd backend\predictors` → `pip install -r requirements.txt` → `uvicorn server:app --port 8000` for Predictions page |

---

## Troubleshooting

- **“npm is not recognized”**  
  Install Node.js from https://nodejs.org and ensure “Add to PATH” is checked. Close all terminals and open a new one.

- **“Request failed with status code 500” or “Internal server error” on login**  
  The database is not set up or the backend is not reading it. From the **backend** folder run (in order):
  ```powershell
  cd c:\Users\Trupal Dholariya\OneDrive\Desktop\odoo\backend
  copy .env.example .env
  npx prisma generate
  npx prisma db push
  npm run db:seed
  ```
  Then start the backend again with `npm run dev`. Make sure you run all of these from inside the `backend` folder.

- **Backend or frontend port already in use**  
  Change `PORT=3001` in `backend\.env` or use another port for the frontend (e.g. in `frontend\vite.config.ts`).

- **Predictions page says predictor unavailable**  
  Start the Python predictor (Optional steps above) and ensure it is running on port 8000.
