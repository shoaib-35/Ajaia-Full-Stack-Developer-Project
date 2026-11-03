# Ajaia Docs — Project Structure

This document describes where the main application responsibilities live.

```text
ajaia-docs/
├── config/
│   ├── settings.py          Django settings and environment configuration
│   ├── urls.py              Project-level routes (authentication and app routes)
│   └── wsgi.py              WSGI application entry point
├── workspace/
│   ├── migrations/          Database schema migrations
│   ├── static/
│   │   ├── css/style.css    Application styling
│   │   └── js/
│   │       ├── app.js       Shared UI behavior (modals, sidebar, forms)
│   │       └── editor.js    Quill editor and autosave behavior
│   ├── templates/
│   │   ├── registration/    Login and signup pages
│   │   └── workspace/       Dashboard, editor, files and account pages
│   ├── admin.py             Django admin registrations
│   ├── apps.py              Workspace application configuration
│   ├── forms.py             Profile, sharing and signup forms
│   ├── models.py            Documents, sharing permissions and uploaded files
│   ├── services.py          HTML sanitization and document access checks
│   ├── urls.py              Workspace URL routes
│   ├── views.py             Request handling and application workflows
│   └── tests.py             Authentication and document permission tests
├── manage.py                Django management entry point
├── requirements.txt         Python dependencies
└── README.md                Setup, deployment and usage instructions
```

## Request and data flow

1. `config/urls.py` routes authentication URLs and includes `workspace.urls`.
2. `workspace/urls.py` maps application URLs to functions in `workspace/views.py`.
3. Views use forms from `forms.py`, database models from `models.py`, and shared
   security helpers from `services.py`.
4. Django templates render the pages. `style.css` controls presentation;
   `app.js` handles shared interface interactions.
5. The document editor uses Quill and `editor.js` to submit sanitized content
   to the document-save endpoint.
6. `tests.py` covers owner, viewer and editor access as well as signup.

## Maintenance notes

- Keep database schema changes in new Django migrations; do not edit an already
  applied migration to make routine model changes.
- Keep permission checks on the server in `services.py` and the relevant views.
  Frontend read-only controls are not a substitute for server-side authorization.
- Sanitize rich-text HTML before it is stored and before it is rendered.
- Do not commit `.env`, virtual environments, Python bytecode, or local cache
  directories.
