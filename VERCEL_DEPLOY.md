# Vercel Deployment Guide

This document explains how to deploy the AI News Aggregator to Vercel using a scheduled Serverless Function that runs the daily pipeline and sends the email digest.

## Overview
- Runtime: Python 3.11 Serverless Functions on Vercel
- Trigger: Vercel Cron (scheduled function)
- Data: External PostgreSQL (Neon, Supabase, Render, etc.)
- Email: SMTP with Gmail App Password or a transactional provider (e.g., Resend)
- Source of truth: `app/daily_runner.py` and `main.py`

## Prerequisites
- Vercel account with GitHub/GitLab/Bitbucket integration
- External PostgreSQL instance and credentials
- OpenAI API key
- Email sending method:
  - Option A: Gmail SMTP with App Password (may be restricted on some platforms)
  - Option B (recommended): Provider like Resend/SendGrid (HTTP API)
- Python 3.11 locally for optional testing, and `vercel` CLI installed (`npm i -g vercel`)

## Repo Preparation
1) Ensure dependencies are available for Vercel’s Python runtime:
   - Preferred: generate `requirements.txt` from `pyproject.toml`.
     - If you use `uv`: `uv pip compile pyproject.toml -o requirements.txt`
     - Or create `requirements.txt` manually matching `[project.dependencies]` in `pyproject.toml`.
2) Keep project layout so imports like `from app.daily_runner import run_daily_pipeline` work in functions.
3) Confirm DB URL envs in `app/database/connection.py` align with your hosted Postgres.

## New Files to Add
Create the following (names are suggestions; feel free to adjust):

- `vercel.json`
  ```json
  {
    "functions": {
      "api/**/*.py": { "runtime": "python3.11" }
    },
    "crons": [
      { "path": "/api/run", "schedule": "0 13 * * *" }
    ]
  }
  ```
  Notes:
  - The cron runs at 13:00 UTC daily; change as needed.
  - Python runtime must match your code’s version constraints.

- `api/run.py` (Serverless Function entry)
  ```python
  from http.server import BaseHTTPRequestHandler
  from urllib.parse import urlparse, parse_qs
  import json
  from app.daily_runner import run_daily_pipeline

  class handler(BaseHTTPRequestHandler):
      def do_GET(self):
          try:
              qs = parse_qs(urlparse(self.path).query)
              hours = int(qs.get("hours", ["24"]) [0])
              top_n = int(qs.get("top_n", ["10"]) [0])
          except Exception:
              hours, top_n = 24, 10
          result = run_daily_pipeline(hours=hours, top_n=top_n)
          status = 200 if result.get("success") else 500
          body = json.dumps(result, default=str).encode("utf-8")
          self.send_response(status)
          self.send_header("Content-Type", "application/json")
          self.send_header("Content-Length", str(len(body)))
          self.end_headers()
          self.wfile.write(body)
  ```
  Tips:
  - Keep the function idempotent and short; the platform enforces execution time limits.
  - For long jobs, consider splitting into multiple functions or using an external job runner.

## Environment Variables (Vercel Project → Settings → Environment Variables)
- Core:
  - `OPENAI_API_KEY`
  - `POSTGRES_HOST`
  - `POSTGRES_PORT` (e.g., `5432`)
  - `POSTGRES_DB`
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`
- Email (pick one approach):
  - SMTP (current code):
    - `MY_EMAIL` (sender and default recipient)
    - `APP_PASSWORD` (Gmail App Password)
    - Note: Some platforms restrict SMTP. If blocked, switch to a provider’s HTTP API.
  - Email provider (optional future change):
    - e.g., `RESEND_API_KEY` and adjust `app/services/email.py` to use HTTP API.
- Optional:
  - `PROXY_USERNAME`, `PROXY_PASSWORD` (for YouTube transcript proxy support)

Set each variable for the `Production` environment (and `Preview`/`Development` as needed).

## Database Setup
1) Provision a hosted Postgres (Neon, Supabase, etc.).
2) Fill in the env vars above with your DB credentials.
3) Create tables:
   - Option A (local once): run a short script that imports and executes your create-tables logic (e.g., `python -c "from app.database import models; from app.database.connection import engine; models.Base.metadata.create_all(engine)"`).
   - Option B (one-time function): add a temporary `api/migrate.py` that calls the same and hit it once, then remove.

## Scheduling
- The `vercel.json` `crons` entry triggers `GET /api/run` on the schedule.
- Times are in UTC; convert from your local timezone.
- To run ad-hoc: open the function URL or `curl` it with optional query params `hours` and `top_n`.

## Email Delivery Notes
- Current code sends via Gmail SMTP (`smtp.gmail.com:465`) using `MY_EMAIL` and `APP_PASSWORD`.
- If SMTP is blocked or unreliable, prefer an email API provider (e.g., Resend) and update `app/services/email.py` accordingly.

## Local Testing
1) Install deps locally (using your venv):
   - `pip install -r requirements.txt` (or `uv sync` if using uv)
2) Dry-run the pipeline:
   - `python main.py 24 10`
3) Test the function locally with Vercel CLI:
   - `vercel dev`
   - In another shell: `curl "http://localhost:3000/api/run?hours=24&top_n=10"`

## Deploy
1) Push to a Git repo and import into Vercel (or use `vercel` CLI in this folder).
2) In Vercel, set the Environment Variables.
3) Trigger a deployment; verify logs for the `api/run` function.
4) Confirm the cron invoked the function at the scheduled time (Logs → Cron Invocations).

## Observability & Limits
- Check Vercel Function logs for scraping/processing/email steps.
- Be mindful of execution time and memory limits. If the job is too slow:
  - Reduce `hours` window or `top_n`.
  - Split scraping/processing/email into separate endpoints and chain them via multiple crons.
  - Move heavy work to a dedicated job runner (container/VM) and keep Vercel as the scheduler.

## Common Pitfalls
- Missing `requirements.txt` → runtime import errors.
- Wrong DB host/port or blocked IP → connection failures.
- SMTP blocked by platform or provider throttling → switch to email API.
- Timezone confusion for cron → verify UTC vs. local time mapping.

## What You Don’t Need
- Docker is not required for Vercel Serverless Functions (keep `docker-compose.yml` for local Postgres only).
- A long-running web server; the function runs on-demand.

---

Scaffolded files: `vercel.json`, `api/run.py`, `api/migrate.py`, and `requirements.txt`. You can import into Vercel now; run `api/migrate.py` once (open its URL) to create tables, then remove or protect it.
