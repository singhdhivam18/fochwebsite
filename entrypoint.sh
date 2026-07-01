#!/usr/bin/env bash
# entrypoint.sh — runs inside the container on every start
set -euo pipefail

echo "[entrypoint] Collecting static files..."
python manage.py collectstatic --noinput

# ── Database migrations (Step 12 — deferred) ─────────────────────────────────
# The application uses pyodbc directly for SQL Server; it does NOT use Django
# ORM migrations for that database.  The SQLite line below only applies to
# Django's own internal tables (admin, auth, sessions).
# Uncomment when you are ready to initialise Django's internal database:
# python manage.py migrate --noinput

echo "[entrypoint] Starting Gunicorn..."
exec gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log
