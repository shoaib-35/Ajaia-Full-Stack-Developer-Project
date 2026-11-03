# AI Workflow and Usage Notes

This document records where AI assistance contributed to the Ajaia Docs project and how generated suggestions were reviewed. It distinguishes assistance with planning and review from implementation work that was completed and verified by the developer.

## 1. AI tools used

- **ChatGPT:** Used during project planning and review conversations to help break down the assignment requirements, discuss application structure and permission behavior, review documentation, suggest interface improvements, explain Django implementation concepts, and troubleshoot Git workflow questions.
- **Other AI coding tools:** Add a tool here only if you actually used it while writing or changing the project code. Do not list a tool merely because it was available.

## 2. Where AI assistance helped

AI assistance was used for tasks such as:

- Organizing the assignment requirements into a practical implementation checklist.
- Discussing the Django application structure and the responsibilities of models, views, services, templates, and static assets.
- Reviewing the intended owner, editor, and viewer permission behavior.
- Explaining the document import and autosave workflows.
- Reviewing UI behavior and suggesting improvements to controls, layout, and confirmation interactions.
- Reviewing the project documentation for clarity, consistency, setup instructions, and submission readiness.
- Explaining Git errors encountered while connecting the local project to its GitHub repository.

These activities supported planning, understanding, review, and troubleshooting. They should not be interpreted as proof that every suggested code change was applied.

## 3. Generated suggestions reviewed or adapted

AI-generated suggestions were treated as drafts rather than accepted automatically.

Examples of review and adaptation included:

- **Project structure:** Suggestions were compared with the existing Django files so documentation would describe the actual repository rather than an assumed structure.
- **Permissions:** The owner/editor/viewer model was reviewed against the intended application behavior. Server-side checks remain necessary even when the interface hides or disables controls.
- **Delete confirmation:** A custom confirmation dialog was considered as a replacement for the browser's default confirmation prompt. It should only be described as implemented after the dialog has been integrated and tested across the relevant delete forms.
- **Environment setup:** Documentation was revised to avoid implying that Django automatically reads a `.env` file. Environment-variable instructions must match the configuration loader actually present in the project.
- **Documentation:** Placeholder text and ambiguous claims were identified for correction before final submission.

If you make further changes based on AI suggestions, add a concrete example here describing what you accepted, modified, or rejected.

## 4. Human review and verification

The developer remains responsible for deciding which suggestions to use, integrating changes, and verifying the result.

Before submission, verify the following against the final repository:

- The documented folder and file names match the submitted source.
- The README setup and deployment commands work in the target environment.
- The application starts and Django's system check completes successfully.
- The automated test suite is executed, and its actual result is recorded.
- Owner, editor, and viewer permissions are tested through the application.
- Document creation, editing, autosave, reopening, deletion, and supported imports are checked.
- The deployed application is tested using the production database and configured hostname.
- No secrets, local virtual environments, or local database files are included in the public repository.

Do not state that a test, deployment, or manual verification passed unless it was actually run and observed.

## 5. Test execution record

Complete this section after running the checks on the final version of the project.

| Check | Result |
|---|---|
| `python manage.py check` | Pending verification |
| `python manage.py test --verbosity 2` | Pending verification |
| Local manual workflow checks | Pending verification |
| Production deployment checks | Pending verification |

Replace each pending status with the actual outcome and, where useful, a short note about any issue found and fixed.

## 6. Known limitations

AI assistance does not replace testing or security review. The application still has the product limitations documented in `ARCHITECTURE.md` and `README.md`, including the absence of real-time co-editing and version history.

This note should be updated before handoff if additional AI tools were used, if the implementation workflow changes, or if the verification results become available.
