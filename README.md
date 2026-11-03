# Ajaia Docs

Ajaia Docs is a lightweight collaborative document workspace built with Django. It supports authenticated workspaces, rich-text documents, autosave, document sharing with viewer/editor roles, and TXT/Markdown/DOCX import.

## Project structure\n\nSee [CODE_STRUCTURE.md](CODE_STRUCTURE.md) for the folder map and a summary of how requests, models, templates and frontend assets fit together.\n\n## Features

- Django username/password authentication, public account registration, and account profile settings.
- Show/hide password controls and a sign-out confirmation dialog.
- Create, rename, edit, autosave and delete documents.
- Quill rich-text editor with headings, bold, italic, underline, lists, blockquotes and links.
- Share documents with registered users as Viewer or Editor; server-side permissions are enforced.
- Import `.txt`, `.md` and `.docx` files (maximum 5 MB), create an editable document, retain the original file, download it, or delete the original independently.
- SQLite locally; PostgreSQL via `DATABASE_URL` in production.
- Django automated tests for document access and editor permissions.

## Requirements

- Python 3.10+
- pip

## Local setup (Windows PowerShell)

```powershell
cd ajaia-docs
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000. New users can register at `/accounts/signup/`; the first account can also be created with `python manage.py createsuperuser`. To demonstrate sharing, register a second account in a private/incognito browser window. Share by username.

### macOS / Linux

```bash
cd ajaia-docs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The example `.env` is a reference; the project reads environment variables directly. For local use, the built-in development secret is sufficient. Set a unique `SECRET_KEY` for any shared deployment.

## Run tests

```bash
python manage.py test
```

## File import behavior

Supported formats are `.txt`, `.md`, and `.docx`; maximum upload size is 5 MB. Imports create a new editable document. The original upload is retained in the database and can be downloaded or deleted from Uploaded files. Deleting the original upload does not delete the imported document. Images, PDFs and legacy `.doc` files are intentionally not supported.

## Deployment notes

The application supports PostgreSQL through `DATABASE_URL` and WhiteNoise for static assets. A production deployment needs a persistent PostgreSQL database and environment variables:

- `SECRET_KEY`: a long random secret.
- `DEBUG=False`
- `ALLOWED_HOSTS`: comma-separated hostnames.
- `CSRF_TRUSTED_ORIGINS`: comma-separated HTTPS origins, e.g. `https://your-app.onrender.com`.
- `DATABASE_URL`: PostgreSQL connection string.

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command:

```bash
gunicorn config.wsgi:application
```

For a Render deployment, provision a PostgreSQL database, configure the variables above, and use the build/start commands. Do not use ephemeral SQLite storage for production. The original uploaded files are stored as database binary data, avoiding reliance on an ephemeral web-service disk. Configure a real deployment and verify it before sharing a live URL.

## Security and limitations

- All document routes require login. Owner/editor/viewer permissions are checked server-side.
- Document HTML is sanitized with Bleach before storage and again before display.
- File extension, size and DOCX archive signature are checked server-side; uploaded files are served as attachments.
- This is a time-boxed assignment implementation, not an enterprise document platform. It does not include real-time multi-user editing, operational audit logs, version history, OAuth, virus scanning, or formal penetration testing.
- Quill is loaded from a public CDN; an offline deployment should vendor the library locally.
