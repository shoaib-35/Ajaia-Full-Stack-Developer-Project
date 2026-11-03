# Architecture and Product Decisions

## 1. Product scope

Ajaia Docs is a lightweight, Django-based document workspace. Its main workflow is:

1. A user registers or signs in.
2. The user creates a document or imports a supported file.
3. The user edits the document using the rich-text editor.
4. Changes are autosaved and stored in the database.
5. The user can reopen the document later.
6. The owner can share the document with another registered user and assign Viewer or Editor access.

The implementation prioritizes the core document lifecycle and access-control requirements within the assignment time limit. It does not implement real-time co-editing, version history, comments, or email-based invitations.

## 2. Application architecture

The application uses Django's server-rendered architecture:

- **`config/`** contains project-level settings, root URL routing, and the WSGI entry point.
- **`workspace/models.py`** defines the persistent document, sharing, and uploaded-file records.
- **`workspace/views.py`** handles page requests and document actions.
- **`workspace/services.py`** centralizes document access checks and HTML sanitization.
- **`workspace/forms.py`** contains form definitions used by the workspace.
- **`workspace/templates/`** contains the server-rendered pages and shared layout.
- **`workspace/static/`** contains the application's CSS and JavaScript.
- **Django authentication** manages user accounts and authenticated sessions.

The browser handles the editor interaction, while Django remains responsible for authentication, authorization, validation, and persistence.

## 3. Data model

The application uses three main workspace models.

### Document

A document stores its owner, HTML content, and timestamps. The owner relationship identifies the user who controls the document.

### DocumentShare

A sharing record connects a document to another user and stores that user's permission role:

- `viewer`: can open and read the document.
- `editor`: can open and modify the document content.

A uniqueness constraint prevents duplicate share records for the same document and user.

### UploadedFile

An uploaded-file record stores the uploader, an optional relationship to the document created from the upload, and the original file bytes. The upload size is limited to 5 MB.

The original upload is kept separately from the imported document content. This means deleting an original uploaded file does not automatically delete the document created from it.

## 4. Authorization model

Access is enforced on the server, not only by hiding or disabling interface controls.

| Action | Owner | Editor | Viewer |
|---|---:|---:|---:|
| Open and read document | Yes | Yes | Yes |
| Edit document content | Yes | Yes | No |
| Rename document | Yes | No | No |
| Manage sharing | Yes | No | No |
| Delete document | Yes | No | No |

The centralized access service determines whether a user owns a document or has a sharing record and role. Views use these checks before allowing protected operations.

This separation helps keep permission rules consistent across document pages and action endpoints.

## 5. Editing and autosave flow

The document editor uses Quill for rich-text editing. The editor produces HTML, which is sent to the Django backend when the user makes changes.

The save flow is:

1. The user edits the document in the browser.
2. JavaScript waits briefly after the latest edit before starting an autosave request (a 750 ms debounce).
3. The browser sends the document content as JSON and includes the Django CSRF token.
4. The backend validates the request and sanitizes the submitted HTML.
5. The sanitized content is saved to the database.
6. The interface updates its save status after the server acknowledges the request.

The backend uses an HTML tag, attribute, and protocol allowlist when sanitizing content. This reduces the risk of unsafe markup being stored and displayed.

The editor also warns users when they attempt to leave with changes that have not yet been acknowledged as saved. Autosave is not real-time collaboration: simultaneous edits from different users can still overwrite one another.

## 6. File import flow

The application accepts TXT, Markdown, and DOCX files up to 5 MB.

- **TXT:** decoded as UTF-8 and converted into document content.
- **Markdown:** decoded as UTF-8 and rendered into HTML.
- **DOCX:** paragraph text is extracted using `python-docx`.

Imported HTML passes through the same sanitization process used for editor content. The original file bytes are stored separately in the uploaded-file record.

DOCX import is intentionally limited: it extracts paragraph text and does not guarantee preservation of complex formatting, tables, or the full original Word layout. PDF, image, and legacy DOC imports are outside the supported scope.

## 7. Storage and deployment

SQLite is used for local development to keep setup simple. The application is configured to use PostgreSQL through the `DATABASE_URL` environment variable for deployment.

Gunicorn is used as the production WSGI server, and WhiteNoise is used to serve collected static assets. Uploaded originals are stored in the database rather than relying on a local upload directory, which avoids depending on an ephemeral application disk for those files.

Production deployment still requires correct environment variables, a persistent PostgreSQL database, and verification of the deployed application.

## 8. Interface principles

The interface uses a restrained visual style intended to keep document work clear and focused:

- Consistent navigation and page structure.
- Clear visual hierarchy and readable typography.
- Immediate feedback for actions such as saving.
- Consistent controls and spacing.
- Subtle transitions rather than distracting animation.
- Support for reduced-motion preferences where implemented.

Decorative translucency is used selectively rather than applied to every surface.

## 9. Technical trade-offs and future work

The implementation makes several deliberate scope trade-offs:

- **Django:** provides authentication, URL routing, server-side request handling, and database integration in one framework.
- **SQLite locally and PostgreSQL in deployment:** keeps local setup lightweight while supporting a production database.
- **Quill via CDN:** avoids the setup overhead of a separate frontend build pipeline, but the editor library depends on CDN availability.
- **Existing user accounts for sharing:** keeps sharing within the application without implementing email invitations.
- **Database storage for uploaded originals:** avoids relying on ephemeral local disk, with the trade-off that uploaded bytes contribute to database storage.

Potential improvements include:

- Automated integration testing of the complete user workflows.
- Deployment and production-configuration verification.
- Stronger upload inspection and operational monitoring.
- Conflict detection to reduce accidental overwrites during simultaneous editing.
- Version history, comments, and real-time collaboration.
- Email-based invitations and more granular sharing controls.

These are future improvements and should not be interpreted as features already implemented.
