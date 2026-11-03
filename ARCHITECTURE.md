# Architecture and product decisions

## Product slice

Ajaia Docs focuses on the core document lifecycle: authenticate, create/import, edit, save, reopen, share and manage access. It deliberately avoids real-time co-editing and version history in the four-hour scope.

## Application structure

- `config/`: Django settings, root URLs and WSGI entry point.
- `workspace/models.py`: `Document`, `DocumentShare` and `UploadedFile` persistence.
- `workspace/views.py`: authenticated page and action endpoints.
- `workspace/services.py`: HTML sanitization and centralized access policy.
- `workspace/templates/`: server-rendered pages and reusable application shell.
- `workspace/static/`: responsive CSS and small JavaScript modules.

## Data model

- A `Document` has one owner, HTML content and timestamps.
- `DocumentShare` connects a document to a user with a `viewer` or `editor` role. A unique constraint prevents duplicate share rows.
- `UploadedFile` belongs to the uploading user and optionally references the imported document. Original bytes are stored in a database binary field (with a 5 MB cap) so deployment does not depend on ephemeral local disk.

## Authorization

The owner can view, edit, rename, share and delete. An editor can view and edit content. A viewer can view only. Every document endpoint checks access on the server; hiding controls in the browser is not treated as authorization. Share management and deletion are owner-only.

## Content and autosave

Quill produces HTML. The browser debounces edits for 750 ms and posts JSON with the Django CSRF token. The server validates payload size, sanitizes HTML with a tag/attribute/protocol allowlist and persists it. The editor exposes a save state. A navigation warning is shown when the current editor content differs from the last acknowledged save.

## Import pipeline

TXT and Markdown are decoded as UTF-8. Markdown is rendered to HTML. DOCX paragraphs are extracted with `python-docx`. All imported HTML passes through the same sanitizer as editor content. The original file bytes are stored separately, so deleting an upload does not delete the imported document.

## UI principles

The interface follows the recovered Apple Design skill: immediate feedback, restrained translucency, system typography, consistent navigation, accessible controls, subtle reversible transitions, and reduced-motion/reduced-transparency support. Glass effects are limited to the top navigation rather than applied to every surface.

## Tradeoffs and next steps

SQLite is used for frictionless local setup; PostgreSQL is supported for deployment. Quill is loaded from CDN to avoid spending the timebox bundling a frontend build. Sharing uses existing local accounts rather than invitations/email. The next 2–4 hours should go to integration testing, deployment verification, stronger upload inspection, conflict handling for simultaneous edits, and a reviewer-friendly demo account setup. Real-time collaboration should only follow after the basic permissions and persistence flows are validated.
