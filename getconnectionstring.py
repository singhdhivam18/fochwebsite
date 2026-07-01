"""
getconnectionstring.py
----------------------
Builds the SQL Server pyodbc connection string from environment variables.

REPLACES the previous config.ini approach.

config.ini has been REMOVED from the project because it contained hardcoded
credentials (sa / Test@123) and was committed to GitHub. Credentials now live
only in the .env file on the server (never committed — see .gitignore).

dataaccess.py imports `connectionstring` from this module at load time:
    from getconnectionstring import connectionstring

If DB_HOST / DB_NAME / DB_USER / DB_PASSWORD are not set yet (database is being
configured later per deployment Step 12), connectionstring will be an empty string.
Django starts fine; any actual DB query will fail with a clear pyodbc error at
request time — not at startup — which is the correct behaviour for the deferred-DB
phase.

Environment variables required (set in .env on the server):
    DB_DRIVER   — ODBC driver name  (default: ODBC Driver 18 for SQL Server)
    DB_HOST     — SQL Server host    (use host.docker.internal from Docker)
    DB_PORT     — SQL Server port    (default: 1433)
    DB_NAME     — database name      (ssms_new)
    DB_USER     — SQL login          (fochwebsite_user)
    DB_PASSWORD — SQL password
"""

import os

_driver   = os.getenv("DB_DRIVER",   "ODBC Driver 18 for SQL Server")
_host     = os.getenv("DB_HOST",     "")
_port     = os.getenv("DB_PORT",     "1433")
_database = os.getenv("DB_NAME",     "")
_uid      = os.getenv("DB_USER",     "")
_password = os.getenv("DB_PASSWORD", "")

if _host and _database and _uid and _password:
    connectionstring = (
        f"DRIVER={{{_driver}}};"
        f"SERVER={_host},{_port};"
        f"DATABASE={_database};"
        f"UID={_uid};"
        f"PWD={_password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
        f"ConnectRetryCount=3;"
        f"ConnectRetryInterval=10;"
    )
else:
    # DB env vars not set yet (Step 12 deferred).
    # App will start; any DB call will fail at request time with a clear error.
    connectionstring = ""
    import sys
    print(
        "[getconnectionstring] WARNING: DB_HOST / DB_NAME / DB_USER / DB_PASSWORD "
        "are not set. Database queries will fail until .env is updated and the "
        "container is restarted.",
        file=sys.stderr,
    )
