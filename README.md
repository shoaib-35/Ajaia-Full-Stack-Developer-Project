# Ajaia Docs

Ajaia Docs is a lightweight document workspace built with Django. It supports authenticated user accounts, rich-text document editing, autosaving, document sharing with viewer/editor roles, and importing TXT, Markdown, and DOCX files.

## Features

- Username/password authentication and public account registration.
- Create, rename, edit, autosave, reopen, and delete documents.
- Quill rich-text editor with headings, bold, italic, underline, lists, blockquotes, and links.
- Share documents with registered users as Viewer or Editor.
- Enforce document ownership and sharing permissions on the server.
- Import `.txt`, `.md`, and `.docx` files up to 5 MB.
- Retain uploaded originals so they can be downloaded or deleted independently of the imported document.
- Use SQLite for local development and PostgreSQL through `DATABASE_URL` for production.
- Include Django automated tests for core authentication, document access, and editor-permission behavior.

## Project structure

See [CODE_STRUCTURE.md](CODE_STRUCTURE.md) for the project folder map and an explanation of how the Django configuration, models, views, templates, and frontend assets fit together.

## Requirements

- Python 3.10 or later
- pip

## Local setup

### Windows PowerShell

```powershell
cd ajaia-docs
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### macOS / Linux

```bash
cd ajaia-docs
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

New users can register at `/accounts/signup/`. You do not need to create a Django superuser for normal app usage. To create an administrator account for the Django admin interface, run:

```bash
python manage.py createsuperuser
```

To test document sharing, register a second user in another browser session and share a document with that user's username.

### Environment variables

The project reads configuration from environment variables. It does not automatically load a `.env` file, so do not assume that copying `.env.example` to `.env` will configure the application unless a dotenv loader has been added.

For local PowerShell development, you can set variables for the current terminal session:

```powershell
$env:SECRET_KEY = "your-local-development-secret"
$env:DEBUG = "True"
```

For production, set a unique secret key and the deployment variables described below through your hosting provider's environment-variable settings. Never commit real secrets or a populated `.env` file to Git.

## Validate the project and run tests

Run Django's system checks:

```bash
python manage.py check
```

Run the automated test suite:

```bash
python manage.py test --verbosity 2
```

Run these commands from the directory containing `manage.py`. Review the command output and resolve any reported errors before deployment.

## File import behavior

The application supports `.txt`, `.md`, and `.docx` uploads up to 5 MB. Importing a file creates a new editable document. The original uploaded file is retained and can be downloaded or deleted from the Uploaded files area.

Deleting the original upload does not delete the imported document. DOCX import extracts paragraph text; it does not preserve every feature of the original Word document, such as complex layouts or tables. PDF, image, and legacy `.doc` imports are not supported.

## Deployment

The project is configured to support PostgreSQL through `DATABASE_URL`, Gunicorn, and WhiteNoise for static assets. A production deployment requires a persistent PostgreSQL database and the following environment variables:

- `SECRET_KEY`: a long, randomly generated secret.
- `DEBUG`: set to `False`.
- `ALLOWED_HOSTS`: comma-separated allowed hostnames.
- `CSRF_TRUSTED_ORIGINS`: comma-separated trusted HTTPS origins, for example `https://your-app.onrender.com`.
- `DATABASE_URL`: the PostgreSQL connection string supplied by the database provider.

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command:

```bash
gunicorn config.wsgi:application
```

For Render, create a PostgreSQL database, add the required environment variables to the web service, and configure the build and start commands above. Do not use ephemeral SQLite storage for production. Uploaded originals are stored as database binary data, so they do not depend on an ephemeral web-service disk.

The presence of deployment configuration in the repository does not mean the application is already deployed. Verify the live service, database connection, static files, registration, document editing, and sharing before publishing a live URL.

## Security and limitations

- Document routes require authentication.
- Owner, editor, and viewer permissions are enforced by server-side checks.
- Document HTML is sanitized with Bleach before storage and again before display.
- Upload extension, size, and DOCX archive signature are checked server-side; uploaded originals are served as attachments.
- This is a time-boxed assignment implementation, not an enterprise document platform.
- Real-time multi-user editing, operational audit logs, version history, OAuth, virus scanning, and formal penetration testing are not included.
- Quill is loaded from a public CDN. An offline deployment would need to serve the library locally.

## Related project documentation

- [Architecture](ARCHITECTURE.md) — application design, data flow, and technical decisions.
- [Code structure](CODE_STRUCTURE.md) — directory layout and responsibilities.
- [AI workflow](AI_WORKFLOW.md) — how AI assistance was used and how suggestions were reviewed.
- [Submission checklist](SUBMISSION.md) — final links and materials required for handoff.
