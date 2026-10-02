# TableKeeper - BAND Dark Factory Submission

This repository demonstrates a five-person BAND (Broadcast Asynchronous Negotiated Delivery) team structure for the WeAreDevelopers x BAND "Dark Factory" hackathon challenge.

## BAND Room Structure

The TableKeeper factory operates as a five-seat BAND room with specialized roles:

### 1. **Planner** 
- Receives task from product owner
- Decomposes into acceptance criteria
- Writes specification for implementer
- Rejects ambiguous or unbounded work

### 2. **Implementer**
- Receives specification from planner
- Builds solution to specification
- Writes clean, testable code
- Hands off to test author

### 3. **Test Author**
- Receives implementation from implementer
- Verifies all acceptance criteria met
- Runs comprehensive test suite
- Rejects failed implementations back to implementer

### 4. **Reviewer**
- Receives passing code from test author
- Conducts independent code review
- Verifies correctness, safety, maintainability
- Rejects code with issues back to implementer

### 5. **Integrator**
- Receives reviewed code from reviewer
- Merges into main branch
- Verifies deployment readiness
- Rejects integration failures back to reviewer

## Task Dispatch & Handoff Sequence

```
Product Owner
    ↓
[Planner] → writes specification
    ↓
[Implementer] → builds solution
    ↓
[Test Author] → verifies functionality
    ↓
[Reviewer] → audits code quality
    ↓
[Integrator] → deploys to production
    ↓
User/System
```

### Handoff Mechanics

**Planner → Implementer:**
- Task specification with acceptance criteria
- No solution prescribed (implementer has autonomy)

**Implementer → Test Author:**
- Clean, working code
- File change summary
- Implementation notes

**Test Author → Reviewer:**
- Tested implementation
- Full test suite results
- Evidence of passing verification

**Reviewer → Integrator:**
- Code review completion
- Security and architecture assessment
- Approval for integration

**Integrator → Release:**
- Merged code
- Regression test confirmation
- Deployment verification

## Rejection & Recovery

Each role can reject work back to its upstream source:

- **Planner rejects** to product owner (ambiguous requirements)
- **Implementer rejects** to planner (impossible spec) or accepts from planner
- **Test Author rejects** to implementer (failures) or accepts from implementer
- **Reviewer rejects** to implementer (quality issues) or accepts from test author
- **Integrator rejects** to reviewer (merge conflicts) or accepts from reviewer

Failed work returns to its source with specific feedback for correction.

## Mandate Design

Each role operates under a generic **mandate** (see `mandates/` folder):

- [planner.md](mandates/planner.md) — Specification writing, scope definition
- [implementer.md](mandates/implementer.md) — Clean code, minimal scope
- [test_author.md](mandates/test_author.md) — Verification, acceptance criteria
- [reviewer.md](mandates/reviewer.md) — Code quality, security, maintainability
- [integrator.md](mandates/integrator.md) — Merging, deployment, release

**Critical principle**: Mandates are generic—no mention of TableKeeper specifics (restaurants, reservations, tables, Flask routes, endpoint paths, field names, status codes, double-booking, etc.). Each mandate describes ownership, handoffs, evidence required, and rejection criteria.

## Verification Evidence

The factory produces evidence at each stage:

### Planner Evidence
- Task specification document
- Acceptance criteria (testable, measurable)
- Known unknowns and risks

### Implementer Evidence
- Source code changes
- File change summary
- Clean Git history

### Test Author Evidence
- Full test suite results (all passing)
- Test execution logs or screenshots
- Coverage summary (which criteria tested)

### Reviewer Evidence
- Code review checklist
- Security assessment
- Architectural alignment confirmation

### Integrator Evidence
- Merge confirmation (commit hash)
- Regression test results
- Deployment verification

## Testing & Quality Gates

The TableKeeper Stage 1 service includes comprehensive automated tests:

```powershell
# Run full test suite
pytest stage-1/test_app.py -v

# Expected result: 15 passed
# Tests cover: API endpoints, business logic, validation, error handling
```

Tests verify:
- ✅ Successful reservations
- ✅ Double-booking prevention
- ✅ Capacity validation
- ✅ Time validation
- ✅ Deletion workflow
- ✅ Error handling

## Docker Verification

Clean container build verifies deployment readiness:

```powershell
# Run the verification script
.\verify_clean_container.ps1

# Builds fresh Docker image from stage-1/
# Runs with --network none (no external access)
# Maps port 5000
# Confirms service starts
```

## Known Limitations

This is a **Stage 1 demo** implementation intended for the hackathon:

- **Ephemeral Database**: SQLite resets on restart (suitable for time-limited demo)
- **No Persistent Storage**: No volume mount used (data loss on restart)
- **Single-Process Deployment**: Development mode (not production-ready)
- **No Authentication**: Suitable for internal demo only

For production use:
- Migrate to PostgreSQL/MySQL
- Add persistent storage volume
- Deploy with multi-process app server
- Add authentication/authorization
- Implement comprehensive logging and monitoring

## Repository Structure

```
TableKeeper-AI-Factory/
├── FACTORY.md                          # This file
├── README.md                           # Repository overview
├── stage-1/                            # Complete Stage 1 service
│   ├── app.py
│   ├── test_app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── templates/index.html
│   └── README.md
├── mandates/                           # Generic standing instructions
│   ├── planner.md
│   ├── implementer.md
│   ├── test_author.md
│   ├── reviewer.md
│   └── integrator.md
├── band-export/                        # BAND room export (TBD)
│   └── README.md
├── verify_clean_container.ps1          # Docker verification script
├── docs/images/                        # Screenshots and evidence
└── Procfile                            # Deployment configuration
```

## BAND Room Export

A placeholder for the BAND Desktop room export is at `band-export/README.md`. The actual exported room session (with agent logs, decisions, message transcripts, and handoff evidence) will be placed in this directory before final submission.

## Getting Started with the Factory

### For Product Owners
1. Write task specification
2. Send to planner
3. Track progress through handoff sequence
4. Verify evidence at each gate

### For Developers (Planner Role)
1. See [mandates/planner.md](mandates/planner.md)
2. Read incoming task
3. Write acceptance criteria
4. Hand off to implementer

### For Developers (Implementer Role)
1. See [mandates/implementer.md](mandates/implementer.md)
2. Receive specification from planner
3. Build solution
4. Run `pytest stage-1/test_app.py -v` to verify
5. Hand off to test author

### For Developers (Test Author Role)
1. See [mandates/test_author.md](mandates/test_author.md)
2. Receive implementation from implementer
3. Run test suite: `pytest stage-1/test_app.py -v`
4. Verify all acceptance criteria met
5. Hand off (pass) or reject (fail)

### For Developers (Reviewer Role)
1. See [mandates/reviewer.md](mandates/reviewer.md)
2. Receive tested code from test author
3. Conduct code review
4. Check security, correctness, maintainability
5. Hand off (pass) or reject (fail)

### For Developers (Integrator Role)
1. See [mandates/integrator.md](mandates/integrator.md)
2. Receive reviewed code from reviewer
3. Merge into main branch
4. Run regression tests
5. Verify deployment: `.\verify_clean_container.ps1`
6. Confirm system operational

## Support

- **Architecture Questions**: See [FACTORY.md](FACTORY.md)
- **Role-Specific Instructions**: See [mandates/](mandates/)
- **Service Details**: See [stage-1/README.md](stage-1/README.md)
- **Testing**: Run `pytest stage-1/test_app.py -v`
- **Deployment**: Run `.\verify_clean_container.ps1`

## Submission

This submission includes:

1. ✅ **Stage 1 Service** (`stage-1/`) — Complete, buildable, testable implementation
2. ✅ **BAND Mandates** (`mandates/`) — Generic standing instructions for five roles
3. ✅ **Factory Documentation** (`FACTORY.md`) — Team structure, handoff sequence, evidence gates
4. ✅ **Verification Scripts** (`verify_clean_container.ps1`) — Docker build/run verification
5. ✅ **Test Suite** (`stage-1/test_app.py`) — 15 automated tests with full pass
6. ✅ **Room Export Placeholder** (`band-export/`) — Ready for BAND Desktop export
7. ✅ **Evidence Documentation** (`docs/images/`) — Screenshots of successful booking, double-booking prevention, and test results

---

**Submitted for**: WeAreDevelopers x BAND "Dark Factory" Hackathon Challenge  
**Stage**: 1 - MVP Demonstration  
**Date**: October 2026
