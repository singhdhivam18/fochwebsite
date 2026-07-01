# syntax=docker/dockerfile:1
#
# Production image — fochwebsite (Django + PyJWT + pyodbc → SQL Server)
# Project layout: manage.py at root, mysite/ = project package, coreapp/ = app
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential curl gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# ── Microsoft ODBC Driver 18 for SQL Server ───────────────────────────────────
# pyodbc (in requirements.txt) needs this driver installed at the OS level.
# Even though the database connection is deferred to Step 12, the driver must
# be present at build time or Django will crash when dataaccess.py is imported.
# Uses Microsoft's dynamic-version method so it adapts to whatever Debian
# version python:3.12-slim ships — no hardcoded Debian release number needed.
RUN curl -sSL -O "https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb" \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
       msodbcsql18 unixodbc-dev libgssapi-krb5-2 \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ───────────────────────────────────────────────────────
# Copy requirements first so Docker caches this layer; only rebuilt on change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application source ────────────────────────────────────────────────────────
COPY . .

# ── Runtime directories + non-root user ──────────────────────────────────────
# staticfiles/ is populated by collectstatic in entrypoint.sh.
# media/ and logs/ are bind-mounted from the host at runtime.
RUN mkdir -p staticfiles media logs \
    && chmod +x entrypoint.sh \
    && useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
