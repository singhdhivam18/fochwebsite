# Foch Project

A Django web application for student management — tracks student profiles, attendance, expenses, and support records.

---

## Project Structure

```
fochdata/
├── coreapp/            # Main Django app (models, views, urls)
├── mysite/             # Django project settings
├── django_project/     # Docker & deployment config
├── static/             # CSS and JavaScript files
├── templates/          # HTML templates
├── media/              # User-uploaded files (not tracked in git)
├── dataaccess.py       # Database access layer
├── getconnectionstring.py  # Builds DB connection string from config
├── manage.py
├── requirements.txt
├── config.ini.example  # Copy to config.ini and fill in your DB details
└── django_project/
    └── .env.example    # Copy to .env.prod and fill in your secrets
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fochproject.git
cd fochproject/fochdata
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up config files

```bash
# Database config (used by getconnectionstring.py / dataaccess.py)
cp config.ini.example config.ini
# → Edit config.ini and fill in your DB credentials

# Environment variables (used by Django settings)
cp django_project/.env.example django_project/.env.prod
# → Edit .env.prod and fill in SECRET_KEY and DB details
```

### 4. Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Docker (Production)

```bash
cd django_project
docker-compose -f docker-compose.prod.yml up --build
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` in production |
| `DB_HOST` | Azure SQL / DB server hostname |
| `DB_PORT` | Database port (default: 1433) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |

---

## Notes

- `config.ini` and `.env.prod` are excluded from version control — never commit them.
- `media/` folder (uploaded receipts/files) is excluded from git — ensure your server has persistent storage configured.
- `db.sqlite3` is for local development only; production uses Azure SQL Server via ODBC.
