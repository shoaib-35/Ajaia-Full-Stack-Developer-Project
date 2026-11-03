# AI workflow note

This file is a submission template. Edit it to accurately reflect the tools and actions actually used during implementation; do not claim tool usage or verification that did not occur.

## Tools used

- ChatGPT: requirement decomposition, scope prioritization, architecture planning, implementation guidance and review checklists.
- AI coding assistant: [add the coding assistant actually used, or remove this item].

## Where AI accelerated the work

AI assistance was used to break the broad assignment into a small product slice, draft Django models and routes, outline permission rules, scaffold templates and frontend behavior, and create a focused test plan. The implementation was kept intentionally server-rendered to reduce setup and integration overhead.

## Output reviewed or rejected

The implementation avoids generated suggestions for real-time collaboration, complex OAuth, comments, version history and a full frontend framework because those features would threaten delivery of the core workflow in the timebox. Security-sensitive decisions—password handling, CSRF, server-side authorization and HTML sanitization—were implemented using Django facilities and explicit checks rather than trusting client-side UI state.

## Verification performed

Before submission, run and record the results of:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

Then manually verify login/logout, create/edit/reopen, autosave after refresh, upload each supported file type, download/delete original files, share as viewer/editor, and direct unauthorized URL/API access. Verify the deployed URL separately after deployment.

## Human judgment

The main product decision was to prioritize a complete document lifecycle and understandable sharing permissions over stretch features. The UI uses a restrained Apple-inspired visual language while preserving familiar document-editor conventions. Final claims in the submission should be limited to functionality that has actually been tested.
