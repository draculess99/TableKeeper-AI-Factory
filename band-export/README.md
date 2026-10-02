# BAND Room Export

This directory contains the exported BAND Desktop room session for the TableKeeper Dark Factory submission.

## What Goes Here

The actual BAND room export includes:
- **Agent Logs**: Complete transcript of all agent-to-agent communications
- **Decision Records**: Choices made by each role (planner, implementer, test author, reviewer, integrator)
- **Handoff Evidence**: Documentation of work passed between roles
- **Message Transcripts**: Full conversation history and task progression
- **Rejection/Approval Records**: When work was accepted or rejected and why
- **Test Evidence**: Test suite outputs and verification results
- **Deployment Logs**: Integration and deployment verification

## Export Format

The BAND Desktop room export will be placed in this directory as a complete archive containing:
- `room-session.json` (or equivalent) — Full room state and history
- `agents/` — Individual agent logs
- `decisions/` — Decision records for each handoff
- `evidence/` — Supporting evidence files
- `README.md` — Export metadata and summary

## Before Submission

**DO NOT** invent or fabricate a room export. Instead:

1. Run the actual BAND Desktop application
2. Create a five-seat room with roles: Planner, Implementer, Test Author, Reviewer, Integrator
3. Execute the factory workflow (dispatch task → plan → implement → test → review → integrate)
4. Export the complete room session from BAND Desktop
5. Place the exported files in this directory
6. Commit to repository

## Export Instructions

**In BAND Desktop:**
1. Navigate to your room
2. Click "Export Room" or equivalent
3. Select export format (JSON, archive, etc.)
4. Save to `band-export/` directory
5. Commit: `git add band-export/; git commit -m "Add BAND room export"`

## Verification

After export is placed, verify:
```powershell
# Check that band-export/ contains exported files
ls band-export/

# Confirm it includes evidence of all five handoffs
# - Planner → Implementer
# - Implementer → Test Author
# - Test Author → Reviewer
# - Reviewer → Integrator
# - Integrator → Release
```

## Current Status

🔴 **PLACEHOLDER** — Awaiting actual BAND Desktop room export

This directory is currently a placeholder. The real room export will replace this file with complete evidence of the factory workflow in action.

---

**Related Documentation**:
- [FACTORY.md](../FACTORY.md) — BAND team structure and workflow
- [mandates/](../mandates/) — Role-specific standing instructions
- [stage-1/](../stage-1/) — Buildable service implementation
