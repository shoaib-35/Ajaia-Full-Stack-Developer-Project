# Ajaia Docs — Submission contents

## Included in this folder

- `manage.py` and `config/`: Django project configuration.
- `workspace/`: document, sharing, upload, account, UI and automated test implementation.
- `requirements.txt`: Python dependencies.
- `.env.example`: environment variable reference.
- `README.md`: local setup, run, test and deployment instructions.
- `ARCHITECTURE.md`: architecture, data model, access rules and tradeoffs.
- `AI_WORKFLOW.md`: AI usage and verification note (review and edit to reflect actual usage).
- `walkthrough_url.txt`: placeholder for the recorded walkthrough URL.

## Reviewer access

Create two local accounts (owner and recipient) using the public signup page at `/accounts/signup/` or `createsuperuser`, then share a document by recipient username. No demo credentials are hardcoded into the source. For a deployed review, provision dedicated test accounts and list their credentials here only after creating them securely.

## Live product and walkthrough

- Live product URL: NOT DEPLOYED — add the verified deployment URL after publishing.
- Walkthrough video: NOT RECORDED — add the unlisted Loom/YouTube URL to `walkthrough_url.txt`.
- Google Drive folder: upload this project folder and add its share link when ready.

## Known limitations

- No real-time collaborative editing, comments, suggestions or version history.
- No email-based invitations; sharing is by existing username.
- Supported imports: TXT, Markdown and DOCX only, up to 5 MB.
- Quill is loaded from a CDN.
- A production deployment and external reviewer accounts still need to be configured and verified.
