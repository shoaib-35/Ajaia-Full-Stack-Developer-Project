# Submission Checklist

Use this file to prepare the final Ajaia Docs handoff. Replace every placeholder and pending status before sharing the project with reviewers.

## 1. Project information

- **Project name:** Ajaia Docs
- **Repository:** [ADD PUBLIC OR REVIEWER-ACCESSIBLE REPOSITORY URL]
- **Live application:** [ADD VERIFIED DEPLOYED APPLICATION URL]
- **Walkthrough video:** [ADD RECORDED VIDEO URL]
- **Submission Drive folder:** [ADD SHARED DRIVE FOLDER URL]

Do not submit placeholder URLs. Open each link in a private/incognito browser session or a separate account to confirm that the intended reviewer can access it.

## 2. Required source files

Confirm that the submission folder or repository includes:

- [ ] Django application source (`config/`, `workspace/`, and `manage.py`).
- [ ] Database migrations (`workspace/migrations/`).
- [ ] `requirements.txt`.
- [ ] `.gitignore`.
- [ ] `.env.example`, containing example configuration only and no real secrets.
- [ ] `README.md`.
- [ ] `ARCHITECTURE.md`.
- [ ] `CODE_STRUCTURE.md`.
- [ ] `AI_WORKFLOW.md`.
- [ ] `SUBMISSION.md`.
- [ ] Deployment configuration files, if used (`Procfile`, `render.yaml`).

Do not include `.venv/`, `__pycache__/`, compiled Python files, a local `db.sqlite3`, real `.env` files, or other machine-specific generated files.

## 3. Live application verification

Complete this section only after deploying the application.

- [ ] The live URL opens successfully over HTTPS.
- [ ] Registration and login work.
- [ ] A user can create, rename, edit, save, and reopen a document.
- [ ] Rich-text controls work as expected.
- [ ] A document owner can share a document with another registered user.
- [ ] A viewer can read but cannot edit the shared document.
- [ ] An editor can edit the shared document.
- [ ] An unshared user cannot access another user's private document.
- [ ] Supported TXT, Markdown, and DOCX imports have been checked.
- [ ] Uploaded-file download and deletion behavior has been checked.
- [ ] Static assets load correctly.
- [ ] The production database is persistent and connected.

Record any known issues or incomplete features below:

[ADD KNOWN ISSUES, OR WRITE “None known after the checks above” ONLY IF VERIFIED]

## 4. Reviewer access

If the application requires reviewers to sign in, provide test accounts through a secure channel or create accounts for the reviewers if the application supports registration.

| Role | Username | Password / access instructions |
|---|---|---|
| Owner | [ADD TEST USERNAME] | [SHARE SECURELY; DO NOT COMMIT PASSWORDS TO GIT] |
| Editor | [ADD TEST USERNAME] | [SHARE SECURELY; DO NOT COMMIT PASSWORDS TO GIT] |
| Viewer | [ADD TEST USERNAME] | [SHARE SECURELY; DO NOT COMMIT PASSWORDS TO GIT] |

Use non-personal test accounts and sample documents. Do not use real users' private documents or passwords.

If reviewers can register themselves and no preconfigured accounts are required, replace this table with clear registration and test instructions.

## 5. Automated checks

Run the following commands from the project directory in the same environment used for final verification:

```bash
python manage.py check
python manage.py test --verbosity 2
```

Record the actual results:

- **Django system check:** [PENDING — ADD ACTUAL RESULT]
- **Automated tests:** [PENDING — ADD ACTUAL RESULT AND TEST COUNT]
- **Date and environment tested:** [ADD DATE AND ENVIRONMENT]

Do not mark checks as passed unless the commands completed successfully. If a test fails, record the failure and whether it was resolved.

## 6. Walkthrough video (3–5 minutes)

The video should show the application running and demonstrate the main user journey:

1. Introduce Ajaia Docs and its purpose.
2. Register or sign in.
3. Create a document and demonstrate rich-text editing.
4. Show that edits are saved and the document can be reopened.
5. Rename and delete a sample document.
6. Import a supported file.
7. Share a document with another account.
8. Demonstrate the difference between Viewer and Editor permissions.
9. Briefly mention important limitations or future improvements.

Keep the video within the requested 3–5 minute duration. Confirm that the video link is accessible to reviewers.

## 7. Known scope limitations

The current assignment implementation does not include the following unless they have since been added and verified:

- Real-time simultaneous co-editing.
- Document version history.
- Comments or suggestion mode.
- Email-based sharing invitations.
- OAuth or social sign-in.
- Full preservation of complex DOCX formatting and tables.
- PDF, image, and legacy `.doc` import.

Mention any additional limitations discovered during final testing.

## 8. Final handoff checklist

- [ ] Source code is committed and pushed to the intended repository.
- [ ] Repository contains no secrets, local databases, or virtual environments.
- [ ] All project documentation has been reviewed and updated.
- [ ] Django checks and automated tests have been run; actual results are recorded.
- [ ] Live deployment has been tested, if a live URL is required.
- [ ] Reviewer access instructions or test accounts are ready.
- [ ] Walkthrough video is recorded and accessible.
- [ ] Drive folder contains the required deliverables.
- [ ] Repository, live app, video, and Drive links have been checked.
- [ ] All placeholders in this document have been replaced.

**Final status:** [NOT READY / READY FOR REVIEW — UPDATE AFTER COMPLETING THE CHECKLIST]
