# Code Structure

This document maps the Ajaia Docs repository and explains the responsibility of each major part of the codebase.

## 1. Repository layout

```text
ajaia-docs/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── workspace/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── registration/
│   │   └── workspace/
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile
├── render.yaml
├── README.md
├── ARCHITECTURE.md
├── CODE_STRUCTURE.md
├── AI_WORKFLOW.md
└── SUBMISSION.md
```

The tree shows the main application files. Individual static files, templates, and migration files are contained within their respective directories.

## 2. Django project configuration

### `config/settings.py`

Contains Django project settings, including installed applications, middleware, templates, database configuration, static-file settings, authentication settings, and environment-based production configuration.

### `config/urls.py`

Defines the root URL configuration and connects the project URL routes to the workspace and authentication routes.

### `config/wsgi.py`

Provides the WSGI application entry point used by the production application server.

## 3. Workspace application

### `workspace/models.py`

Defines the database models:

- `Document` — document owner, content, and timestamps.
- `DocumentShare` — the relationship between a document and a shared user, including the viewer/editor role.
- `UploadedFile` — uploaded original file information and stored file bytes.

### `workspace/views.py`

Contains the request handlers for the workspace, including document listing and editing, document actions, sharing, uploaded-file operations, and account-related page flows.

Views are responsible for handling requests and responses. Access-control decisions are delegated to the service layer where appropriate.

### `workspace/services.py`

Contains shared application logic, including:

- Resolving a user's access level for a document.
- Requiring the appropriate access before protected operations.
- Sanitizing document HTML before it is stored or displayed.

Keeping these rules in a service module helps avoid duplicating permission and sanitization logic across views.

### `workspace/forms.py`

Contains Django form definitions used by the application.

### `workspace/urls.py`

Maps workspace URL patterns to their corresponding view functions.

### `workspace/migrations/`

Contains Django database migration files. Keep these files in version control: they describe the database schema changes required to create and update the application's tables.

### `workspace/tests.py`

Contains automated tests for important application behavior, including document ownership and persistence, access restrictions for unshared users, viewer/editor permissions, HTML sanitization during editor saves, and signup availability.

## 4. Templates

### `workspace/templates/registration/`

Contains authentication-related templates, such as the login and signup pages.

### `workspace/templates/workspace/`

Contains the main workspace pages, including the dashboard, document editor, and uploaded-file views.

Templates render the interface using Django's template language and receive page data from the corresponding views.

## 5. Static assets

### `workspace/static/css/`

Contains the stylesheets used by the application, including layout, navigation, editor, form, and responsive styling.

### `workspace/static/js/`

Contains browser-side JavaScript for interactive behavior such as editor initialization, autosave, and interface actions.

Quill is loaded by the editor page from a public CDN. Check the relevant template and JavaScript file when changing editor configuration or toolbar behavior.

## 6. Root-level files

| File | Responsibility |
|---|---|
| `manage.py` | Django command-line entry point for migrations, development server, tests, and administration. |
| `requirements.txt` | Python package dependencies. |
| `.env.example` | Example names and values for environment configuration; it is not itself a secret store. |
| `.gitignore` | Excludes local environments, secrets, generated files, and local database files from Git. |
| `Procfile` | Declares the production web process command for compatible hosting platforms. |
| `render.yaml` | Render deployment configuration. |
| `README.md` | Installation, local setup, validation, and deployment instructions. |
| `ARCHITECTURE.md` | Application architecture, data flow, and technical decisions. |
| `CODE_STRUCTURE.md` | This repository guide. |
| `AI_WORKFLOW.md` | Documents AI assistance and how generated suggestions were reviewed. |
| `SUBMISSION.md` | Final submission checklist and handoff links. |

## 7. Main request and data flow

A typical document-editing request follows this path:

1. The browser requests a workspace URL.
2. Django's URL configuration routes the request to a view.
3. The view checks authentication and asks the service layer to verify document access.
4. The view reads or updates the relevant model through Django's ORM.
5. Django returns a rendered template or a JSON response.
6. For editor changes, browser-side JavaScript sends the content to the save endpoint; the backend sanitizes and persists the content before acknowledging the save.

For imports, the upload request is validated and parsed by the backend. The resulting document content is sanitized and saved, while the original upload is retained in its uploaded-file record.

## 8. Maintenance notes

- Do not remove `workspace/migrations/` from the repository.
- Do not commit `.venv/`, `__pycache__/`, compiled Python files, local SQLite databases, or real environment secrets.
- Keep authorization checks on the backend even when the interface hides controls from viewers.
- Route document-content changes through the sanitization logic in the service layer.
- When adding a model field or changing a model, create and commit the corresponding Django migration.
- Update this document when the repository structure or responsibilities change.
