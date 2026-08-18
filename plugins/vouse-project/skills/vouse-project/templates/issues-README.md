# Known issues

One file per known bug or limitation: `issue-YYYY-MM-DD-<slug>.md`. These are
living documents — status and workarounds are edited in place as they change.

Create one with `python scripts/new_issue.py --slug <slug> --severity <sev>`
from the project root. Validate with `python scripts/check_issue.py issues/*.md`.

An issue is a **defect that exists in something already shipped or in use**. It
is not a task (that is a slice), not a question (that is a campaign), and not a
frozen result (that is `record/`). Filing an issue is not scheduling a fix —
fixing routes as a `kind: patch` slice that names the issue id.

Unresolved issues appear in MAP's generated table. Resolved ones stay here as
history and drop out of the table.
